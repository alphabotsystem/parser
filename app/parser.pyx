# cython: language_level=3, boundscheck=False, wraparound=False, cdivision=True, always_allow_keywords=False

import cython

from os import environ
from sys import maxsize as MAXSIZE
from signal import signal, SIGINT, SIGTERM
from time import sleep, perf_counter
from datetime import datetime
from pytz import utc
from zmq import Context, Poller, ROUTER, REQ, LINGER, POLLIN
from lark import Lark, Token, Transformer
from lark.reconstruct import Reconstructor
from orjson import dumps, loads
from traceback import format_exc
from threading import Thread

import ccxt
from ccxt.base import decimal_to_precision as dtp
from pycoingecko import CoinGeckoAPI
from google.cloud.error_reporting import Client as ErrorReportingClient

from TickerParser import Exchange

from assets import static_storage
from helpers.utils import Utils
from helpers import supported


GRAMMAR = """
	?start: sum
	?sum: product
		| sum "+" product   -> add
		| sum "-" product   -> sub
	?product: atom
		| product "*" atom  -> mul
		| product "/" atom  -> div
	?atom: NUMBER           -> number
		 | "-" atom         -> neg
		 | NAME             -> var
		 | NAME ":" NUMBER  -> var
		 | "'" NAME "'"     -> literal
		 | "\\"" NAME "\\"" -> literal
		 | "‘" NAME "’"     -> literal
		 | "“" NAME "”"     -> literal
		 | "(" sum ")"
	%import common.LETTER
	%import common.DIGIT
	%import common.NUMBER
	%import common.WS_INLINE
	%ignore WS_INLINE

	NAME: LETTER ("_"|":"|LETTER|DIGIT)*
"""

larkParser = Lark(GRAMMAR, parser='lalr')
Ticker = larkParser.parse
reconstructor = Reconstructor(larkParser)


TICKER_OVERRIDES = {
	"TradingView": [
		("SPX500USD", ["SPX", "SP500", "SPX500"]),
		("NFTY", ["NIFTY"])
	]
}


cdef class TickerParserServer(object):
	cdef object coinGecko, logging, context, jobQueue, socket
	cdef dict exchanges, ccxtIndex, serumIndex, coinGeckoIndex, iexcStocksIndex, iexcForexIndex
	cdef list coingeckoVsCurrencies, coingeckoFiatCurrencies
	cdef int isServiceAvailable

	def __init__(self):
		self.coinGecko = CoinGeckoAPI()

		self.exchanges = {}
		self.ccxtIndex = {}
		self.serumIndex = {}
		self.coinGeckoIndex = {}
		self.iexcStocksIndex = {}
		self.iexcForexIndex = {}

		self.coingeckoVsCurrencies = []
		self.coingeckoFiatCurrencies = []

		self.logging = ErrorReportingClient(service="parser")
		self.context = Context.instance()

		self.refresh_coingecko_index()
		cdef list processes = [
			Thread(target=lambda: self.refresh_coingecko_exchange_rates()),
			Thread(target=lambda: self.refresh_ccxt_index()),
			Thread(target=lambda: self.refresh_serum_index()),
			Thread(target=lambda: self.refresh_iexc_index())
		]
		for p in processes: p.start()
		for p in processes: p.join()

		self.jobQueue = Thread(target=self.job_queue)
		self.jobQueue.start()

		self.socket = self.context.socket(ROUTER)
		self.socket.bind("tcp://*:6900")

		self.isServiceAvailable = 1
		signal(SIGINT, self.exit_gracefully)
		signal(SIGTERM, self.exit_gracefully)

		print("[Startup]: Ticker Parser is online")

	cdef void exit_gracefully(self, int signum, object frame):
		print("[Startup]: Ticker Parser is exiting")
		self.socket.close()
		self.isServiceAvailable = 0

	cpdef void run(self):
		cdef list response, message, request
		while self.isServiceAvailable:
			try:
				response = []
				message = self.socket.recv_multipart()
				if len(message) < 4: continue
				origin, delimeter, service = message[:3]
				request = message[3:]

				if service == b"match_ticker":
					[tickerId, exchangeId, platform, bias] = request
					response = self.match_ticker(tickerId.decode(), exchangeId.decode(), platform.decode(), bias.decode())
				elif service == b"find_exchange":
					[raw, platform, bias] = request
					response = self.find_exchange(raw.decode(), platform.decode(), bias.decode())
				elif service == b"check_if_fiat":
					[tickerId] = request
					response = self.check_if_fiat(tickerId.decode())
				elif service == b"get_listings":
					[tickerBase, tickerQuote] = request
					response = self.get_listings(tickerBase.decode(), tickerQuote.decode())
				elif service == b"get_formatted_price_ccxt":
					[exchangeId, symbol, price] = request
					response = self.format_price(exchangeId.decode(), symbol.decode(), price.decode())
				elif service == b"get_formatted_amount_ccxt":
					[exchangeId, symbol, amount] = request
					response = self.format_amount(exchangeId.decode(), symbol.decode(), amount.decode())
				elif service == b"get_venues":
					[platforms, tickerId] = request
					response = self.get_venues(platforms.decode(), tickerId.decode())

			except (KeyboardInterrupt, SystemExit): return
			except Exception:
				print(format_exc())
				if environ["PRODUCTION_MODE"]: self.logging.report_exception(user=f"{request}")
			finally:
				try: self.socket.send_multipart([origin, delimeter] + response)
				except: pass

	cpdef void job_queue(self):
		cdef object t
		cdef list timeframes
		while True:
			try:
				sleep(Utils.seconds_until_cycle())
				t = datetime.now().astimezone(utc)
				timeframes = Utils.get_accepted_timeframes(t)

				if "1H" in timeframes:
					self.refresh_ccxt_index()
					self.refresh_coingecko_index()
					self.refresh_serum_index()
					self.refresh_coingecko_exchange_rates()
				if "1D" in timeframes:
					self.refresh_iexc_index()

			except Exception:
				print(format_exc())
				if environ["PRODUCTION_MODE"]: self.logging.report_exception()

	cdef void refresh_ccxt_index(self):
		cdef set difference = set(ccxt.exchanges).symmetric_difference(supported.ccxtExchanges)
		cdef list newExchanges = []
		cdef list newSupportedExchanges = []
		cdef list unsupportedCryptoExchanges = []
		cdef object ex
		cdef str e
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

		cdef set completedTasks = set()
		cdef dict sortedIndexReference = {}
		cdef str platform, exchange, symbol, base, quote

		for platform in supported.cryptoExchanges:
			if platform not in sortedIndexReference: sortedIndexReference[platform] = {}
			for exchange in supported.cryptoExchanges[platform]:
				if exchange not in completedTasks:
					if exchange not in self.exchanges: self.exchanges[exchange] = Exchange(exchange, "crypto" if exchange in ccxt.exchanges else "traditional")
					try: self.exchanges[exchange].properties.load_markets()
					except: continue
					completedTasks.add(exchange)

				for symbol in self.exchanges[exchange].properties.symbols:
					if '.' not in symbol and Utils.is_active(symbol, self.exchanges[exchange]):
						base = self.exchanges[exchange].properties.markets[symbol].get("base")
						quote = self.exchanges[exchange].properties.markets[symbol].get("quote")

						if base not in sortedIndexReference[platform]:
							sortedIndexReference[platform][base] = {}
						if quote not in sortedIndexReference[platform][base]:
							sortedIndexReference[platform][base][quote] = self.coinGeckoIndex.get(quote, {}).get("market_cap_rank", MAXSIZE)

		for platform in sortedIndexReference:
			self.ccxtIndex[platform] = {}
			for base in sortedIndexReference[platform]:
				if base not in self.ccxtIndex[platform]: self.ccxtIndex[platform][base] = []
				self.ccxtIndex[platform][base] = sorted(sortedIndexReference[platform][base].keys(), key=lambda quote: sortedIndexReference[platform][base][quote])
				try: self.ccxtIndex[platform][base].insert(0, self.ccxtIndex[platform][base].pop(self.ccxtIndex[platform][base].index("USDT")))
				except: pass
				try: self.ccxtIndex[platform][base].insert(0, self.ccxtIndex[platform][base].pop(self.ccxtIndex[platform][base].index("USD")))
				except: pass

	cdef void refresh_serum_index(self):
		cdef dict rawData, market, token, usdcMarket
		cdef object socket, poller
		cdef list responses, processed
		cdef str base, quote, symbol
		try:
			for i in range(3):
				socket = self.context.socket(REQ)
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
				if base not in self.serumIndex:
					self.serumIndex[base] = []
				self.serumIndex[base].append({"id": market["address"], "name": base, "base": base, "quote": quote, "image": None, "program": market["programId"]})

			for token in rawData["tokenList"]:
				symbol = token["symbol"].upper()
				if symbol not in self.serumIndex:
					self.serumIndex[symbol] = []
				processed = []
				for market in self.serumIndex[symbol]:
					processed.append(market["quote"])
					market["name"] = token["name"]
					market["image"] = token.get("logoURI")
				for extension, address in token.get("extensions", {}).items():
					if extension.startswith("serumV3"):
						quote = extension.removeprefix("serumV3").upper()
						if quote not in processed:
							processed.append(quote)
							self.serumIndex[symbol].append({"id": address, "name": token["name"], "base": symbol, "quote": quote, "image": token.get("logoURI"), "program": "9xQeWvG816bUx9EPjHmaT23yvVM2ZWbrrpZb9PusVFin"})
				if len(self.serumIndex[symbol]) == 0:
					self.serumIndex.pop(symbol)
				elif self.serumIndex[symbol][0]["quote"] != "USDC":
					usdcMarket = {}
					for index, market in enumerate(self.serumIndex[symbol]):
						if market["quote"] == "USDC":
							usdcMarket = self.serumIndex[symbol].pop(index)
							break
					if usdcMarket:
						self.serumIndex[symbol].insert(0, usdcMarket)

		except Exception:
			print(format_exc())

	cdef void refresh_coingecko_index(self):
		cdef list blacklist = ["UNIUSD", "AAPL", "TSLA", "ETHUSDADL4"]
		cdef list rawData = []
		cdef dict indexReference = {}
		cdef int page = 1
		cdef list response
		cdef str symbol, adjustedSymbol
		try:
			while True:
				try:
					response = self.coinGecko.get_coins_markets(vs_currency="usd", order="id_asc", per_page=250, page=page)
					sleep(0.6)
				except:
					print(format_exc())
					sleep(10)
					continue

				if len(response) == 0: break
				rawData += response
				page += 1

			rawData.sort(reverse=True, key=lambda k: (float('-inf') if k["market_cap_rank"] is None else -k["market_cap_rank"], 0 if k["total_volume"] is None else k["total_volume"], k["name"], k["id"]))
			for e in rawData:
				symbol = e["symbol"].upper()
				if symbol in blacklist: continue
				if symbol not in indexReference:
					indexReference[symbol] = {
						"id": e["id"],
						"name": e["name"],
						"base": symbol,
						"quote": "USD",
						"image": e["image"],
						"market_cap_rank": MAXSIZE if e["market_cap_rank"] is None else e["market_cap_rank"]
					}
				elif indexReference[symbol]["id"] != e["id"]:
					for i in range(2, 11):
						adjustedSymbol = "{}:{}".format(symbol, i)
						if adjustedSymbol not in indexReference:
							indexReference[adjustedSymbol] = {
								"id": e["id"],
								"name": e["name"],
								"base": symbol,
								"quote": "USD",
								"image": e["image"],
								"market_cap_rank": MAXSIZE if e["market_cap_rank"] is None else e["market_cap_rank"]
							}
							break
			self.coinGeckoIndex = indexReference

		except Exception:
			print(format_exc())

	cdef void refresh_coingecko_exchange_rates(self):
		try:
			self.coingeckoVsCurrencies = [e.upper() for e in self.coinGecko.get_supported_vs_currencies()]
			for ticker, value in self.coinGecko.get_exchange_rates()["rates"].items():
				if value["type"] == "fiat":
					self.coingeckoFiatCurrencies.append(ticker.upper())
		except Exception:
			print(format_exc())

	cdef void refresh_iexc_index(self):
		cdef set iexcExchanges = set()
		cdef list exchanges = Utils.get_url("https://cloud.iexapis.com/stable/ref-data/market/us/exchanges?token={}".format(environ['IEXC_KEY']))
		cdef dict suffixMap = {}

		cdef dict exchange
		cdef str exchangeId
		for exchange in exchanges:
			if exchange["mic"] == "": continue
			exchangeId = exchange["mic"]
			iexcExchanges.add(exchangeId.lower())
			self.exchanges[exchangeId.lower()] = Exchange(exchangeId, "traditional", exchange["longName"], region="us")
		exchanges = Utils.get_url("https://cloud.iexapis.com/stable/ref-data/exchanges?token={}".format(environ['IEXC_KEY']))
		for exchange in exchanges:
			exchangeId = exchange["mic"]
			if exchangeId.lower() in iexcExchanges: continue
			iexcExchanges.add(exchangeId.lower())
			self.exchanges[exchangeId.lower()] = Exchange(exchangeId, "traditional", exchange["description"], region=exchange["region"])
			suffixMap[exchangeId.lower()] = exchange["exchangeSuffix"]

		cdef set difference = set(iexcExchanges).symmetric_difference(supported.iexcExchanges)
		cdef list newSupportedExchanges = []
		cdef list unsupportedCryptoExchanges = []
		for exchangeId in difference:
			if exchangeId not in supported.iexcExchanges:
				newSupportedExchanges.append(exchangeId)
			else:
				unsupportedCryptoExchanges.append(exchangeId)
		if len(newSupportedExchanges) != 0: print(f"New supported IEXC exchanges: {newSupportedExchanges}")
		if len(unsupportedCryptoExchanges) != 0: print(f"New deprecated IEXC exchanges: {unsupportedCryptoExchanges}")

		for exchangeId in supported.traditionalExchanges["IEXC"]:
			symbols = Utils.get_url("https://cloud.iexapis.com/stable/ref-data/exchange/{}/symbols?token={}".format(self.exchanges[exchangeId].id, environ['IEXC_KEY']))
			if len(symbols) == 0: print(f"No symbols found on {exchangeId}")
			for symbol in symbols:
				suffix = suffixMap.get(exchangeId, "")
				tickerId = symbol["symbol"]
				if tickerId not in self.iexcStocksIndex:
					self.iexcStocksIndex[tickerId] = {"id": tickerId.removesuffix(suffix), "name": symbol["name"], "base": tickerId.removesuffix(suffix), "quote": symbol["currency"]}
				self.exchanges[exchangeId].properties.symbols.append(tickerId)

		cdef dict forexSymbols = Utils.get_url("https://cloud.iexapis.com/stable/ref-data/fx/symbols?token={}".format(environ['IEXC_KEY']))
		cdef set derivedCurrencies = set()
		cdef dict pair
		for pair in forexSymbols["pairs"]:
			derivedCurrencies.add(pair["fromCurrency"])
			derivedCurrencies.add(pair["toCurrency"])
			self.iexcForexIndex[pair["symbol"]] = {"id": pair["symbol"], "name": pair["symbol"], "base": pair["fromCurrency"], "quote": pair["toCurrency"], "reversed": False}
			self.iexcForexIndex[pair["toCurrency"] + pair["fromCurrency"]] = {"id": pair["symbol"], "name": pair["toCurrency"] + pair["fromCurrency"], "base": pair["toCurrency"], "quote": pair["fromCurrency"], "reversed": True}
		cdef str fromCurrency, toCurrency
		for fromCurrency in derivedCurrencies:
			for toCurrency in derivedCurrencies:
				symbol = fromCurrency + toCurrency
				if fromCurrency != toCurrency and symbol not in self.iexcForexIndex:
					self.iexcForexIndex[symbol] = {"id": symbol, "name": symbol, "base": fromCurrency, "quote": toCurrency, "reversed": False}

	cdef list find_exchange(self, str raw, str platform, str bias):
		if platform not in supported.cryptoExchanges and platform not in supported.traditionalExchanges: return [b"0", b""]
		if raw in ["pro"]: return [b"0", b""]

		cdef dict shortcuts = {
			"crypto": {
				"binance": ["bin", "bi", "b"],
				"bitmex": ["bmx", "mex", "btmx", "bx"],
				"binanceusdm": ["binancefutures", "binancef", "fbin", "binf", "bif", "bf", "bnf"],
				"coinbasepro": ["cbp", "coin", "base", "cb", "coinbase", "coinbasepro", "cbpro"],
				"bitfinex2": ["bfx", "finex", "bf"],
				"bittrex": ["btrx", "brx"],
				"poloniex": ["po", "polo"],
				"kraken": ["k", "kra"],
				"gemini": ["ge", "gem"]
			},
			"traditional": {}
		}

		if platform in ["TradingLite", "Bookmap", "GoCharting", "LLD", "CoinGecko", "CCXT", "Serum", "Ichibot"]:
			bias = "crypto"
		elif platform in ["IEXC"]:
			bias = "traditional"

		cdef str name, nameNoSpaces, exchangeId
		if bias == "crypto":
			for exchangeId in supported.cryptoExchanges[platform]:
				if exchangeId in shortcuts["crypto"] and raw in shortcuts["crypto"][exchangeId]:
					return [b"1", dumps(self.exchanges[exchangeId].to_dict())]
				if exchangeId in self.exchanges and self.exchanges[exchangeId].name is not None:
					name = self.exchanges[exchangeId].name.split(" ")[0].lower()
					nameNoSpaces = self.exchanges[exchangeId].name.replace(" ", "").replace(".", "").lower()
				else:
					name, nameNoSpaces = exchangeId, exchangeId

				if len(name) * 0.33 > len(raw): continue

				if name.startswith(raw) or name.endswith(raw):
					return [b"1", dumps(self.exchanges[exchangeId].to_dict())]
				elif nameNoSpaces.startswith(raw) or nameNoSpaces.endswith(raw):
					return [b"1", dumps(self.exchanges[exchangeId].to_dict())]
				elif exchangeId.startswith(raw) or exchangeId.endswith(raw):
					return [b"1", dumps(self.exchanges[exchangeId].to_dict())]

			for platform in supported.cryptoExchanges:
				for exchangeId in supported.cryptoExchanges[platform]:
					if exchangeId in shortcuts["crypto"] and raw in shortcuts["crypto"][exchangeId]:
						return [b"0", dumps(self.exchanges[exchangeId].to_dict())]
					if exchangeId in self.exchanges and self.exchanges[exchangeId].name is not None:
						name = self.exchanges[exchangeId].name.split(" ")[0].lower()
						nameNoSpaces = self.exchanges[exchangeId].name.replace(" ", "").replace(".", "").lower()
					else:
						name, nameNoSpaces = exchangeId, exchangeId

					if name.startswith(raw) or name.endswith(raw):
						return [b"0", dumps(self.exchanges[exchangeId].to_dict())]
					elif nameNoSpaces.startswith(raw) or nameNoSpaces.endswith(raw):
						return [b"0", dumps(self.exchanges[exchangeId].to_dict())]
					elif exchangeId.startswith(raw) or exchangeId.endswith(raw):
						return [b"0", dumps(self.exchanges[exchangeId].to_dict())]

		else:
			for exchangeId in supported.traditionalExchanges[platform]:
				if exchangeId in shortcuts["traditional"] and raw in shortcuts["traditional"][exchangeId]:
					return [b"1", dumps(self.exchanges[exchangeId].to_dict())]
				if exchangeId in self.exchanges and self.exchanges[exchangeId].name is not None:
					name = self.exchanges[exchangeId].name.split(" ")[0].lower()
					nameNoSpaces = self.exchanges[exchangeId].name.replace(" ", "").replace(".", "").lower()
				else:
					name, nameNoSpaces = exchangeId, exchangeId

				if len(name) * 0.33 > len(raw): continue

				if name.startswith(raw) or name.endswith(raw):
					return [b"1", dumps(self.exchanges[exchangeId].to_dict())]
				elif nameNoSpaces.startswith(raw) or nameNoSpaces.endswith(raw):
					return [b"1", dumps(self.exchanges[exchangeId].to_dict())]
				elif exchangeId.startswith(raw) or exchangeId.endswith(raw):
					return [b"1", dumps(self.exchanges[exchangeId].to_dict())]

			for platform in supported.traditionalExchanges:
				for exchangeId in supported.traditionalExchanges[platform]:
					if exchangeId in shortcuts["traditional"] and raw in shortcuts["traditional"][exchangeId]:
						return [b"0", dumps(self.exchanges[exchangeId].to_dict())]
					if exchangeId in self.exchanges and self.exchanges[exchangeId].name is not None:
						name = self.exchanges[exchangeId].name.split(" ")[0].lower()
						nameNoSpaces = self.exchanges[exchangeId].name.replace(" ", "").replace(".", "").lower()
					else:
						name, nameNoSpaces = exchangeId, exchangeId

					if name.startswith(raw) or name.endswith(raw):
						return [b"0", dumps(self.exchanges[exchangeId].to_dict())]
					elif nameNoSpaces.startswith(raw) or nameNoSpaces.endswith(raw):
						return [b"0", dumps(self.exchanges[exchangeId].to_dict())]
					elif exchangeId.startswith(raw) or exchangeId.endswith(raw):
						return [b"0", dumps(self.exchanges[exchangeId].to_dict())]

		return [b"0", b""]

	cdef list match_ticker(self, str tickerId, str exchangeId, str platform, str bias):
		if platform in ["TradingLite", "Bookmap", "LLD", "CoinGecko", "CCXT", "Serum", "Ichibot"]: bias = "crypto"
		elif platform in ["IEXC"]: bias = "traditional"

		cdef dict exchange = {} if exchangeId == "" else self.exchanges.get(exchangeId).to_dict()

		cdef object ticker
		try:
			ticker = Ticker(tickerId)
		except:
			return [dumps({
				"tree": [
					"var",
					[[
						"NAME",
						{
							"id": "BTC",
							"name": "BTC",
							"base": None,
							"quote": None,
							"symbol": None,
							"exchange": exchange,
							"mcapRank": MAXSIZE
						}
					]]
				],
				"id": tickerId,
				"name": tickerId,
				"exchange": exchange,
				"base": None,
				"quote": None,
				"symbol": None,
				"mcapRank": MAXSIZE,
				"isSimple": True
			}), b""]

		self.ticker_tree_search(ticker, exchangeId, platform, bias, shouldMatch=1)

		cdef int isSimple = isinstance(ticker.children[0], Token) and ticker.children[0].type == "NAME"
		cdef dict simpleTicker = ticker.children[0].value if isSimple else {}
		if not isSimple and platform not in ["TradingView", "Alternative.me", "CoinGecko", "CCXT", "Serum", "IEXC", "LLD"]:
			return [b"", f"Aggregated tickers aren't available on {platform}".encode()]

		cdef str reconstructedId = reconstructor.reconstruct(self.ticker_tree_search(Ticker(tickerId), exchangeId, platform, bias))

		response = {
			"tree": TickerTree().transform(ticker),
			"id": reconstructedId,
			"name": simpleTicker.get("name", reconstructedId),
			"exchange": simpleTicker.get("exchange", {}),
			"base": simpleTicker.get("base", None),
			"quote": simpleTicker.get("quote", None),
			"symbol": simpleTicker.get("symbol", None),
			"image": simpleTicker.get("image", static_storage.icon),
			"mcapRank": simpleTicker.get("mcapRank", MAXSIZE),
			"isSimple": bool(isSimple)
		}
		if isSimple and bias == "crypto": response["tradable"] = self.find_tradable_markets(reconstructedId, exchangeId, platform)

		return [dumps(response), b""]

	cdef object ticker_tree_search(self, object node, str exchangeId, str platform, str bias, int shouldMatch=0):
		cdef int i
		cdef object child, newValue
		for i, child in enumerate(node.children):
			if not isinstance(child, Token):
				node.children[i] = self.ticker_tree_search(child, exchangeId, platform, bias, shouldMatch)
			elif child.type == "NAME":
				newValue = self.internal_match(child.value, exchangeId, platform, bias)
				if not shouldMatch: newValue = newValue["id"]
				node.children[i] = child.update(value=newValue)
		return node

	cdef dict internal_match(self, str tickerId, str exchangeId, str platform, str bias):
		cdef dict _ticker
		if tickerId.startswith("$"): tickerId = tickerId[1:] + "USD"
		elif tickerId.startswith("€"): tickerId = tickerId[1:] + "EUR"
		tickerId, _ticker = self._check_overrides(tickerId, platform), None
		if bias == "crypto":
			if platform in ["CoinGecko"] and exchangeId == "": _ticker = self.find_coingecko_crypto_market(tickerId)
			elif platform in ["Serum"] and exchangeId == "": _ticker = self.find_serum_crypto_market(tickerId)
			else: _ticker = self.find_ccxt_crypto_market(tickerId, exchangeId, platform)
		else:
			if platform in ["IEXC"]: _ticker = self.find_iexc_market(tickerId, exchangeId, platform)
		if not _ticker:
			_ticker = {
				"id": tickerId,
				"name": tickerId,
				"base": None,
				"quote": None,
				"symbol": None,
				"exchange": {} if exchangeId == "" else self.exchanges.get(exchangeId).to_dict(),
				"mcapRank": MAXSIZE
			}
		return _ticker

	cdef dict find_ccxt_crypto_market(self, str tickerId, str exchangeId, str platform):
		cdef object exchange = None if exchangeId == "" else self.exchanges[exchangeId]
		if platform not in supported.cryptoExchanges or (exchange is not None and exchange.type != "crypto"): return None
		cdef list exchanges = [self.exchanges[e] for e in supported.cryptoExchanges[platform] if self.exchanges[e].type == "crypto"] if exchange is None else [exchange]

		cdef object e
		cdef str symbol, base, quote, marketId
		cdef long currentBestMatch, currentBestFit, mcapRank
		cdef dict currentResult
		cdef list marketPair
		for e in exchanges:
			if e.properties is not None and e.properties.symbols is not None:
				if tickerId in self.ccxtIndex[platform]:
					for quote in self.ccxtIndex[platform][tickerId]:
						symbol = tickerId + "/" + quote
						if symbol in e.properties.symbols:
							if exchange is None and platform not in ["Ichibot"] and self._is_tokenized_stock(e, symbol): continue
							base = e.properties.markets[symbol].get("base")
							quote = e.properties.markets[symbol].get("quote")
							if not base in self.coingeckoFiatCurrencies and Utils.is_active(symbol, e):
								marketId = Utils.generate_market_id(symbol, e)
								return {
									"id": marketId,
									"name": self.coinGeckoIndex.get(tickerId, {}).get("name", marketId),
									"base": tickerId,
									"quote": quote,
									"symbol": symbol,
									"image": self.coinGeckoIndex.get(tickerId, {}).get("image", static_storage.icon),
									"exchange": e.to_dict(),
									"mcapRank": self.coinGeckoIndex.get(tickerId, {}).get("market_cap_rank", MAXSIZE)
								}

				else:
					currentBestMatch = MAXSIZE
					currentBestFit = MAXSIZE
					currentResult = {}
					for symbol in e.properties.symbols:
						if exchange is None and platform not in ["Ichibot"] and self._is_tokenized_stock(e, symbol): continue
						base = e.properties.markets[symbol].get("base")
						quote = e.properties.markets[symbol].get("quote")
						marketPair = symbol.split("/")
						marketId = Utils.generate_market_id(symbol, e)
						mcapRank = self.coinGeckoIndex.get(base, {}).get("market_cap_rank", MAXSIZE)
						if Utils.is_active(symbol, e):
							if len(marketPair) == 1:
								if (tickerId == base or (marketId.startswith(tickerId) and len(marketId) * 0.5 <= len(tickerId))) and currentBestFit > 2:
									currentBestFit = 2
									currentResult = {
										"id": marketId,
										"name": self.coinGeckoIndex.get(base, {}).get("name", marketId),
										"base": base,
										"quote": quote,
										"symbol": symbol,
										"image": self.coinGeckoIndex.get(base, {}).get("image", static_storage.icon),
										"exchange": e.to_dict(),
										"mcapRank": mcapRank
									}

							elif base in self.ccxtIndex[platform] and quote in self.ccxtIndex[platform][base]:
								rankScore = self.ccxtIndex[platform][base].index(quote)
								if (tickerId == base + quote or (marketId.startswith(tickerId) and len(marketId) * 0.5 <= len(tickerId))) and currentBestFit >= 1 and base not in self.coingeckoFiatCurrencies and rankScore < currentBestMatch:
									currentBestMatch = rankScore
									currentBestFit = 1
									currentResult = {
										"id": marketId,
										"name": self.coinGeckoIndex.get(base, {}).get("name", marketId),
										"base": base,
										"quote": quote,
										"symbol": symbol,
										"image": self.coinGeckoIndex.get(base, {}).get("image", static_storage.icon),
										"exchange": e.to_dict(),
										"mcapRank": mcapRank
									}

					if currentResult: return currentResult

		return {}

	cdef dict find_coingecko_crypto_market(self, str tickerId):
		cdef list split = tickerId.split(":")
		cdef str _tickerId, rank
		if len(split) == 2:
			_tickerId, rank = split[0], "" if split[1] == "1" else ":" + split[1]
		elif len(split) == 3:
			_tickerId, rank = split[0] + split[2], "" if split[1] == "1" else ":" + split[1]
		else:
			_tickerId, rank = tickerId, ""

		cdef str base, quote
		if tickerId in self.coinGeckoIndex:
			return {
				"id": f"{_tickerId}USD",
				"name": self.coinGeckoIndex[tickerId]["name"],
				"base": tickerId,
				"quote": "USD",
				"symbol": self.coinGeckoIndex[tickerId]["id"],
				"image": self.coinGeckoIndex[tickerId].get("image"),
				"exchange": {},
				"mcapRank": self.coinGeckoIndex[tickerId]["market_cap_rank"]
			}

		else:
			for base in self.coinGeckoIndex:
				if tickerId.startswith(base) and base + rank in self.coinGeckoIndex:
					for quote in self.coingeckoVsCurrencies:
						if _tickerId == f"{base}{quote}":
							return {
								"id": _tickerId,
								"name": self.coinGeckoIndex[base + rank]["name"],
								"base": base + rank,
								"quote": quote,
								"symbol": self.coinGeckoIndex[base + rank]["id"],
								"image": self.coinGeckoIndex[base + rank].get("image"),
								"exchange": {},
								"mcapRank": self.coinGeckoIndex[base + rank]["market_cap_rank"]
							}

			for base in self.coinGeckoIndex:
				if base.startswith(_tickerId) and base + rank in self.coinGeckoIndex:
					return {
						"id": f"{base}USD",
						"name": self.coinGeckoIndex[base + rank]["name"],
						"base": base + rank,
						"quote": "USD",
						"symbol": self.coinGeckoIndex[base + rank]["id"],
						"image": self.coinGeckoIndex[base + rank].get("image"),
						"exchange": {},
						"mcapRank": self.coinGeckoIndex[base + rank]["market_cap_rank"]
					}

		return {}

	cdef dict find_iexc_market(self, str tickerId, str exchangeId, str platform):
		cdef object exchange = None if exchangeId == "" else self.exchanges[exchangeId]
		if platform not in supported.traditionalExchanges or (exchange is not None and exchange.type != "traditional"): return None
		cdef list exchanges = [self.exchanges[e] for e in supported.traditionalExchanges[platform] if self.exchanges[e].type == "traditional"] if exchange is None else [exchange]

		cdef object e
		cdef dict matchedTicker
		cdef str symbol
		if tickerId in self.iexcForexIndex and exchange is None:
			matchedTicker = self.iexcForexIndex[tickerId]
			return {
				"id": matchedTicker["id"],
				"name": matchedTicker["name"],
				"base": matchedTicker["base"],
				"quote": matchedTicker["quote"],
				"symbol": f"{matchedTicker['base']}/{matchedTicker['quote']}",
				"exchange": {}
			}

		else:
			for e in exchanges:
				if tickerId in e.properties.symbols:
					matchedTicker = self.iexcStocksIndex[tickerId]
					return {
						"id": matchedTicker["id"],
						"name": matchedTicker["name"],
						"base": matchedTicker["base"],
						"quote": matchedTicker["quote"],
						"symbol": tickerId,
						"exchange": e.to_dict()
					}

				else:
					for symbol in e.properties.symbols:
						if tickerId == self.iexcStocksIndex.get(symbol, {}).get("id"):
							matchedTicker = self.iexcStocksIndex[symbol]
							return {
								"id": matchedTicker["id"],
								"name": matchedTicker["name"],
								"base": matchedTicker["base"],
								"quote": matchedTicker["quote"],
								"symbol": symbol,
								"exchange": e.to_dict()
							}

		return {}

	cdef dict find_serum_crypto_market(self, str tickerId):
		cdef long mcapRank
		cdef dict market
		cdef str base
		if tickerId in self.serumIndex:
			for market in self.serumIndex[tickerId]:
				mcapRank = self.coinGeckoIndex[tickerId]["market_cap_rank"] if tickerId in self.coinGeckoIndex else MAXSIZE
				return {
					"id": market["id"],
					"name": self.coinGeckoIndex.get(tickerId, {}).get("name", tickerId + market["quote"]),
					"base": tickerId,
					"quote": market["quote"],
					"symbol": market["program"],
					"image": market.get("image"),
					"exchange": {},
					"mcapRank": mcapRank
				}
		
		else:
			for base in self.serumIndex:
				if tickerId.startswith(base):
					for market in self.serumIndex[base]:
						if tickerId == f"{base}{market['quote']}":
							mcapRank = self.coinGeckoIndex[base]["market_cap_rank"] if base in self.coinGeckoIndex else MAXSIZE
							return {
								"id": market["id"],
								"name": self.coinGeckoIndex.get(tickerId, {}).get("name", tickerId + market["quote"]),
								"base": tickerId,
								"quote": market["quote"],
								"symbol": market["program"],
								"image": market.get("image"),
								"mcapRank": mcapRank
							}

			for base in self.serumIndex:
				if base.startswith(tickerId):
					market = self.serumIndex[base][0]
					mcapRank = self.coinGeckoIndex[base]["market_cap_rank"] if base in self.coinGeckoIndex else MAXSIZE
					return {
						"id": market["id"],
						"name": self.coinGeckoIndex.get(tickerId, {}).get("name", tickerId + market["quote"]),
						"base": tickerId,
						"quote": market["quote"],
						"symbol": market["program"],
						"image": market.get("image"),
						"exchange": {},
						"mcapRank": mcapRank
					}

		return {}

	cdef list check_if_fiat(self, str tickerId):
		cdef str fiat
		for fiat in self.coingeckoFiatCurrencies:
			if fiat.upper() in tickerId: return [b"1", fiat.encode()]
		return [b"0", b""]

	cdef list get_listings(self, str tickerBase, str tickerQuote):
		cdef dict listings = {tickerQuote: []}
		cdef int total = 0
		cdef str e, symbol, base, quote
		for e in supported.cryptoExchanges["CCXT"]:
			if self.exchanges[e].properties is not None and self.exchanges[e].properties.symbols is not None:
				for symbol in self.exchanges[e].properties.symbols:
					base = self.exchanges[e].properties.markets[symbol]["base"]
					quote = self.exchanges[e].properties.markets[symbol]["quote"]
					if tickerBase == base:
						if quote not in listings: listings[quote] = []
						if self.exchanges[e].name not in listings[quote]:
							listings[quote].append(self.exchanges[e].name)
							total += 1

		cdef list response = [[tickerQuote, listings.pop(tickerQuote)]]
		if tickerBase in self.ccxtIndex["CCXT"]:
			for quote in self.ccxtIndex["CCXT"][tickerBase]:
				if quote in listings:
					response.append([quote, listings.pop(quote)])

		return [dumps(response), str(total).encode()]

	cdef list format_price(self, str exchangeId, str symbol, str price):
		cdef object exchange = self.exchanges[exchangeId].properties
		cdef int precision = exchange.markets.get(symbol, {}).get("precision", {}).get("price", 8)
		return [dtp.decimal_to_precision(price, rounding_mode=dtp.ROUND, precision=precision, counting_mode=exchange.precisionMode, padding_mode=dtp.PAD_WITH_ZERO).encode()]

	cdef list format_amount(self, str exchangeId, str symbol, str amount):
		cdef object exchange = self.exchanges[exchangeId].properties
		cdef int precision = exchange.markets.get(symbol, {}).get("precision", {}).get("amount", 8)
		return [dtp.decimal_to_precision(amount, rounding_mode=dtp.TRUNCATE, precision=precision, counting_mode=exchange.precisionMode, padding_mode=dtp.NO_PADDING).encode()]

	cdef dict find_tradable_markets(self, str tickerId, str exchangeId, str platform):
		if exchangeId != "" and exchangeId not in supported.cryptoExchanges["Ichibot"]: return {}
		cdef list exchangeIds = supported.cryptoExchanges["Ichibot"] if exchangeId == "" else [exchangeId]

		cdef dict matches = {}
		cdef str e
		cdef dict match, check
		for e in exchangeIds:
			match = self.find_ccxt_crypto_market(tickerId, e, "Ichibot")
			check = self.find_ccxt_crypto_market(tickerId, exchangeId, platform)
			if match and check:
				matches[e] = self.exchanges[e].properties.markets[match.get("symbol")]["id"]
		return matches

	cdef list get_venues(self, str platforms, str tickerId):
		cdef list venues = []

		# self.find_coingecko_crypto_market(tickerId)
		# self.find_iexc_market(tickerId, "", "IEXC")
 
		cdef str platform
		if platforms == "":
			venues += ["CoinGecko", "Serum"]
			for ids in supported.traditionalExchanges.values():
				venues += [self.exchanges[e].name for e in ids]
		else:
			for platform in platforms.split(","):
				if platform == "CoinGecko":
					venues += ["CoinGecko"]
				elif platform == "Serums":
					venues += ["Serums"]
				else:
					venues += [self.exchanges[e].name for e in supported.traditionalExchanges.get(platform, [])]
		return [dumps(venues)]

	cdef str _check_overrides(self, str tickerId, str platform):
		cdef str tickerOverride
		cdef list triggers
		for tickerOverride, triggers in TICKER_OVERRIDES.get(platform, []):
			if tickerId in triggers:
				tickerId = tickerOverride
				return tickerId
		return tickerId

	cdef int _is_tokenized_stock(self, object e, str symbol):
		cdef int ftxTokenizedStock = e.id == "ftx" and e.properties.markets[symbol]["info"].get("tokenizedEquity", False)
		cdef int bittrexTokenizedStock = e.id == "bittrex" and "TOKENIZED_SECURITY" in e.properties.markets[symbol]["info"].get("tags", [])
		return ftxTokenizedStock or bittrexTokenizedStock


class TickerTree(Transformer):
	def add(self, list tree): return self.genenrate_list(tree, "add")
	def sub(self, list tree): return self.genenrate_list(tree, "sub")
	def mul(self, list tree): return self.genenrate_list(tree, "mul")
	def div(self, list tree): return self.genenrate_list(tree, "div")
	def neg(self, list tree): return self.genenrate_list(tree, "neg")
	def var(self, list tree): return self.genenrate_list(tree, "var")
	def number(self, list tree): return self.genenrate_list(tree, "number")
	def name(self, list tree): return self.genenrate_list(tree, "name")
	def literal(self, list tree): return self.genenrate_list(tree, "literal")

	def genenrate_list(self, list tree, str method):
		cdef list l = [method, []]
		cdef object child
		for child in tree:
			if not isinstance(child, Token): l[1].append(child)
			else: l[1].append([child.type, child.value])
		return l