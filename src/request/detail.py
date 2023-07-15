from sys import maxsize as MAXSIZE
from time import time
from traceback import format_exc

from matching.instruments import match_ticker
from .parameter import DetailParameter as Parameter
from .abstract import AbstractRequestHandler, AbstractRequest


PARAMETERS = {
	"preferences": [
		Parameter("forcePlatform", "request quote on CoinGecko", ["cg", "coingecko"], coingecko=True),
		Parameter("forcePlatform", "request quote on a stock exchange", ["equities", "forex", "fx", "metal", "metals", "stock", "stocks"], twelvedata=True),
	]
}
DEFAULTS = {
	"CoinGecko": {
		"preferences": []
	},
	"Twelvedata": {
		"preferences": []
	}
}


class DetailRequestHandler(AbstractRequestHandler):
	def __init__(self, tickerId, platforms, assetClass=None):
		super().__init__(platforms, assetClass)
		for platform in platforms:
			self.requests[platform] = DetailRequest(tickerId, platform)

	def set_defaults(self):
		for platform, request in self.requests.items():
			if request.errorIsFatal: continue
			for parameterType in PARAMETERS:
				request.set_default_for(parameterType)

	async def find_caveats(self):
		for platform, request in self.requests.items():
			if request.errorIsFatal: continue

			if not request.ticker.get("isSimple"):
				request.set_error("Details for complex tickers aren't available.", isFatal=True)

			if platform == "CoinGecko":
				pass
			elif platform == "Twelvedata":
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
	def __init__(self, tickerId, platform):
		super().__init__(platform)
		self.tickerId = tickerId
		self.ticker = {}

		self.preferences = []

	async def process_argument(self, argument):
		# None None - No successful parse
		# None True - Successful parse and add
		# "" False - Successful parse and error
		# None False - Successful parse and breaking error

		finalOutput = None

		responseMessage, success = await self.add_preferences(argument)
		if responseMessage is not None: finalOutput = responseMessage
		elif success: return

		if finalOutput is None:
			self.set_error("`{}` is not a valid argument.".format(argument[:229]), isFatal=True)
		elif finalOutput.startswith("`Request Detail"):
			self.set_error(None, isFatal=True)
		else:
			self.set_error(finalOutput)

	async def process_ticker(self, assetClass):
		updatedTicker, error = None, None
		try:
			updatedTicker, error = await match_ticker(self.tickerId, None, self.platform, assetClass)
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
			"preferences": [{"id": e.id, "value": e.parsed[self.platform]} for e in self.preferences]
		}
		return d