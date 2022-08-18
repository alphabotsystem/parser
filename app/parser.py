from os import environ
environ["PRODUCTION"] = environ["PRODUCTION"] if "PRODUCTION" in environ and environ["PRODUCTION"] else ""

from sys import maxsize as MAXSIZE
from time import sleep
from datetime import datetime
from pytz import utc
from fastapi import FastAPI, Request
from uvicorn import Config, Server
from zmq import Context, Poller, ROUTER, REQ, LINGER, POLLIN
from asyncio import new_event_loop, set_event_loop, create_task
from lark import Token
from orjson import dumps, loads
from traceback import format_exc

import ccxt
from ccxt.base import decimal_to_precision as dtp
from google.cloud.firestore import Client
from google.cloud.error_reporting import Client as ErrorReportingClient

from TickerParser import Exchange

from assets import static_storage
from helpers.utils import Utils, TokenNotFoundException, STRICT_MATCH
from helpers import supported
from helpers.lark import Ticker, Reconstructor, TickerTree


app = FastAPI()
database = Client()
logging = ErrorReportingClient(service="parser")
loop = new_event_loop()
set_event_loop(loop)

exchanges = {}
ccxtIndex = {}
serumIndex = {}
coinGeckoIndex = {}
iexcStocksIndex = {}
iexcForexIndex = {}

coingeckoVsCurrencies = []
coingeckoFiatCurrencies = []


# -------------------------
# Startup
# -------------------------

def refresh_coingecko_index():
	global coinGeckoIndex, coingeckoVsCurrencies, coingeckoFiatCurrencies

	coingeckoVsCurrencies = database.collection("parser").document("coingecko").collection("meta").document("base").get().to_dict()["symbols"]
	coingeckoFiatCurrencies = database.collection("parser").document("coingecko").collection("meta").document("fiat").get().to_dict()["symbols"]

	pages = database.collection("parser").document("coingecko").collection("assets").get()
	coinGeckoIndex = {}
	for page in pages:
		for key, value in page.to_dict().items():
			coinGeckoIndex[key] = value

def refresh_ccxt_index():
	difference = set(ccxt.exchanges).symmetric_difference(supported.ccxtExchanges)
	newExchanges = []
	newSupportedExchanges = []
	unsupportedCryptoExchanges = []
	for e in difference:
		try:
			ex = getattr(ccxt, e)()
		except:
			unsupportedCryptoExchanges.append(e)
			continue
		if e not in supported.ccxtExchanges:
			if ex.has['fetchOHLCV'] != False and ex.has['fetchOrderBook'] != False and ex.timeframes is not None and len(ex.timeframes) != 0: newSupportedExchanges.append(e)
			else: newExchanges.append(e)
	if len(newSupportedExchanges) != 0: print(f"New supported CCXT exchanges: {newSupportedExchanges}")
	if len(newExchanges) != 0: print(f"New partially unsupported CCXT exchanges: {newExchanges}")
	if len(unsupportedCryptoExchanges) != 0: print(f"New deprecated CCXT exchanges: {unsupportedCryptoExchanges}")

	completedTasks = set()
	sortedIndexReference = {}

	for platform in supported.cryptoExchanges:
		if platform not in sortedIndexReference: sortedIndexReference[platform] = {}
		for exchange in supported.cryptoExchanges[platform]:
			if exchange not in completedTasks:
				completedTasks.add(exchange)
				if exchange not in exchanges:
					exchanges[exchange] = Exchange(exchange, "crypto" if exchange in ccxt.exchanges else "traditional")
					try: exchanges[exchange].properties.load_markets()
					except: continue

			for symbol in exchanges[exchange].properties.symbols:
				if '.' not in symbol and Utils.is_active(symbol, exchanges[exchange]):
					base = exchanges[exchange].properties.markets[symbol].get("base")
					quote = exchanges[exchange].properties.markets[symbol].get("quote")

					if base not in sortedIndexReference[platform]:
						sortedIndexReference[platform][base] = {}
					if quote not in sortedIndexReference[platform][base]:
						sortedIndexReference[platform][base][quote] = coinGeckoIndex.get(quote, {}).get("market_cap_rank", MAXSIZE)

	for platform in sortedIndexReference:
		ccxtIndex[platform] = {}
		for base in sortedIndexReference[platform]:
			if base not in ccxtIndex[platform]: ccxtIndex[platform][base] = []
			ccxtIndex[platform][base] = sorted(sortedIndexReference[platform][base].keys(), key=lambda quote: sortedIndexReference[platform][base][quote])
			try: ccxtIndex[platform][base].insert(0, ccxtIndex[platform][base].pop(ccxtIndex[platform][base].index("USDT")))
			except: pass
			try: ccxtIndex[platform][base].insert(0, ccxtIndex[platform][base].pop(ccxtIndex[platform][base].index("USD")))
			except: pass

def refresh_serum_index():
	try:
		rawData = []
		for i in range(3):
			socket = Context.instance().socket(REQ)
			socket.connect("tcp://serum-server:6900")
			socket.setsockopt(LINGER, 0)
			poller = Poller()
			poller.register(socket, POLLIN)

			socket.send(dumps({"endpoint": "list"}))
			responses = poller.poll(10000)

			if len(responses) != 0:
				response = socket.recv()
				socket.close()
				rawData = loads(response)
				break
			else:
				socket.close()

		for market in rawData["markets"]:
			base, quote = market["name"].split("/", 1)
			if base not in serumIndex:
				serumIndex[base] = []
			serumIndex[base].append({"id": market["address"], "name": base, "base": base, "quote": quote, "image": None, "program": market["programId"]})

		for token in rawData["tokenList"]:
			symbol = token["symbol"].upper()
			if symbol not in serumIndex:
				serumIndex[symbol] = []
			processed = []
			for market in serumIndex[symbol]:
				processed.append(market["quote"])
				market["name"] = token["name"]
				market["image"] = token.get("logoURI")
			for extension, address in token.get("extensions", {}).items():
				if extension.startswith("serumV3"):
					quote = extension.removeprefix("serumV3").upper()
					if quote not in processed:
						processed.append(quote)
						serumIndex[symbol].append({"id": address, "name": token["name"], "base": symbol, "quote": quote, "image": token.get("logoURI"), "program": "9xQeWvG816bUx9EPjHmaT23yvVM2ZWbrrpZb9PusVFin"})
			if len(serumIndex[symbol]) == 0:
				serumIndex.pop(symbol)
			elif serumIndex[symbol][0]["quote"] != "USDC":
				usdcMarket = None
				for index, market in enumerate(serumIndex[symbol]):
					if market["quote"] == "USDC":
						usdcMarket = serumIndex[symbol].pop(index)
						break
				if usdcMarket is not None:
					serumIndex[symbol].insert(0, usdcMarket)

	except Exception:
		print(format_exc())

def refresh_iexc_index():
	global exchanges, iexcStocksIndex, iexcForexIndex

	availableExchanges = set()
	suffixMap = {}

	index = database.collection("parser").document("iexc").collection("stocks").get()
	for doc in index:
		exchange = doc.to_dict()
		exchanges[doc.id] = Exchange.from_dict(exchange)
		suffixMap[doc.id] = exchange.pop("suffix", "")
		availableExchanges.add(doc.id)

	difference = set(availableExchanges).symmetric_difference(supported.iexcExchanges)
	newSupportedExchanges = []
	unsupportedCryptoExchanges = []
	for exchangeId in difference:
		if exchangeId not in supported.iexcExchanges:
			newSupportedExchanges.append(exchangeId)
		else:
			unsupportedCryptoExchanges.append(exchangeId)
	if len(newSupportedExchanges) != 0: print(f"New supported IEXC exchanges: {newSupportedExchanges}")
	if len(unsupportedCryptoExchanges) != 0: print(f"New deprecated IEXC exchanges: {unsupportedCryptoExchanges}")

	for exchangeId in supported.traditionalExchanges["IEXC"]:
		suffix = suffixMap.get(exchangeId)
		pages = database.collection("parser").document("iexc").collection("stocks").document(exchangeId).collection("markets").get()
		for page in pages:
			for tickerId, market in page.to_dict().items():
				exchanges[exchangeId].properties.symbols.append(tickerId)
				exchanges[exchangeId].properties.markets[tickerId] = market
				if tickerId not in iexcStocksIndex:
					iexcStocksIndex[tickerId] = {"id": tickerId.removesuffix(suffix), "name": market["name"], "base": tickerId.removesuffix(suffix), "quote": market["quote"], "exchanges": [exchangeId]}
				else:
					iexcStocksIndex[tickerId]["exchanges"].append(exchangeId)

	iexcForexIndex = database.collection("parser").document("iexc").collection("forex").document("index").get().to_dict()


# -------------------------
# Main functions
# -------------------------

def find_exchange(raw, platform, bias):
	if platform not in supported.cryptoExchanges and platform not in supported.traditionalExchanges: return {"success": False, "match": None}
	if raw in ["pro"]: return {"success": False, "match": None}

	shortcuts = {
		"crypto": {
			"binance": ["bin", "bi", "b", "nance"],
			"bitmex": ["bmx", "mex", "btmx"],
			"binanceusdm": ["binancefutures", "binancef", "fbin", "binf", "bif", "bnf"],
			"coinbasepro": ["cbp", "coin", "base", "cb", "coinbase", "coinbasepro", "cbpro"],
			"bitfinex2": ["bfx", "finex"],
		},
		"traditional": {}
	}

	if platform in ["TradingLite", "Bookmap", "GoCharting", "LLD", "CoinGecko", "CCXT", "Serum", "Ichibot"]:
		bias = "crypto"
	elif platform in ["IEXC"]:
		bias = "traditional"

	if bias == "crypto":
		for exchangeId in supported.cryptoExchanges[platform]:
			if exchangeId in shortcuts["crypto"] and raw in shortcuts["crypto"][exchangeId]:
				return {"success": True, "match": exchanges[exchangeId].to_dict()}
			if exchangeId in exchanges and exchanges[exchangeId].name is not None:
				name = exchanges[exchangeId].name.split(" ")[0].lower()
				nameNoSpaces = exchanges[exchangeId].name.replace(" ", "").replace(".", "").lower()
			else:
				name, nameNoSpaces = exchangeId, exchangeId

			if len(name) * 0.25 > len(raw): continue

			if name.startswith(raw) or name.endswith(raw):
				return {"success": True, "match": exchanges[exchangeId].to_dict()}
			elif nameNoSpaces.startswith(raw) or nameNoSpaces.endswith(raw):
				return {"success": True, "match": exchanges[exchangeId].to_dict()}
			elif exchangeId.startswith(raw) or exchangeId.endswith(raw):
				return {"success": True, "match": exchanges[exchangeId].to_dict()}

		for platform in supported.cryptoExchanges:
			for exchangeId in supported.cryptoExchanges[platform]:
				if exchangeId in shortcuts["crypto"] and raw in shortcuts["crypto"][exchangeId]:
					return {"success": False, "match": exchanges[exchangeId].to_dict()}
				if exchangeId in exchanges and exchanges[exchangeId].name is not None:
					name = exchanges[exchangeId].name.split(" ")[0].lower()
					nameNoSpaces = exchanges[exchangeId].name.replace(" ", "").replace(".", "").lower()
				else:
					name, nameNoSpaces = exchangeId, exchangeId

				if name.startswith(raw) or name.endswith(raw):
					return {"success": False, "match": exchanges[exchangeId].to_dict()}
				elif nameNoSpaces.startswith(raw) or nameNoSpaces.endswith(raw):
					return {"success": False, "match": exchanges[exchangeId].to_dict()}
				elif exchangeId.startswith(raw) or exchangeId.endswith(raw):
					return {"success": False, "match": exchanges[exchangeId].to_dict()}

	else:
		for exchangeId in supported.traditionalExchanges[platform]:
			if exchangeId in shortcuts["traditional"] and raw in shortcuts["traditional"][exchangeId]:
				return {"success": True, "match": exchanges[exchangeId].to_dict()}
			if exchangeId in exchanges and exchanges[exchangeId].name is not None:
				name = exchanges[exchangeId].name.split(" ")[0].lower()
				nameNoSpaces = exchanges[exchangeId].name.replace(" ", "").replace(".", "").lower()
			else:
				name, nameNoSpaces = exchangeId, exchangeId

			if len(name) * 0.25 > len(raw): continue

			if name.startswith(raw) or name.endswith(raw):
				return {"success": True, "match": exchanges[exchangeId].to_dict()}
			elif nameNoSpaces.startswith(raw) or nameNoSpaces.endswith(raw):
				return {"success": True, "match": exchanges[exchangeId].to_dict()}
			elif exchangeId.startswith(raw) or exchangeId.endswith(raw):
				return {"success": True, "match": exchanges[exchangeId].to_dict()}

		for platform in supported.traditionalExchanges:
			for exchangeId in supported.traditionalExchanges[platform]:
				if exchangeId in shortcuts["traditional"] and raw in shortcuts["traditional"][exchangeId]:
					return {"success": False, "match": exchanges[exchangeId].to_dict()}
				if exchangeId in exchanges and exchanges[exchangeId].name is not None:
					name = exchanges[exchangeId].name.split(" ")[0].lower()
					nameNoSpaces = exchanges[exchangeId].name.replace(" ", "").replace(".", "").lower()
				else:
					name, nameNoSpaces = exchangeId, exchangeId

				if name.startswith(raw) or name.endswith(raw):
					return {"success": False, "match": exchanges[exchangeId].to_dict()}
				elif nameNoSpaces.startswith(raw) or nameNoSpaces.endswith(raw):
					return {"success": False, "match": exchanges[exchangeId].to_dict()}
				elif exchangeId.startswith(raw) or exchangeId.endswith(raw):
					return {"success": False, "match": exchanges[exchangeId].to_dict()}

	return {"success": False, "match": None}

def match_ticker(tickerId, exchangeId, platform, bias):
	if platform in ["TradingLite", "Bookmap", "LLD", "CoinGecko", "CCXT", "Serum", "Ichibot"]: bias = "crypto"
	elif platform in ["IEXC"]: bias = "traditional"

	exchange = {} if exchangeId == "" else exchanges.get(exchangeId).to_dict()

	try:
		ticker = Ticker(tickerId)
	except:
		print(tickerId)
		print(format_exc())
		return {"response": None, "message": "Requested ticker could not be found."}

	try:
		ticker_tree_search(ticker, exchangeId, platform, bias, shouldMatch=True)
	except TokenNotFoundException as e:
		return {"response": None, "message": e.message}

	isSimple = isinstance(ticker.children[0], Token) and ticker.children[0].type == "NAME"
	simpleTicker = ticker.children[0].value if isSimple else {}
	if not isSimple and platform not in ["TradingView", "TradingView Premium", "CoinGecko", "CCXT", "Serum", "IEXC", "LLD"]:
		return {"response": None, "message": f"Aggregated tickers aren't available on {platform}"}

	reconstructedId = Reconstructor.reconstruct(ticker_tree_search(Ticker(tickerId), exchangeId, platform, bias))

	response = {
		"tree": TickerTree().transform(ticker),
		"id": reconstructedId,
		"name": simpleTicker.get("name", reconstructedId),
		"exchange": simpleTicker.get("exchange", {}),
		"base": simpleTicker.get("base"),
		"quote": simpleTicker.get("quote"),
		"symbol": simpleTicker.get("symbol"),
		"image": simpleTicker.get("image", static_storage.icon),
		"mcapRank": simpleTicker.get("mcapRank", MAXSIZE),
		"isSimple": isSimple
	}
	if isSimple and bias == "crypto": response["tradable"] = find_tradable_markets(reconstructedId, exchangeId, platform)

	return {"response": response, "message": None}

def ticker_tree_search(node, exchangeId, platform, bias, shouldMatch=False):
	for i, child in enumerate(node.children):
		if not isinstance(child, Token):
			node.children[i] = ticker_tree_search(child, exchangeId, platform, bias, shouldMatch)
		elif child.type == "NAME":
			newValue = internal_match(child.value, exchangeId, platform, bias)
			if not shouldMatch: newValue = newValue["id"]
			node.children[i] = child.update(value=newValue)
	return node

def internal_match(tickerId, exchangeId, platform, bias):
	ticker = None
	if bias == "crypto":
		if platform == "CoinGecko" and exchangeId == "": ticker = find_coingecko_crypto_market(tickerId)
		elif platform == "Serum" and exchangeId == "": ticker = find_serum_crypto_market(tickerId)
		else: ticker = find_ccxt_crypto_market(tickerId, exchangeId, platform)
	else:
		if platform == "IEXC": ticker = find_iexc_market(tickerId, exchangeId, platform)
	if ticker is None:
		if platform in STRICT_MATCH:
			raise TokenNotFoundException("Requested ticker could not be found.")
		return {
			"id": tickerId,
			"name": tickerId,
			"base": None,
			"quote": None,
			"symbol": None,
			"exchange": {} if exchangeId == "" else exchanges.get(exchangeId).to_dict(),
			"mcapRank": MAXSIZE
		}
	return ticker

def find_ccxt_crypto_market(tickerId, exchangeId, platform):
	exchange = None if exchangeId == "" else exchanges[exchangeId]
	if platform not in supported.cryptoExchanges or (exchange is not None and exchange.type != "crypto"): return None
	relevantExchanges = [exchanges[e] for e in supported.cryptoExchanges[platform] if exchanges[e].type == "crypto"] if exchange is None else [exchange]

	for e in relevantExchanges:
		if e.properties is not None and e.properties.symbols is not None:
			if tickerId in ccxtIndex[platform]:
				for quote in ccxtIndex[platform][tickerId]:
					symbol = f"{tickerId}/{quote}"
					if symbol in e.properties.symbols:
						if exchange is None and platform not in ["Ichibot"] and Utils.is_tokenized_stock(e, symbol): continue
						base = e.properties.markets[symbol].get("base")
						quote = e.properties.markets[symbol].get("quote")
						if not base in coingeckoFiatCurrencies and Utils.is_active(symbol, e):
							marketId = Utils.generate_market_id(symbol, e)
							return {
								"id": marketId,
								"name": coinGeckoIndex.get(tickerId, {}).get("name", marketId),
								"base": tickerId,
								"quote": quote,
								"symbol": symbol,
								"image": coinGeckoIndex.get(tickerId, {}).get("image", static_storage.icon),
								"exchange": e.to_dict(),
								"mcapRank": coinGeckoIndex.get(tickerId, {}).get("market_cap_rank", MAXSIZE)
							}

			else:
				currentBestMatch = MAXSIZE
				currentBestFit = MAXSIZE
				currentResult = None
				for symbol in e.properties.symbols:
					if exchange is None and platform not in ["Ichibot"] and Utils.is_tokenized_stock(e, symbol): continue
					base = e.properties.markets[symbol].get("base")
					quote = e.properties.markets[symbol].get("quote")
					marketPair = symbol.split("/")
					marketId = Utils.generate_market_id(symbol, e)
					mcapRank = coinGeckoIndex.get(base, {}).get("market_cap_rank", MAXSIZE)
					if Utils.is_active(symbol, e):
						if len(marketPair) == 1:
							if (tickerId == base or (marketId.startswith(tickerId) and len(marketId) * 0.5 <= len(tickerId))) and currentBestFit > 2:
								currentBestFit = 2
								currentResult = {
									"id": marketId,
									"name": coinGeckoIndex.get(base, {}).get("name", marketId),
									"base": base,
									"quote": quote,
									"symbol": symbol,
									"image": coinGeckoIndex.get(base, {}).get("image", static_storage.icon),
									"exchange": e.to_dict(),
									"mcapRank": mcapRank
								}

						elif base in ccxtIndex[platform] and quote in ccxtIndex[platform][base]:
							rankScore = ccxtIndex[platform][base].index(quote)
							if (tickerId == base + quote or (marketId.startswith(tickerId) and len(marketId) * 0.5 <= len(tickerId))) and currentBestFit >= 1 and base not in coingeckoFiatCurrencies and rankScore < currentBestMatch:
								currentBestMatch = rankScore
								currentBestFit = 1
								currentResult = {
									"id": marketId,
									"name": coinGeckoIndex.get(base, {}).get("name", marketId),
									"base": base,
									"quote": quote,
									"symbol": symbol,
									"image": coinGeckoIndex.get(base, {}).get("image", static_storage.icon),
									"exchange": e.to_dict(),
									"mcapRank": mcapRank
								}

				if currentResult is not None: return currentResult

	return None

def find_coingecko_crypto_market(tickerId):
	split = tickerId.split(":")
	if len(split) == 2:
		_tickerId, rank = split[0], "" if split[1] == "1" else f":{split[1]}"
	elif len(split) == 3:
		_tickerId, rank = split[0] + split[2], "" if split[1] == "1" else f":{split[1]}"
	else:
		_tickerId, rank = tickerId, ""

	if _tickerId in coinGeckoIndex:
		return {
			"id": f"{_tickerId}USD",
			"name": coinGeckoIndex[_tickerId]["name"],
			"base": _tickerId,
			"quote": "USD",
			"symbol": coinGeckoIndex[_tickerId]["id"],
			"image": coinGeckoIndex[_tickerId].get("image"),
			"exchange": {},
			"mcapRank": coinGeckoIndex[_tickerId]["market_cap_rank"]
		}

	else:
		for base in coinGeckoIndex:
			if _tickerId.startswith(base) and base + rank in coinGeckoIndex:
				for quote in coingeckoVsCurrencies:
					if _tickerId == f"{base}{quote}":
						return {
							"id": _tickerId,
							"name": coinGeckoIndex[base + rank]["name"],
							"base": base + rank,
							"quote": quote,
							"symbol": coinGeckoIndex[base + rank]["id"],
							"image": coinGeckoIndex[base + rank].get("image"),
							"exchange": {},
							"mcapRank": coinGeckoIndex[base + rank]["market_cap_rank"]
						}

	return None

def find_iexc_market(tickerId, exchangeId, platform):
	exchange = None if exchangeId == "" else exchanges[exchangeId]
	if platform not in supported.traditionalExchanges or (exchange is not None and exchange.type != "traditional"): return None
	relevantExchanges = [exchanges[e] for e in supported.traditionalExchanges[platform] if exchanges[e].type == "traditional"] if exchange is None else [exchange]

	if tickerId in iexcForexIndex and exchange is None:
		matchedTicker = iexcForexIndex[tickerId]
		return {
			"id": matchedTicker["id"],
			"name": matchedTicker["name"],
			"base": matchedTicker["id"],
			"quote": matchedTicker["quote"],
			"symbol": f"{matchedTicker['base']}/{matchedTicker['quote']}",
			"exchange": { "id": "fx" }
		}

	elif tickerId + "USD" in iexcForexIndex and exchange is None:
		matchedTicker = iexcForexIndex[tickerId + "USD"]
		return {
			"id": matchedTicker["id"],
			"name": matchedTicker["name"],
			"base": matchedTicker["id"],
			"quote": matchedTicker["quote"],
			"symbol": f"{matchedTicker['base']}/{matchedTicker['quote']}",
			"exchange": { "id": "fx" }
		}

	elif tickerId in iexcStocksIndex and exchange is None:
		matchedTicker = iexcStocksIndex[tickerId]
		return {
			"id": matchedTicker["id"],
			"name": matchedTicker["name"],
			"base": matchedTicker["id"],
			"quote": matchedTicker["quote"],
			"symbol": tickerId,
			"exchange": exchanges[matchedTicker["exchanges"][0]].to_dict()
		}

	else:
		for e in relevantExchanges:
			if tickerId in e.properties.symbols:
				matchedTicker = e.properties.markets[tickerId]
				return {
					"id": matchedTicker["id"],
					"name": matchedTicker["name"],
					"base": matchedTicker["id"],
					"quote": matchedTicker["quote"],
					"symbol": tickerId,
					"exchange": e.to_dict()
				}

			else:
				for symbol, market in e.properties.markets.items():
					if tickerId == market["id"]:
						return {
							"id": market["id"],
							"name": market["name"],
							"base": market["id"],
							"quote": market["quote"],
							"symbol": symbol,
							"exchange": e.to_dict()
						}

	return None

def find_serum_crypto_market(tickerId):
	if tickerId in serumIndex:
		for market in serumIndex[tickerId]:
			mcapRank = coinGeckoIndex[tickerId]["market_cap_rank"] if tickerId in coinGeckoIndex else MAXSIZE
			return {
				"id": market["id"],
				"name": coinGeckoIndex.get(tickerId, {}).get("name", tickerId + market["quote"]),
				"base": tickerId,
				"quote": market["quote"],
				"symbol": market["program"],
				"image": market.get("image"),
				"exchange": {},
				"mcapRank": mcapRank
			}
	
	else:
		for base in serumIndex:
			if tickerId.startswith(base):
				for market in serumIndex[base]:
					if tickerId == f"{base}{market['quote']}":
						mcapRank = coinGeckoIndex[base]["market_cap_rank"] if base in coinGeckoIndex else MAXSIZE
						return {
							"id": market["id"],
							"name": coinGeckoIndex.get(tickerId, {}).get("name", tickerId + market["quote"]),
							"base": tickerId,
							"quote": market["quote"],
							"symbol": market["program"],
							"image": market.get("image"),
							"mcapRank": mcapRank
						}

	return None

def find_tradable_markets(tickerId, exchangeId, platform):
	if exchangeId != "" and exchangeId not in supported.cryptoExchanges["Ichibot"]: return {}
	exchangeIds = supported.cryptoExchanges["Ichibot"] if exchangeId == "" else [exchangeId]

	matches = {}
	for e in exchangeIds:
		match = find_ccxt_crypto_market(tickerId, e, "Ichibot")
		check = find_ccxt_crypto_market(tickerId, exchangeId, platform)
		if match is not None and check is not None:
			matches[e] = exchanges[e].properties.markets[match.get("symbol")]["id"]
	return matches


# -------------------------
# Endpoints
# -------------------------

@app.post("/parser/match_ticker")
async def run(req: Request):
	request = await req.json()
	return match_ticker(request["tickerId"], request["exchangeId"], request["platform"], request["bias"])

@app.post("/parser/find_exchange")
async def run(req: Request):
	request = await req.json()
	return find_exchange(request["raw"], request["platform"], request["bias"])

@app.post("/parser/check_if_fiat")
async def check_if_fiat(req: Request):
	request = await req.json()
	tickerId = request["tickerId"]

	for fiat in coingeckoFiatCurrencies:
		if fiat.upper() in tickerId: return {"asset": fiat, "isFieat": True}
	return {"asset": None, "isFiat": False}

@app.post("/parser/get_listings")
async def get_listings(req: Request):
	request = await req.json()
	tickerBase, tickerQuote = request["tickerBase"], request["tickerQuote"]

	listings = {tickerQuote: []}
	total = 0
	for e in supported.cryptoExchanges["CCXT"]:
		if exchanges[e].properties is not None and exchanges[e].properties.symbols is not None:
			for symbol in exchanges[e].properties.symbols:
				base = exchanges[e].properties.markets[symbol]["base"]
				quote = exchanges[e].properties.markets[symbol]["quote"]
				if tickerBase == base:
					if quote not in listings: listings[quote] = []
					if exchanges[e].name not in listings[quote]:
						listings[quote].append(exchanges[e].name)
						total += 1

	response = [[tickerQuote, listings.pop(tickerQuote)]]
	if tickerBase in ccxtIndex["CCXT"]:
		for quote in ccxtIndex["CCXT"][tickerBase]:
			if quote in listings:
				response.append([quote, listings.pop(quote)])

	return {"response": response, "total": total}	

@app.post("/parser/get_formatted_price_ccxt")
async def format_price(req: Request):
	request = await req.json()
	exchange = exchanges[request["exchangeId"]].properties
	precision = exchange.markets.get(request["symbol"], {}).get("precision", {}).get("price", 8)
	text = dtp.decimal_to_precision(request["price"], rounding_mode=dtp.ROUND, precision=precision, counting_mode=exchange.precisionMode, padding_mode=dtp.PAD_WITH_ZERO)
	return {"response": text.rstrip("0").rstrip(".")}

@app.post("/parser/get_formatted_amount_ccxt")
async def format_amount(req: Request):
	request = await req.json()
	exchange = exchanges[request["exchangeId"]].properties
	precision = exchange.markets.get(request["symbol"], {}).get("precision", {}).get("amount", 8)
	text = dtp.decimal_to_precision(request["amount"], rounding_mode=dtp.TRUNCATE, precision=precision, counting_mode=exchange.precisionMode, padding_mode=dtp.NO_PADDING)
	return {"response": text.rstrip("0").rstrip(".")}

@app.post("/parser/get_venues")
async def get_venues(req: Request):
	request = await req.json()
	platforms = request["platforms"]

	venues = []
	if platforms == "":
		venues += ["CoinGecko", "Serum"]
		for ids in supported.traditionalExchanges.values():
			venues += [exchanges[e].name for e in ids]
	else:
		for platform in platforms.split(","):
			if platform == "CoinGecko":
				venues += ["CoinGecko"]
			elif platform == "Serums":
				venues += ["Serums"]
			else:
				venues += [exchanges[e].name for e in supported.traditionalExchanges.get(platform, [])]
	return {"response": venues}


# -------------------------
# Startup
# -------------------------

if __name__ == "__main__":
	refresh_coingecko_index()
	refresh_iexc_index()
	refresh_ccxt_index()
	refresh_serum_index()

	print("[Startup]: Ticker Parser is online")
	# config = Config(app=app, port=int(environ.get("PORT", 6900)), host="0.0.0.0", loop=loop)
	config = Config(app=app, port=6900, host="0.0.0.0", loop=loop)
	server = Server(config)
	loop.run_until_complete(server.serve())