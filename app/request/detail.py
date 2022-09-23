from sys import maxsize as MAXSIZE
from time import time
from traceback import format_exc

from matching.instruments import match_ticker
from .parameter import DetailParameter as Parameter
from .abstract import AbstractRequestHandler, AbstractRequest


PARAMETERS = {
	"preferences": [
		Parameter("forcePlatform", "request quote on CoinGecko", ["cg", "coingecko", "crypto"], coingecko=True),
		Parameter("forcePlatform", "request quote on a stock exchange", ["ix", "iexc", "stock", "stocks"], iexc=True),
	]
}
DEFAULTS = {
	"CoinGecko": {
		"preferences": []
	},
	"IEXC": {
		"preferences": []
	}
}


class DetailRequestHandler(AbstractRequestHandler):
	def __init__(self, tickerId, platforms, bias="traditional"):
		super().__init__(platforms)
		for platform in platforms:
			self.requests[platform] = DetailRequest(tickerId, platform, bias)

	async def parse_argument(self, argument):
		for platform, request in self.requests.items():
			_argument = argument.lower().replace(" ", "")
			if request.errorIsFatal or argument == "": continue

			# None None - No successeful parse
			# None True - Successful parse and add
			# "" False - Successful parse and error
			# None False - Successful parse and breaking error

			finalOutput = None

			responseMessage, success = await request.add_preferences(_argument)
			if responseMessage is not None: finalOutput = responseMessage
			elif success: continue

			if finalOutput is None:
				request.set_error("`{}` is not a valid argument.".format(argument[:229]), isFatal=True)
			elif finalOutput.startswith("`Force Detail"):
				request.set_error(None, isFatal=True)
			else:
				request.set_error(finalOutput)

	def set_defaults(self):
		for platform, request in self.requests.items():
			if request.errorIsFatal: continue
			for type in PARAMETERS:
				request.set_default_for(type)

	async def find_caveats(self):
		for platform, request in self.requests.items():
			if request.errorIsFatal: continue

			if not request.ticker.get("isSimple"):
				request.set_error("Details for complex tickers aren't available.", isFatal=True)

			if platform == "CoinGecko":
				pass
			elif platform == "IEXC":
				pass


	def to_dict(self):
		d = {
			"platforms": self.platforms,
			"currentPlatform": self.currentPlatform
		}

		for platform in self.platforms:
			d[platform] = self.requests[platform].to_dict()

		return d


class DetailRequest(AbstractRequest):
	def __init__(self, tickerId, platform, bias):
		super().__init__(platform, bias)
		self.tickerId = tickerId
		self.ticker = {}

		self.preferences = []

	async def process_ticker(self):
		updatedTicker, error = None, None
		try: updatedTicker, error = await match_ticker(self.tickerId, None, self.platform, self.parserBias)
		except: error = "Something went wrong while processing the requested ticker."

		if error is not None:
			self.set_error(error, isFatal=True)
		elif updatedTicker.get("id") is None:
			self.couldFail = True
		else:
			self.ticker = updatedTicker
			self.tickerId = updatedTicker.get("id")

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

	async def add_timeframe(self, argument): raise NotImplementedError

	async def add_exchange(self, argument): raise NotImplementedError

	async def add_style(self, argument): raise NotImplementedError

	# async def add_preferences(self, argument) -- inherited

	def set_default_for(self, t):
		if t == "preferences":
			for parameter in DEFAULTS.get(self.platform, {}).get(t, []):
				if not self.has_parameter(parameter.id, self.preferences): self.preferences.append(parameter)


	def to_dict(self):
		d = {
			"ticker": self.ticker,
			"parserBias": self.parserBias,
			"preferences": [{"id": e.id, "value": e.parsed[self.platform]} for e in self.preferences]
		}
		return d