from sys import maxsize as MAXSIZE
from asyncio import wait
from traceback import format_exc

from matching.exchanges import find_exchange

class AbstractRequestHandler(object):
	def __init__(self, platforms, assetClass):
		self.assetClass = assetClass
		self.platforms = platforms
		self.currentPlatform = self.platforms[0]
		self.requests = {}

	async def parse_argument(self, argument):
		tasks = set()
		for platform, request in self.requests.items():
			_argument = argument.lower().replace(" ", "")
			if request.errorIsFatal or _argument == "": continue
			tasks.add(request.process_argument(_argument))
		if len(tasks) > 0:
			await wait(tasks)

	async def process_ticker(self):
		tasks = set()
		for platform, request in self.requests.items():
			if request.errorIsFatal: continue
			tasks.add(request.process_ticker(self.assetClass))
		if len(tasks) > 0:
			await wait(tasks)

	def get_preferred_platform(self):
		currentMinimumErrors = MAXSIZE
		preferredPlatformOrder = []
		preferredRequestOrder = []

		for platform in self.platforms:
			request = self.requests[platform]
			numberOfErrors = MAXSIZE if len(request.errors) > 0 and request.errors[0] is None else len(request.errors)
			if currentMinimumErrors > numberOfErrors:
				currentMinimumErrors = numberOfErrors
				preferredPlatformOrder = [platform]
				preferredRequestOrder = [request]
			elif numberOfErrors == 0:
				preferredPlatformOrder.append(platform)
				preferredRequestOrder.append(request)

		i = 0
		while i < len(self.platforms):
			platform = self.platforms[i]
			if platform not in preferredPlatformOrder:
				self.platforms.remove(platform)
				self.requests.pop(platform, None)
			else: i += 1
		if len(self.platforms) > 0: self.currentPlatform = self.platforms[0]

		responseMessage = None if currentMinimumErrors == 0 else (preferredRequestOrder[0].errors[0] if len(preferredRequestOrder) > 0 else "None of the available platforms could process your request.")
		return responseMessage

class AbstractRequest(object):
	def __init__(self, platform):
		self.platform = platform
		self.errors = []
		self.errorIsFatal = False
		self.couldFail = False

	async def add_timeframe(self, argument):
		timeframeSupported, parsedTimeframe, requiresPro = self.add_parameter(argument, "timeframes")
		if parsedTimeframe is not None and not self.has_parameter(parsedTimeframe.id, self.timeframes):
			if not timeframeSupported:
				responseMessage = f"{parsedTimeframe.name} timeframe is " + (f"only available with the {requiresPro} add-on." if requiresPro else f"not supported on {self.platform}.")
				return responseMessage, False
			self.timeframes.append(parsedTimeframe)
			return None, True
		return None, None

	async def add_exchange(self, argument):
		if self.hasExchange: return None, None
		if self.platform in ["Alternative.me", "CNN Business", "CoinGecko", "Blockchair"]: return None, None
		exchangeSupported, parsedExchange = None, None
		try: exchangeSupported, parsedExchange = await find_exchange(argument, self.platform)
		except: return "Parser could not process your request. Please try again in a bit.", False
		if parsedExchange is not None:
			if not exchangeSupported:
				responseMessage = f"{parsedExchange.get('name')} exchange is not supported by {self.platform}."
				return responseMessage, False
			self.exchange = parsedExchange
			self.hasExchange = True
			return None, True
		return None, None

	async def add_style(self, argument):
		styleSupported, parsedStyle, requiresPro = self.add_parameter(argument, "style")
		if parsedStyle is not None and not self.has_parameter(parsedStyle.id, self.styles):
			if not styleSupported:
				responseMessage = f"`{parsedStyle.name.title()}` parameter is " + (f"only available with the {requiresPro} add-on." if requiresPro else f"not supported on {self.platform}.")
				return responseMessage, False
			self.styles.append(parsedStyle)
			return None, True
		return None, None

	async def add_preferences(self, argument):
		preferenceSupported, parsedPreference, requiresPro = self.add_parameter(argument, "preferences")
		if parsedPreference is not None and not self.has_parameter(parsedPreference.id, self.preferences):
			if not preferenceSupported:
				responseMessage = f"`{parsedPreference.name.title()}` parameter is " + (f"only available with the {requiresPro} add-on." if requiresPro else f"not supported by {self.platform}.")
				return responseMessage, False
			self.preferences.append(parsedPreference)
			return None, True
		return None, None

	@staticmethod
	def find_parameter_by_id(_id, params, platform, name=None, parameterType=None):
		for t in (params.keys() if parameterType is None else [parameterType]):
			for parameter in params[t]:
				if parameter.supports(platform) and _id == parameter.id and (name is None or parameter.name == name):
					return parameter
		raise ValueError(f"Parameter with id `{_id}`, name `{name}` and type `{parameterType}` is not supported on {platform}.")

	@staticmethod
	def find_parameter_by_trigger(trigger, params, platform, parameterType=None):
		for t in (params.keys() if parameterType is None else [parameterType]):
			for parameter in params[t]:
				if parameter.supports(platform) and trigger in parameter.parsablePhrases:
					return parameter
		return None

	def has_parameter(self, _id, _list, argument=None):
		for e in _list:
			if e.id == _id and (argument is None or e.parsed[self.platform] == argument): return True
		return False

	def set_error(self, error, isFatal=False):
		if len(self.errors) > 0 and self.errors[0] is None: return
		self.errorIsFatal = isFatal
		self.errors.insert(0, error)

	def prepare_styles(self):
		styles = {}
		for e in self.styles:
			styles[e.id] = e.parsed[self.platform]
		return styles

	def prepare_preferences(self):
		parsed = [(e.id, e.parsed[self.platform]) for e in self.preferences]
		preferences = {}
		for i, e in parsed:
			preferences[i] = e
		return preferences