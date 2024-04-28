from sys import maxsize as MAXSIZE
from time import time
from traceback import format_exc

from matching.exchanges import find_exchange
from matching.instruments import match_ticker
from .parameter import PriceParameter as Parameter
from .abstract import AbstractRequestHandler, AbstractRequest


PARAMETERS = {
	"preferences": [
		Parameter("suffix", "funding", ["fun", "fund", "funding"], ccxt=".FUNDING"),
		Parameter("suffix", "open interest", ["oi", "openinterest", "ov", "openvalue"], ccxt=".OI"),
		Parameter("suffix", "longs/shorts ratio", ["ls", "l/s", "longs/shorts", "long/short"], ccxt=".LS"),
		Parameter("suffix", "shorts/longs ratio", ["sl", "s/l", "shorts/longs", "short/long"], ccxt=".SL"),
		Parameter("suffix", "dominance", ["dom", "dominance"], coingecko=".D"),
		Parameter("suffix", "halving", ["halving", "halfing", "halv", "half"], blockchair="HALVING:"),
		Parameter("forcePlatform", "request quote on CoinGecko", ["cg", "coingecko"], coingecko=True),
		Parameter("forcePlatform", "request quote on a crypto exchange", ["cx", "ccxt", "crypto", "exchange"], ccxt=True),
		Parameter("forcePlatform", "request quote on a stock exchange", ["equities", "equity", "forex", "fx", "metal", "metals", "stock", "stocks", "index"], twelvedata=True),
		Parameter("forcePlatform", "request quote on Alternative.me", ["am", "alternativeme"], alternativeme=True),
		Parameter("forcePlatform", "request quote on CNN Business", ["cnn", "cnnbusiness"], cnnbusiness=True),
		Parameter("forcePlatform", "request quote on CNN Business", ["block", "blockchair", "blockchain"], cnnbusiness=True),
	]
}
DEFAULTS = {
	"Alternative.me": {
		"preferences": []
	},
	"CNN Business": {
		"preferences": []
	},
	"Blockchair": {
		"preferences": []
	},
	"CoinGecko": {
		"preferences": []
	},
	"CCXT": {
		"preferences": []
	},
	"Twelvedata": {
		"preferences": []
	}
}


class PriceRequestHandler(AbstractRequestHandler):
	def __init__(self, tickerId, platforms, assetClass=None):
		super().__init__(platforms, assetClass)
		for platform in platforms:
			self.requests[platform] = PriceRequest(tickerId, platform)

	def set_defaults(self):
		for platform, request in self.requests.items():
			if request.errorIsFatal: continue
			for parameterType in PARAMETERS:
				request.set_default_for(parameterType)

	async def find_caveats(self):
		for platform, request in self.requests.items():
			if request.errorIsFatal: continue

			if platform == "Alternative.me":
				if request.tickerId != "FGI":
					request.set_error(None, isFatal=True)

			elif platform == "CNN Business":
				if request.tickerId != "FGI":
					request.set_error(None, isFatal=True)

			elif platform == "Blockchair":
				if not request.tickerId.startswith("HALVING:"):
					request.set_error(None, isFatal=True)

			elif platform == "CoinGecko":
				if request.couldFail:
					request.set_error("Requested ticker could not be found.", isFatal=True)

			elif platform == "CCXT":
				if request.couldFail:
					request.set_error("Requested ticker could not be found.", isFatal=True)
				if not bool(request.exchange):
					request.set_error(None, isFatal=True)

			elif platform == "Twelvedata":
				if request.couldFail:
					request.set_error("Requested ticker could not be found.", isFatal=True)


	def to_dict(self):
		d = {
			"platforms": self.platforms,
			"currentPlatform": self.currentPlatform
		}

		for platform in self.platforms:
			d[platform] = self.requests[platform].to_dict()

		return d


class PriceRequest(AbstractRequest):
	def __init__(self, tickerId, platform):
		super().__init__(platform)
		self.tickerId = tickerId
		self.ticker = {}
		self.exchange = {}

		self.preferences = []

		self.hasExchange = False

	async def process_argument(self, argument):
		# None None - No successful parse
		# None True - Successful parse and add
		# "" False - Successful parse and error
		# None False - Successful parse and breaking error

		finalOutput = None

		responseMessage, success = self.add_preferences(argument)
		if responseMessage is not None: finalOutput = responseMessage
		elif success: return

		responseMessage, success = await self.add_exchange(argument)
		if responseMessage is not None: finalOutput = responseMessage
		elif success: return

		if finalOutput is None:
			self.set_error(f"`{argument[:229]}` is not a valid argument.", isFatal=True)
		elif finalOutput.startswith("`Request Quote"):
			self.set_error(None, isFatal=True)
		else:
			self.set_error(finalOutput)

	async def process_ticker(self, assetClass):
		self.handle_manual_suffix()

		preferences = self.prepare_preferences()
		suffix = preferences.get("suffix")

		if suffix in [".FUNDING", ".OI"]:
			if not self.hasExchange:
				try: _, self.exchange = await find_exchange("bitmex", self.platform)
				except: pass
		elif suffix in [".LS", ".SL"]:
			if not self.hasExchange:
				try: _, self.exchange = await find_exchange("bitfinex", self.platform)
				except: pass

		updatedTicker, error = None, None
		try:
			updatedTicker, error = await match_ticker(self.tickerId, self.exchange.get("id"), self.platform, assetClass)
		except:
			print(format_exc())
			error = "Something went wrong while processing the requested ticker."

		if error is not None:
			self.set_error(error, isFatal=True)
		elif updatedTicker.get("id") is None:
			self.couldFail = True
		else:
			self.ticker = updatedTicker
			self.tickerId = updatedTicker.get("id")
			if suffix is not None:
				self.tickerId = self.tickerId + suffix
				self.ticker["id"] = self.ticker["id"] + suffix
				self.ticker["symbol"] = self.ticker["symbol"] + suffix
			self.exchange = updatedTicker.get("exchange")

	def handle_manual_suffix(self):
		preferences = self.prepare_preferences()
		if self.tickerId.count(".") == 1 and preferences.get("suffix") is None:
			self.tickerId, suffix = self.tickerId.split(".")
			responseMessage, success = self.add_preferences(suffix)
			if responseMessage is not None or not success:
				self.tickerId += "." + suffix

	def add_parameter(self, argument, type):
		isSupported = None
		parsedParameter = None
		requiresPro = None
		for param in PARAMETERS[type]:
			if argument in param.parsablePhrases:
				parsedParameter = param
				isSupported = param.supports(self.platform)
				if isSupported: break
		return isSupported, parsedParameter, requiresPro

	def add_timeframe(self, argument): raise NotImplementedError

	# async def add_exchange(self, argument) -- inherited

	def add_style(self, argument): raise NotImplementedError

	# def add_preferences(self, argument) -- inherited

	def set_default_for(self, t):
		if t == "preferences":
			for parameter in DEFAULTS.get(self.platform, {}).get(t, []):
				if not self.has_parameter(parameter.id, self.preferences): self.preferences.append(parameter)


	def to_dict(self):
		d = {
			"ticker": self.ticker,
			"exchange": self.exchange,
			"preferences": self.prepare_preferences()
		}
		return d