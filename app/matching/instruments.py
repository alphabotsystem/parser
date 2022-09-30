from os import environ
from sys import maxsize as MAXSIZE
from asyncio import gather
from aiohttp import ClientSession
from lark import Token
from traceback import format_exc
from elasticsearch import AsyncElasticsearch
from helpers.constants import QUERY_SORT, STRICT_MATCH, EXCHANGE_TO_TRADINGVIEW, FREE_TRADINGVIEW_SOURCES
from helpers.lark import Ticker, TickerTree
from helpers.utils import TokenNotFoundException


elasticsearch = AsyncElasticsearch(
	cloud_id=environ["ELASTICSEARCH_CLOUD_ID"],
	api_key=environ["ELASTICSEARCH_API_KEY"],
)


async def match_ticker(tickerId, exchangeId, platform, assetClass):
	try:
		ticker = Ticker(tickerId)
	except:
		print(tickerId)
		print(format_exc())
		return None, "Requested ticker could not be found."

	try:
		await ticker_tree_search(ticker, exchangeId, platform, assetClass)
	except TokenNotFoundException as e:
		return None, e.message
	except:
		print(tickerId)
		print(format_exc())
		return None, "Requested ticker could not be found."

	isSimple = isinstance(ticker.children[0], Token) and ticker.children[0].type == "NAME"
	match = ticker.children[0].value if isSimple else {}
	if not isSimple and platform not in ["TradingView", "CoinGecko", "CCXT", "IEXC", "LLD"]:
		return None, f"Complex tickers aren't available on {platform}"

	response = {
		"tree": TickerTree().transform(ticker),
		"id": match.get("id", "Complex ticker"),
		"name": match.get("name", "Complex ticker"),
		"exchange": match.get("exchange", {}),
		"base": match.get("base"),
		"quote": match.get("quote"),
		"tag": match.get("tag"),
		"symbol": match.get("symbol"),
		"image": match.get("image"),
		"metadata": match.get("metadata", {"type": "Unknown", "rank": MAXSIZE}),
		"isSimple": isSimple
	}
	if isSimple: response["tradable"] = await find_tradable_market(match, response["exchange"])

	return response, None

async def ticker_tree_search(node, exchangeId, platform, assetClass):
	for i, child in enumerate(node.children):
		if not isinstance(child, Token):
			node.children[i] = await ticker_tree_search(child, exchangeId, platform, assetClass)
		elif child.type == "NAME":
			newValue = await find_instrument(child.value, exchangeId, platform, assetClass)
			node.children[i] = child.update(value=newValue)
	return node

async def prepare_instrument(instrument, exchangeId):
	if instrument is None: return None
	if instrument["market"]["source"] == "forex":
		exchange = {"id": "forex"}
	elif instrument["market"]["venue"] in ["CCXT", "IEXC"]:
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

def generate_query(search, tag, exchangeId, platform, assetClass):
	tickerQuery = {
		"bool": {
			"must": [{
				"bool": {
					"should": [{
						"match": {"ticker": search} # Ticker should match
					}, {
						"match": {"triggers.pair": search} # Any of the pair triggers should match
					}]
				}
			}, {
				"match": {"supports": platform} # Platform must be supported
			}]
		}
	}
	nameQuery = {
		"bool": {
			"must": [{
				"bool": {
					"should": [{
						"match": {"name": search} # Name should match
					}, {
						"match": {"triggers.name": search} # Any of the name triggers should match
					}]
				}
			}, {
				"match": {"supports": platform} # Platform must be supported
			}]
		}
	}

	if tag is not None:
		tickerQuery["bool"]["must"].append({"term": {"tag": int(tag)}})
		nameQuery["bool"]["must"].append({"term": {"tag": int(tag)}})
	if assetClass is not None:
		tickerQuery["bool"]["must"].append({"term": {"type": assetClass.lower()}})
		nameQuery["bool"]["must"].append({"term": {"type": assetClass.lower()}})
	if exchangeId is None:
		tickerQuery["bool"]["must"].append({"term": {"market.passive": False}})
		nameQuery["bool"]["must"].append({"term": {"market.passive": False}})
	else:
		tickerQuery["bool"]["must"].append({"term": {"market.source": exchangeId}})
		nameQuery["bool"]["must"].append({"term": {"market.source": exchangeId}})

	return tickerQuery, nameQuery

async def perform_search(tickerId, exchangeId, platform, assetClass=None, limit=1):
	search, tag = tickerId.lower().split(":") if ":" in tickerId else (tickerId.lower(), None)
	if tag is not None and not tag.isnumeric(): search, tag = tickerId.lower(), None

	# Generate queries and search by ticker first
	query1, query2 = generate_query(search, tag, exchangeId, platform, assetClass)
	response = await elasticsearch.search(index="assets", query=query1, sort=QUERY_SORT, size=limit)

	# Search by name if no results were found
	if response["hits"]["total"]["value"] == 0:
		response = await elasticsearch.search(index="assets", query=query2, sort=QUERY_SORT, size=limit)

	return response

async def find_instrument(tickerId, exchangeId, platform, assetClass):
	response = await perform_search(tickerId, exchangeId, platform, assetClass=assetClass)

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
			symbol = instrument["id"]
			exchange = EXCHANGE_TO_TRADINGVIEW.get(instrument["exchange"].get("id"), instrument["exchange"].get("id", "").upper())
			if exchange == "FOREX": exchange = ""
			if instrument["exchange"].get("id") in ["binanceusdm", "binancecoinm"] and not symbol.endswith("PERP"):
				instrument["id"] += "PERP"
				symbol += "PERP"
			if exchangeId is None and instrument["metadata"]["type"] != "Crypto":
				symbol = tickerId
				exchange = ""
			if ":" in symbol and exchange == "":
				exchange, symbol = symbol.split(":", 1)
			
			url = f"https://symbol-search.tradingview.com/symbol_search/?text={symbol}&hl=0&exchange={exchange}&lang=en&type=&domain=production"
			print(platform, url)
			async with session.get(url) as response:
				response = await response.json()
				if len(response) == 0:
					raise TokenNotFoundException("Requested ticker could not be found.")
				index = None
				if platform == "TradingView" and exchange == "":
					index = next((e for e in response if response[0]["symbol"] == e["symbol"] and e["exchange"] in FREE_TRADINGVIEW_SOURCES), None)

				if index is not None:
					instrument = {
						"id": index["symbol"],
						"name": index["description"],
						"base": None,
						"quote": None,
						"tag": 1,
						"symbol": index["symbol"],
						"exchange": {"id": "INDEX"},
						"metadata": {
							"type": "Unknown",
							"rank": MAXSIZE,
						}
					}
				elif "contracts" in response[0]:
					instrument = {
						"id": response[0]["contracts"][0]["symbol"],
						"name": response[0]["description"],
						"base": None,
						"quote": None,
						"tag": 1,
						"symbol": response[0]["contracts"][0]["symbol"],
						"exchange": {"id": response[0].get("prefix", response[0]["exchange"])},
						"metadata": {
							"type": "Unknown",
							"rank": MAXSIZE,
						}
					}
				else:
					instrument = {
						"id": response[0]["symbol"],
						"name": response[0]["description"],
						"base": None,
						"quote": None,
						"tag": 1,
						"symbol": response[0]["symbol"],
						"exchange": {"id": response[0].get("prefix", response[0]["exchange"])},
						"metadata": {
							"type": "Unknown",
							"rank": MAXSIZE,
						}
					}

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

async def find_listings(ticker, platform):
	query = {
		"bool": {
			"must": [{
				"term": { "base": ticker["base"].lower() }
			}, {
				"term": { "tag": int(ticker["tag"]) }
			}]
		}
	}
	if platform == "IEXC":
		query["bool"]["must"].append({"match": {"market.venue": "IEXC"}})
	else:
		query["bool"]["must"].append({"match": {"market.venue": "CCXT"}})

	instruments = await elasticsearch.search(index="assets", query=query, size=10000)
	exchanges = await elasticsearch.search(index="exchanges", query={"match_all": {}}, size=10000)

	sources = {}
	for instrument in instruments["hits"]["hits"]:
		if instrument["_source"]["quote"] in sources:
			sources[instrument["_source"]["quote"]].add(instrument["_source"]["market"]["source"])
		else:
			sources[instrument["_source"]["quote"]] = {instrument["_source"]["market"]["source"]}

	response, total = [], 0
	for quote in sources:
		names = []
		for source in sources[quote]:
			names.append(next((exchange["_source"]["name"] for exchange in exchanges["hits"]["hits"] if exchange["_source"]["id"] == source), None))
		response.append([quote, sorted(names)])
		total += len(names)

	return sorted(response, key=lambda x: x[0]), total

async def autocomplete_ticker(tickerId, platforms):
	tasks = []
	for platform in platforms:
		tasks.append(perform_search(tickerId, None, platform, limit=10000))
	responses = await gather(*tasks)
	
	tickers = []
	for platform, response in zip(platforms, responses):
		for hit in response["hits"]["hits"]:
			match = hit["_source"]
			base = match["base"] if match["tag"] == 1 else f"{match['base']}:{match['tag']}"
			suggestion = f"{base} | {match['name']} | {match['type']}"
			if suggestion not in tickers:
				tickers.append(suggestion)

	return tickers

async def autocomplete_venues(tickerId, platforms):
	tasks = []
	for platform in platforms:
		tasks.append(perform_search(tickerId, None, platform, limit=10000))
	tasks.append(elasticsearch.search(index="exchanges", query={"match_all": {}}, size=10000))
	responses = await gather(*tasks)

	ids = {}
	exchanges = responses.pop()
	for exchange in exchanges["hits"]["hits"]:
		ids[exchange["_source"]["id"]] = exchange["_source"]["name"]

	venues = []
	for platform, response in zip(platforms, responses):
		if platform == "CoinGecko" and response["hits"]["total"]["value"] > 0:
			venues.append("CoinGecko")
		else:
			for hit in response["hits"]["hits"]:
				if hit["_source"]["market"]["source"] == "forex":
					venue = "Forex"
				else:
					venue = ids[hit["_source"]["market"]["source"]]
				if venue not in venues:
					venues.append(venue)

	return venues