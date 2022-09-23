from sys import maxsize as MAXSIZE
from time import time
from asyncio import wait
from traceback import format_exc

from matching.exchanges import find_exchange
from matching.instruments import match_ticker
from .parameter import TradeParameter as Parameter
from .abstract import AbstractRequestHandler, AbstractRequest


PARAMETERS = []


class TradeRequestHandler(AbstractRequestHandler):
	def __init__(self, tickerId, platforms, bias="traditional"):
		super().__init__(platforms)
		for platform in platforms:
			self.requests[platform] = TradeRequest(tickerId, platform, bias)

	async def parse_argument(self, argument):
		for platform, request in self.requests.items():
			_argument = argument.lower().replace(" ", "")
			if request.errorIsFatal or argument == "": continue

			# None None - No successeful parse
			# None True - Successful parse and add
			# "" False - Successful parse and error
			# None False - Successful parse and breaking error

			finalOutput = None

			responseMessage, success = await request.add_exchange(_argument)
			if responseMessage is not None: finalOutput = responseMessage
			elif success: continue

			if finalOutput is None:
				request.set_error(f"`{argument[:229]}` is not a valid argument.", isFatal=True)
			elif finalOutput.startswith("`Force Trade"):
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

			if platform == "Ichibot":
				if not bool(request.exchange):
					try: _, request.exchange = await find_exchange("ftx", platform, request.parserBias)
					except: pass
				if request.exchange.get("id") == "binanceusdm":
					request.exchange["id"] = "binancefutures"


	def to_dict(self):
		d = {
			"platforms": self.platforms,
			"currentPlatform": self.currentPlatform
		}

		for platform in self.platforms:
			d[platform] = self.requests[platform].to_dict()

		return d


class TradeRequest(AbstractRequest):
	def __init__(self, tickerId, platform, bias):
		super().__init__(platform, bias)
		self.tickerId = tickerId
		self.ticker = {}
		self.exchange = {}

		self.hasExchange = False

	async def process_ticker(self):
		for i in range(len(self.ticker.parts)):
			tickerPart = self.ticker.parts[i]
			if type(tickerPart) is str: continue

		updatedTicker, error = None, None
		try: updatedTicker, error = await match_ticker(self.tickerId, self.exchange.get("id"), self.platform, self.parserBias)
		except: error = "Something went wrong while processing the requested ticker."

		if error is not None:
			self.set_error(error, isFatal=True)
		elif updatedTicker.get("id") is None:
			self.couldFail = True
		else:
			self.ticker = updatedTicker
			self.tickerId = updatedTicker.get("id")
			self.exchange = updatedTicker.get("exchange")

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

	# async def add_exchange(self, argument) -- inherited

	async def add_style(self, argument): raise NotImplementedError

	async def add_preferences(self, argument): raise NotImplementedError

	def set_default_for(self, t): pass


	def to_dict(self):
		d = {
			"ticker": self.ticker,
			"exchange": self.exchange,
			"parserBias": self.parserBias
		}
		return d