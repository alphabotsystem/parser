from os import environ
environ["PRODUCTION"] = environ["PRODUCTION"] if "PRODUCTION" in environ and environ["PRODUCTION"] else ""

from sys import maxsize as MAXSIZE
from time import time, sleep
from copy import deepcopy
from itertools import chain
from fastapi import FastAPI, Request
from uvicorn import Config, Server
from aiohttp import ClientSession
from asyncio import new_event_loop, set_event_loop, create_task
from lark import Token
from orjson import loads
from traceback import format_exc

import ccxt
from ccxt.base import decimal_to_precision as dtp
from elasticsearch import AsyncElasticsearch
from google.cloud.error_reporting import Client as ErrorReportingClient

from helpers.constants import STRICT_MATCH, EXCHANGE_SHORTCUTS, EXCHANGE_TO_TRADINGVIEW
from helpers.lark import Ticker, TickerTree
from helpers.utils import Utils, TokenNotFoundException


app = FastAPI()
elasticsearch = AsyncElasticsearch(
    cloud_id=environ["ELASTICSEARCH_CLOUD_ID"],
    api_key=environ["ELASTICSEARCH_API_KEY"],
)
logging = ErrorReportingClient(service="parser")
loop = new_event_loop()
set_event_loop(loop)


# -------------------------
# Exchange parsing
# -------------------------

def evaluate_exchange_match_score(raw, exchange):
	if raw == exchange["id"]: return len(raw)

	initials = "".join([word[0] for word in exchange["name"].split(" ")])
	if raw == initials: return len(raw)

	return Utils.overlap(raw, exchange["name"].replace(".", "").replace(" ", "").lower())

async def find_exchange(raw, platform, bias):
	if platform in ["CoinGecko"]: return {"success": False, "match": None}
	elif platform in ["CCXT", "Ichibot", "TradingLite", "Bookmap", "LLD"]: bias = "crypto"
	elif platform in ["IEXC"]: bias = "traditional"

	query = {
		"bool": {
			"must": [{
				"multi_match": {"query": raw, "fields": ["id", "name", "triggers.name", "triggers.shortcuts"]}
			}, {
				"match": {"supports": platform}
			}]
		}
	}
	response = await elasticsearch.search(index="exchanges", query=query, size=1)
	if response["hits"]["total"]["value"] > 0:
		exchange = response["hits"]["hits"][0]["_source"]
		return {"success": True, "match": exchange}
	return {"success": False, "match": None}


# -------------------------
# Main functions
# -------------------------

async def match_ticker(tickerId, exchangeId, platform, bias):
	if platform in ["CoinGecko", "CCXT", "Ichibot", "TradingLite", "Bookmap", "LLD"]: bias = "crypto"
	elif platform in ["IEXC"]: bias = "traditional"

	try:
		ticker = Ticker(tickerId)
	except:
		print(tickerId)
		print(format_exc())
		return {"response": None, "message": "Requested ticker could not be found."}

	try:
		await ticker_tree_search(ticker, exchangeId, platform, bias)
	except TokenNotFoundException as e:
		return {"response": None, "message": e.message}

	isSimple = isinstance(ticker.children[0], Token) and ticker.children[0].type == "NAME"
	match = ticker.children[0].value if isSimple else {}
	if not isSimple and platform not in ["TradingView", "CoinGecko", "CCXT", "IEXC", "LLD"]:
		return {"response": None, "message": f"Complex tickers aren't available on {platform}"}

	response = {
		"tree": TickerTree().transform(ticker),
		"id": match.get("id", "Complex ticker"),
		"name": match.get("name", "Complex ticker"),
		"exchange": match.get("exchange", {}),
		"base": match.get("base"),
		"quote": match.get("quote"),
		"symbol": match.get("symbol"),
		"image": match.get("image"),
		"metadata": match.get("metadata", {"type": "Unknown", "rank": MAXSIZE}),
		"isSimple": isSimple
	}
	if isSimple and bias == "crypto": response["tradable"] = await find_tradable_market(match, response["exchange"])

	return {"response": response, "message": None}

async def ticker_tree_search(node, exchangeId, platform, bias):
	for i, child in enumerate(node.children):
		if not isinstance(child, Token):
			node.children[i] = await ticker_tree_search(child, exchangeId, platform, bias)
		elif child.type == "NAME":
			newValue = await find_instrument(child.value, exchangeId, platform, bias)
			node.children[i] = child.update(value=newValue)
	return node

async def prepare_instrument(instrument, exchangeId):
	if instrument is None: return None
	if instrument["market"]["venue"] in ["CCXT", "IEXC"]:
		if exchangeId is None: exchangeId = instrument["market"]["source"]
		response = await elasticsearch.get(index="exchanges", id=exchangeId)
		exchange = response["_source"]
	else:
		exchange = {}
	return {
		"id": instrument["ticker"],
		"name": instrument["name"],
		"base": instrument["base"],
		"quote": instrument["quote"],
		"tag": instrument["tag"],
		"symbol": instrument["market"]["symbol"],
		"image": instrument.get("image"),
		"exchange": exchange,
		"metadata": {
			"type": instrument["type"],
			"rank": instrument["rank"]["base"],
		}
	}

async def find_instrument(tickerId, exchangeId, platform, bias):
	search, tag = tickerId.split(":") if ":" in tickerId else (tickerId, None)
	if tag is not None and not tag.isnumeric(): search, tag = tickerId, None

	sort = [{
		"rank.base": "asc",
		"rank.exchange": "asc",
		"rank.quote": "asc"
	}]
	query = {
		"bool": {
			"must": [{
				"bool": {
					"should": [{
						"term": {"base": search}
					}, {
						"match": {"name": search}
					}, {
						"match": {"ticker": search}
					}, {
						"match": {"triggers.name": search}
					}, {
						"match": {"triggers.pair": search}
					}]
				}
			}, {
				"match": {"supports": platform}
			}]
		}
	}
	if tag is not None:
		query["bool"]["must"].append({"term": {"tag": int(tag)}})
	if exchangeId is None:
		query["bool"]["must"].append({"term": {"market.passive": False}})
	else:
		query["bool"]["must"].append({"term": {"market.source": exchangeId}})

	response = await elasticsearch.search(index="assets", query=query, sort=sort, size=10)

	if response["hits"]["total"]["value"] == 0:
		if platform in STRICT_MATCH:
			raise TokenNotFoundException("Requested ticker could not be found.")
		else:
			if exchangeId is not None:
				response = await elasticsearch.get(index="exchanges", id=exchangeId)
				exchange = response["_source"]
			else:
				exchange = {}
			instrument = {
				"id": tickerId,
				"name": tickerId,
				"base": None,
				"quote": None,
				"tag": 1,
				"symbol": None,
				"exchange": exchange,
				"metadata": {
					"type": "Unknown",
					"rank": MAXSIZE,
				}
			}
	else:
		instrument = await prepare_instrument(response["hits"]["hits"][0]["_source"], exchangeId)

	if platform in ["TradingView", "TradingView Premium"]:
		async with ClientSession() as session:
			exchange = EXCHANGE_TO_TRADINGVIEW.get(instrument["exchange"].get("id"), instrument["exchange"].get("id", "").upper())
			symbol = instrument["id"]
			if instrument["exchange"].get("id") in ["binanceusdm", "binancecoinm"] and not symbol.endswith("PERP"):
				symbol += "PERP"
			url = f"https://symbol-search.tradingview.com/symbol_search/?text={symbol}&hl=0&exchange={exchange}&lang=en&type=&domain=production"
			print(url)
			async with session.get(url) as response:
				response = await response.json()
				if len(response) == 0:
					raise TokenNotFoundException("Requested ticker could not be found.")
				elif instrument["id"] != response[0]["symbol"]:
					print(f"Rewrite from {instrument['id']} to {response[0]['symbol']}")
					instrument["id"] = response[0]["symbol"]

	return instrument

async def find_tradable_market(match, exchange):
	if not exchange or exchange["id"] not in ["binance", "binanceusdm", "binancecoinm", "ftx"]: return None
	query = {
		"bool": {
			"must": [{
				"match": {"market.symbol": match["symbol"]}
			}, {
				"match": {"market.source": exchange["id"]}
			}]
		}
	}
	response = await elasticsearch.search(index="assets", query=query, size=1)
	if response["hits"]["total"]["value"] > 0:
		return response["hits"]["hits"][0]["_source"]["market"]["id"]
	return None


# -------------------------
# Endpoints
# -------------------------

@app.post("/parser/match_ticker")
async def run(req: Request):
	request = await req.json()
	return await match_ticker(request["tickerId"], request["exchangeId"], request["platform"], request["bias"])

@app.post("/parser/find_exchange")
async def run(req: Request):
	request = await req.json()
	return await find_exchange(request["raw"], request["platform"], request["bias"])

@app.post("/parser/get_listings")
async def get_listings(req: Request):
	request = await req.json()
	ticker = request["ticker"]

	query = {
		"bool": {
			"must": [{
				"term": { "base": ticker["base"] }
			}, {
				"term": { "tag": int(ticker["tag"]) }
			}]
		}
	}

	instruments = await elasticsearch.search(index="assets", query=query, size=10000)
	exchanges = await elasticsearch.search(index="exchanges", query={"match_all": {}}, size=10000)

	sources = {}
	for instrument in instruments["hits"]["hits"]:
		if instrument["_source"]["quote"] in sources:
			sources.add(instrument["_source"]["market"]["source"])
		else:
			sources[instrument["_source"]["quote"]] = {instrument["_source"]["market"]["source"]}

	response, total = [], 0
	for quote in sources:
		names = []
		for source in sources[quote]:
			names.append(next((exchange["_source"]["name"] for exchange in exchanges["hits"]["hits"] if exchange["_source"]["id"] == source), None))
		response.append([quote, sorted(names)])
		total += len(names)

	return {"response": response, "total": total}	

@app.post("/parser/get_formatted_price_ccxt")
async def format_price(req: Request):
	request = await req.json()
	exchange = getattr(ccxt, request["exchangeId"])()
	loop.run_in_executor(None, exchange.load_markets)
	precision = exchange.markets.get(request["symbol"], {}).get("precision", {}).get("price", 8)
	text = dtp.decimal_to_precision(request["price"], rounding_mode=dtp.ROUND, precision=precision, counting_mode=exchange.precisionMode, padding_mode=dtp.PAD_WITH_ZERO)
	return {"response": text.rstrip("0").rstrip(".")}

@app.post("/parser/get_formatted_amount_ccxt")
async def format_amount(req: Request):
	request = await req.json()
	exchange = getattr(ccxt, request["exchangeId"])()
	loop.run_in_executor(None, exchange.load_markets)
	precision = exchange.markets.get(request["symbol"], {}).get("precision", {}).get("amount", 8)
	text = dtp.decimal_to_precision(request["amount"], rounding_mode=dtp.TRUNCATE, precision=precision, counting_mode=exchange.precisionMode, padding_mode=dtp.NO_PADDING)
	return {"response": text.rstrip("0").rstrip(".")}

@app.post("/parser/get_venues")
async def get_venues(req: Request):
	request = await req.json()
	tickerId, platforms = request["tickerId"], request["platforms"]

	venues = []
	if platforms == "":
		venues += ["CoinGecko"]
		venues += [e["name"] for e in exchanges.values()]
	else:
		for platform in platforms.split(","):
			if platform == "CoinGecko":
				venues += ["CoinGecko"]
			else:
				venues += [e["name"] for e in exchanges.values() if platform in e["supports"]]
	return {"response": venues}


# -------------------------
# Startup
# -------------------------

if __name__ == "__main__":
	print("[Startup]: Ticker Parser is online")
	# config = Config(app=app, port=int(environ.get("PORT", 6900)), host="0.0.0.0", loop=loop)
	config = Config(app=app, port=6900, host="0.0.0.0", loop=loop)
	server = Server(config)
	loop.run_until_complete(server.serve())