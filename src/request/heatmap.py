from sys import maxsize as MAXSIZE
from time import time
from traceback import format_exc

from .parameter import HeatmapParameter as Parameter
from .abstract import AbstractRequestHandler, AbstractRequest


PARAMETERS = {
	"timeframes": [
		Parameter(1, "1-minute performance", ["1-minuteperformance", "1", "1m", "1min", "1mins", "1minute", "1minutes", "min"]),
		Parameter(2, "2-minute performance", ["2-minuteperformance", "2", "2m", "2min", "2mins", "2minute", "2minutes"]),
		Parameter(3, "3-minute performance", ["3-minuteperformance", "3", "3m", "3min", "3mins", "3minute", "3minutes"]),
		Parameter(5, "5-minute performance", ["5-minuteperformance", "5", "5m", "5min", "5mins", "5minute", "5minutes"]),
		Parameter(10, "10-minute performance", ["10-minuteperformance", "10", "10m", "10min", "10mins", "10minute", "10minutes"]),
		Parameter(15, "15-minute performance", ["15-minuteperformance", "15", "15m", "15min", "15mins", "15minute", "15minutes"]),
		Parameter(20, "20-minute performance", ["20-minuteperformance", "20", "20m", "20min", "20mins", "20minute", "20minutes"]),
		Parameter(30, "30-minute performance", ["30-minuteperformance", "30", "30m", "30min", "30mins", "30minute", "30minutes"]),
		Parameter(45, "45-minute performance", ["45-minuteperformance", "45", "45m", "45min", "45mins", "45minute", "45minutes"]),
		Parameter(60, "1-hour performance", ["1-hourperformance", "60", "60m", "60min", "60mins", "60minute", "60minutes", "1", "1h", "1hr", "1hour", "1hours", "hourly", "hour", "hr", "h"], tradingViewStockHeatmap="?color=change%7C60", tradingViewCryptoHeatmap="?color=change%7C60"),
		Parameter(120, "2-hour performance", ["2-hourperformance", "120", "120m", "120min", "120mins", "120minute", "120minutes", "2", "2h", "2hr", "2hrs", "2hour", "2hours"]),
		Parameter(180, "3-hour performance", ["3-hourperformance", "180", "180m", "180min", "180mins", "180minute", "180minutes", "3", "3h", "3hr", "3hrs", "3hour", "3hours"]),
		Parameter(240, "4-hour performance", ["4-hourperformance", "240", "240m", "240min", "240mins", "240minute", "240minutes", "4", "4h", "4hr", "4hrs", "4hour", "4hours"], tradingViewStockHeatmap="?color=change%7C240", tradingViewCryptoHeatmap="?color=change%7C240"),
		Parameter(360, "6-hour performance", ["6-hourperformance", "360", "360m", "360min", "360mins", "360minute", "360minutes", "6", "6h", "6hr", "6hrs", "6hour", "6hours"]),
		Parameter(480, "8-hour performance", ["8-hourperformance", "480", "480m", "480min", "480mins", "480minute", "480minutes", "8", "8h", "8hr", "8hrs", "8hour", "8hours"]),
		Parameter(720, "12-hour performance", ["12-hourperformance", "720", "720m", "720min", "720mins", "720minute", "720minutes", "12", "12h", "12hr", "12hrs", "12hour", "12hours"]),
		Parameter(1440, "1-day performance", ["1-dayperformance", "24", "24h", "24hr", "24hrs", "24hour", "24hours", "d", "day", "1", "1d", "1day", "daily", "1440", "1440m", "1440min", "1440mins", "1440minute", "1440minutes"], tradingViewStockHeatmap="?color=change", tradingViewCryptoHeatmap="?color=change"),
		Parameter(2880, "2-day performance", ["2-dayperformance", "48", "48h", "48hr", "48hrs", "48hour", "48hours", "2", "2d", "2day", "2880", "2880m", "2880min", "2880mins", "2880minute", "2880minutes"]),
		Parameter(3420, "3-day performance", ["3-dayperformance", "72", "72h", "72hr", "72hrs", "72hour", "72hours", "3", "3d", "3day", "3420", "3420m", "3420min", "3420mins", "3420minute", "3420minutes"]),
		Parameter(10080, "1-week performance", ["1-weekperformance", "7", "7d", "7day", "7days", "w", "week", "1w", "1week", "weekly"], tradingViewStockHeatmap="?color=Perf.W", tradingViewCryptoHeatmap="?color=Perf.W"),
		Parameter(20160, "2-week performance", ["2-weekperformance", "14", "14d", "14day", "14days", "2w", "2week"]),
		Parameter(43829, "1-month performance", ["1-monthperformance", "30d", "30day", "30days", "1", "1m", "m", "mo", "month", "1mo", "1month", "monthly"], tradingViewStockHeatmap="?color=Perf.1M", tradingViewCryptoHeatmap="?color=Perf.1M"),
		Parameter(87658, "2-month performance", ["2-monthperformance", "2", "2m", "2m", "2mo", "2month", "2months"]),
		Parameter(131487, "3-month performance", ["3-monthperformance", "3", "3m", "3m", "3mo", "3month", "3months"], tradingViewStockHeatmap="?color=Perf.3M", tradingViewCryptoHeatmap="?color=Perf.3M"),
		Parameter(175316, "4-month performance", ["4-monthperformance", "4", "4m", "4m", "4mo", "4month", "4months"]),
		Parameter(262974, "6-month performance", ["6-monthperformance", "6", "6m", "5m", "6mo", "6month", "6months"], tradingViewStockHeatmap="?color=Perf.6M", tradingViewCryptoHeatmap="?color=Perf.6M"),
		Parameter(525949, "1-year performance", ["1-yearperformance", "12", "12m", "12mo", "12month", "12months", "year", "yearly", "1year", "1y", "y", "annual", "annually"], tradingViewStockHeatmap="?color=Perf.Y", tradingViewCryptoHeatmap="?color=Perf.Y"),
		Parameter(1051898, "2-year performance", ["2-yearperformance", "24", "24m", "24mo", "24month", "24months", "2year", "2y"]),
		Parameter(1577847, "3-year performance", ["3-yearperformance", "36", "36m", "36mo", "36month", "36months", "3year", "3y"]),
		Parameter(2103796, "4-year performance", ["4-yearperformance", "48", "48m", "48mo", "48month", "48months", "4year", "4y"]),
		Parameter("ytd", "YTD performance", ["ytdperformance", "ytd"], tradingViewStockHeatmap="?color=Perf.Y", tradingViewCryptoHeatmap="?color=Perf.Y"),
		Parameter("color", "Pre-market change", ["pre-marketchange", "premarketchange", "premarketperformance"], tradingViewStockHeatmap="?color=premarket_change"),
		Parameter("color", "Post-market change", ["post-marketchange", "postmarketchange", "postmarketperformance"], tradingViewStockHeatmap="?color=postmarket_change"),
		Parameter("color", "10-day relative volume", ["10-dayrelativevolume", "relativevolume", "volume"], tradingViewStockHeatmap="?color=relative_volume_10d_calc"),
		Parameter("color", "Gap", ["gap"], tradingViewStockHeatmap="?color=gap", tradingViewCryptoHeatmap="?color=gap"),
		Parameter("color", "1-day volatility", ["1-dayvolatility", "volatility", "vol", "v"], tradingViewStockHeatmap="?color=Volatility.D", tradingViewCryptoHeatmap="?color=Volatility.D"),
	],
	"types": [
		Parameter("type", "Nasdaq 100", ["nasdaq", "nasdaq100"], tradingViewStockHeatmap="&dataset=NASDAQ100"),
		Parameter("type", "S&P 500", ["s&p500", "s&p", "sp500", "sap500", "sap", "spx", "spx500"], tradingViewStockHeatmap="&dataset=SPX500"),
		Parameter("type", "Dow Jones Composite Average", ["dji", "dowjones", "dowjonescompositeaverage", "djca"], tradingViewStockHeatmap="&dataset=DJCA"),
		Parameter("type", "All US companies", ["alluscompanies", "us", "usa", "uscompanies", "allusa"], tradingViewStockHeatmap="&dataset=AllUSA"),
		Parameter("type", "S&P/ASX 200", ["s&p/asx200", "asx200", "asx", "spasx", "sapasx", "sp200", "sap200"], tradingViewStockHeatmap="&dataset=ASX200"),
		Parameter("type", "All Australian companies", ["allaustraliancompanies", "australiancompanies", "au", "allau"], tradingViewStockHeatmap="&dataset=AllAU"),
		Parameter("type", "BEL 20", ["bel20"], tradingViewStockHeatmap="&dataset=BEL20"),
		Parameter("type", "All Belgian companies", ["allbelgiancompanies", "belgiancompanies", "be", "allbe"], tradingViewStockHeatmap="&dataset=AllBE"),
		Parameter("type", "Shenzhen Component Index", ["shenzhencomponentindex", "sci", "szse399001", "szse"], tradingViewStockHeatmap="&dataset=SZSE399001"),
		Parameter("type", "All Chinese companies", ["allchinesecompanies", "chinesecompanies", "cn", "allcn"], tradingViewStockHeatmap="&dataset=AllCN"),
		Parameter("type", "STOXX 50", ["stoxx50", "sx5e"], tradingViewStockHeatmap="&dataset=SX5E"),
		Parameter("type", "STOXX 600", ["stoxx600", "sxxp"], tradingViewStockHeatmap="&dataset=SXXP"),
		Parameter("type", "All European companies", ["alleuropeancompanies", "europeancompanies", "eu", "alleu"], tradingViewStockHeatmap="&dataset=AllEU"),
		Parameter("type", "OMX HELSINKI 25", ["omxhelsinki25", "omx", "helsinki", "helsinki25"], tradingViewStockHeatmap="&dataset=HELSINKI25"),
		Parameter("type", "All Finnish companies", ["allfinnishcompanies", "fi", "allfi", "finnishcompanies"], tradingViewStockHeatmap="&dataset=AllFI"),
		Parameter("type", "CAC 40", ["cac40", "cac"], tradingViewStockHeatmap="&dataset=CAC40"),
		Parameter("type", "All French companies", ["allfrenchcompanies", "fr", "allfr", "frenchcompanies"], tradingViewStockHeatmap="&dataset=AllFR"),
		Parameter("type", "DAX", ["dax"], tradingViewStockHeatmap="&dataset=DAX"),
		Parameter("type", "MDAX Performance", ["mdax", "mdaxperformance"], tradingViewStockHeatmap="&dataset=MDAX"),
		Parameter("type", "SDAX Performance", ["sdax", "sdaxperformance"], tradingViewStockHeatmap="&dataset=SDAX"),
		Parameter("type", "TECDAX TR", ["tecdax", "tecdaxtr"], tradingViewStockHeatmap="&dataset=TECDAX"),
		Parameter("type", "All German companies", ["allgermancompanies", "de", "allde", "germancompanies"], tradingViewStockHeatmap="&dataset=AllDE"),
		Parameter("type", "NIFTY 50", ["nifty50", "nifty"], tradingViewStockHeatmap="&dataset=NIFTY50"),
		Parameter("type", "S&P BSE SENSEX", ["s&pbsesensex", "sensex"], tradingViewStockHeatmap="&dataset=SENSEX"),
		Parameter("type", "All Indian companies", ["allindiancompanies", "in", "allin", "indiancompanies"], tradingViewStockHeatmap="&dataset=AllIN"),
		Parameter("type", "FTSE MIB INDEX", ["ftsemib", "ftsemibindex", "ftse"], tradingViewStockHeatmap="&dataset=FTSEMIB"),
		Parameter("type", "All Italian companies", ["allitaliancompanies", "it", "allit", "italiancompanies"], tradingViewStockHeatmap="&dataset=AllIT"),
		Parameter("type", "All Malaysian companies", ["allmalaysiancompanies", "my", "allmy", "malaysiancompanies"], tradingViewStockHeatmap="&dataset=AllMY"),
		Parameter("type", "MOEX RUSSIA", ["moex", "moexrussia"], tradingViewStockHeatmap="&dataset=MOEXRUSSIA"),
		Parameter("type", "MOEX BROAD MARKET (RUB)", ["moexrub", "moexbroad"], tradingViewStockHeatmap="&dataset=MOEXBROAD"),
		Parameter("type", "MOEX SMID", ["moexsmid"], tradingViewStockHeatmap="&dataset=MOEXSMID"),
		Parameter("type", "RTS", ["rts"], tradingViewStockHeatmap="&dataset=RTS"),
		Parameter("type", "RTS BROAD MARKET", ["rtsbroad"], tradingViewStockHeatmap="&dataset=RTSBROAD"),
		Parameter("type", "All Russian companies", ["allrussiancompanies", "ru", "allru", "russiancompanies"], tradingViewStockHeatmap="&dataset=AllRU"),
		Parameter("type", "All Spanish companies", ["allspanishcompanies", "es", "alles", "spanishcompanies"], tradingViewStockHeatmap="&dataset=AllES"),
		Parameter("type", "BIST 100", ["bist100"], tradingViewStockHeatmap="&dataset=BIST100"),
		Parameter("type", "BIST TUM", ["bisttum"], tradingViewStockHeatmap="&dataset=BISTTUM"),
		Parameter("type", "All Turkish companies", ["allturkishcompanies", "tr", "alltr", "turkishcompanies"], tradingViewStockHeatmap="&dataset=ALLTR"),
		Parameter("type", "UK 100 Index", ["uk100"], tradingViewStockHeatmap="&dataset=UK100"),
		Parameter("type", "All UK companies", ["allukcompanies", "uk", "alluk", "ukcompanies"], tradingViewStockHeatmap="&dataset=AllUK"),
		Parameter("type", "Crypto in USD (excluding Bitcoin)", ["cryptoinusd(excludingbitcoin)"], tradingViewCryptoHeatmap="&dataset=CryptoWithoutBTC"),
		Parameter("type", "Crypto in BTC", ["cryptoinbtc"], tradingViewCryptoHeatmap="&dataset=CryptoInBTC"),
		Parameter("type", "Crypto DeFi", ["cryptodefi"], tradingViewCryptoHeatmap="&dataset=CryptoDeFi"),
		Parameter("type", "Crypto in USD", ["full", "all", "every", "everything", "cryptoinusd"], tradingViewCryptoHeatmap="&dataset=Crypto"),
		Parameter("theme", "Light theme", ["light", "white"], tradingViewStockHeatmap="&theme=light", tradingViewCryptoHeatmap="&theme=light"),
		Parameter("theme", "Dark theme", ["dark", "black"], tradingViewStockHeatmap="&theme=dark", tradingViewCryptoHeatmap="&theme=dark"),
	],
	"style": [],
	"preferences": [
		Parameter("size", "Market cap", ["marketcap", "mcap"], tradingViewStockHeatmap="&size=market_cap_basic", tradingViewCryptoHeatmap="&size=market_cap_calc"),
		Parameter("size", "Traded volume", ["tradedvolume", "volume"], tradingViewCryptoHeatmap="&size=total_value_traded"),
		Parameter("size", "Number of employees", ["numberofemployees", "employees"], tradingViewStockHeatmap="&size=number_of_employees"),
		Parameter("size", "Dividend yield", ["dividendyield", "dividendyield"], tradingViewStockHeatmap="&size=dividend_yield_recent"),
		Parameter("size", "Price to earnings ratio (TTM)", ["pricetoearningsratio(ttm)", "pricetoearningsratio", "pricetoearnings"], tradingViewStockHeatmap="&size=price_earnings_ttm"),
		Parameter("size", "Price to sales (FY)", ["pricetosales(fy)", "pricetosales"], tradingViewStockHeatmap="&size=price_sales_ratio"),
		Parameter("size", "Price to book (FY)", ["pricetobook(fy)", "pricetobook"], tradingViewStockHeatmap="&size=price_book_ratio"),
		Parameter("size", "Price to book (MRQ)", ["pricetoboo(mrq)", "mrq"], tradingViewStockHeatmap="&size=price_book_fq"),
		Parameter("group", "No group", ["nogroup"], tradingViewStockHeatmap="&group=no_group", tradingViewCryptoHeatmap="&group=no_group"),
		Parameter("group", "Sector", ["sector"], tradingViewStockHeatmap="&group=sector"),
		Parameter("category", "Commercial services", ["commercialservices"], tradingViewStockHeatmap="&activeGroup=Commercial%20Services"),
		Parameter("category", "Communications", ["communications"], tradingViewStockHeatmap="&activeGroup=Communications"),
		Parameter("category", "Consumer durables", ["consumerdurables"], tradingViewStockHeatmap="&activeGroup=Consumer%20Durables"),
		Parameter("category", "Consumer non-durables", ["consumernon-durables"], tradingViewStockHeatmap="&activeGroup=Consumer%20Non-Durables"),
		Parameter("category", "Consumer services", ["consumerservices"], tradingViewStockHeatmap="&activeGroup=Consumer%20Services"),
		Parameter("category", "Distribution services", ["distributionservices"], tradingViewStockHeatmap="&activeGroup=Distribution%20Services"),
		Parameter("category", "Electronic technology", ["electronictechnology"], tradingViewStockHeatmap="&activeGroup=Electronic%20Technology"),
		Parameter("category", "Energy minerals", ["energyminerals"], tradingViewStockHeatmap="&activeGroup=Energy%20Minerals"),
		Parameter("category", "Finance", ["finance", "financialservices"], tradingViewStockHeatmap="&activeGroup=Finance"),
		Parameter("category", "Health services", ["healthservices"], tradingViewStockHeatmap="&activeGroup=Health%20Services"),
		Parameter("category", "Health technology", ["health", "healthtechnology", "healthcare"], tradingViewStockHeatmap="&activeGroup=Health%20Technology"),
		Parameter("category", "Industrial services", ["industrialservices"], tradingViewStockHeatmap="&activeGroup=Industrial%20Services"),
		Parameter("category", "Miscellaneous", ["miscellaneous"], tradingViewStockHeatmap="&activeGroup=Miscellaneous"),
		Parameter("category", "Non-energy minerals", ["non-energyminerals"], tradingViewStockHeatmap="&activeGroup=Non-Energy%20Minerals"),
		Parameter("category", "Process industries", ["processindustries"], tradingViewStockHeatmap="&activeGroup=Process%20Industries"),
		Parameter("category", "Producer manufacturing", ["producermanufacturing"], tradingViewStockHeatmap="&activeGroup=Producer%20Manufacturing"),
		Parameter("category", "Retail trade", ["retailtrade"], tradingViewStockHeatmap="&activeGroup=Retail%20Trade"),
		Parameter("category", "Technology services", ["technologyservices"], tradingViewStockHeatmap="&activeGroup=Technology%20Services"),
		Parameter("category", "Transportation", ["transportation"], tradingViewStockHeatmap="&activeGroup=Transportation"),
		Parameter("category", "Utilities", ["utilities"], tradingViewStockHeatmap="&activeGroup=Utilities"),
		Parameter("forcePlatform", "stocks heatmap", ["stocks"], tradingViewStockHeatmap=True),
		Parameter("forcePlatform", "crypto heatmap", ["crypto"], tradingViewCryptoHeatmap=True),
	]
}
DEFAULTS = {
	"TradingView Stock Heatmap": {
		"timeframes": [],
		"types": [AbstractRequest.find_parameter_with_id("theme", name="Dark theme", type="types", params=PARAMETERS), AbstractRequest.find_parameter_with_id("type", name="S&P 500", type="types", params=PARAMETERS)],
		"style": [],
		"preferences": []
	},
	"TradingView Crypto Heatmap": {
		"timeframes": [],
		"types": [AbstractRequest.find_parameter_with_id("theme", name="Dark theme", type="types", params=PARAMETERS), AbstractRequest.find_parameter_with_id("type", name="Crypto in USD", type="types", params=PARAMETERS)],
		"style": [],
		"preferences": []
	}
}


class HeatmapRequestHandler(AbstractRequestHandler):
	def __init__(self, platforms):
		super().__init__(platforms, None)
		for platform in platforms:
			self.requests[platform] = HeatmapRequest(platform)

	async def parse_argument(self, argument):
		for platform, request in self.requests.items():
			_argument = argument.lower().replace(" ", "")
			if request.errorIsFatal or argument == "": continue

			# None None - No successeful parse
			# None True - Successful parse and add
			# "" False - Successful parse and error
			# None False - Successful parse and breaking error

			finalOutput = None

			responseMessage, success = await request.add_timeframe(_argument)
			if responseMessage is not None: finalOutput = responseMessage
			elif success: continue

			responseMessage, success = await request.add_type(_argument)
			if responseMessage is not None: finalOutput = responseMessage
			elif success: continue

			responseMessage, success = await request.add_style(_argument)
			if responseMessage is not None: finalOutput = responseMessage
			elif success: continue

			responseMessage, success = await request.add_preferences(_argument)
			if responseMessage is not None: finalOutput = responseMessage
			elif success: continue

			if finalOutput is None:
				request.set_error(f"`{argument[:229]}` is not a valid argument.", isFatal=True)
			elif finalOutput.startswith("`Stocks Heatmap") or finalOutput.startswith("`Crypto Heatmap"):
				request.set_error(None, isFatal=True)
			else:
				request.set_error(finalOutput)

	async def process_ticker(self): raise NotImplementedError

	def set_defaults(self):
		for platform, request in self.requests.items():
			if request.errorIsFatal: continue
			for type in PARAMETERS:
				request.set_default_for(type)

	async def find_caveats(self):
		for platform, request in self.requests.items():
			if request.errorIsFatal: continue

			types = [{"id": e.id, "value": e.parsed[platform]} for e in request.types]
			preferences = [{"id": e.id, "value": e.parsed[platform]} for e in request.preferences]

			if platform == "TradingView Stock Heatmap":
				size = next((e.get("value") for e in preferences if e.get("id") == "size"), None)
				group = next((e.get("value") for e in preferences if e.get("id") == "group"), None)

				theme = next((e.get("value") for e in types if e.get("id") == "theme"), None)
				_type = next((e.get("value") for e in types if e.get("id") == "type"), None)

				if len(request.timeframes) == 0:
					request.timeframes = [AbstractRequest.find_parameter_with_id(1440, type="timeframes", params=PARAMETERS)]

				if size is None:
					request.preferences.append(AbstractRequest.find_parameter_with_id("size", name="Market cap", type="preferences", params=PARAMETERS))
				if group is None:
					request.preferences.append(AbstractRequest.find_parameter_with_id("group", name="Sector", type="preferences", params=PARAMETERS))

				if theme is None:
					request.types.append(AbstractRequest.find_parameter_with_id("theme", name="Dark theme", type="types", params=PARAMETERS))
				if _type is None:
					request.types.append(AbstractRequest.find_parameter_with_id("type", name="S&P 500", type="types", params=PARAMETERS))
			elif platform == "TradingView Crypto Heatmap":
				size = next((e.get("value") for e in preferences if e.get("id") == "size"), None)
				group = next((e.get("value") for e in preferences if e.get("id") == "group"), None)

				theme = next((e.get("value") for e in types if e.get("id") == "theme"), None)
				_type = next((e.get("value") for e in types if e.get("id") == "type"), None)

				if len(request.timeframes) == 0:
					request.timeframes = [AbstractRequest.find_parameter_with_id(1440, type="timeframes", params=PARAMETERS)]

				if size is None:
					request.preferences.append(AbstractRequest.find_parameter_with_id("size", name="Market cap", type="preferences", params=PARAMETERS))
				if group is None:
					request.preferences.append(AbstractRequest.find_parameter_with_id("group", name="No group", type="preferences", params=PARAMETERS))

				if theme is None:
					request.types.append(AbstractRequest.find_parameter_with_id("theme", name="Dark theme", type="types", params=PARAMETERS))
				if _type is None:
					request.types.append(AbstractRequest.find_parameter_with_id("type", name="Crypto in USD", type="types", params=PARAMETERS))

	def to_dict(self):
		d = {
			"platforms": self.platforms,
			"currentPlatform": self.currentPlatform
		}

		timeframes = []

		for platform in self.platforms:
			request = self.requests[platform].to_dict()
			timeframes.append(request.get("timeframes"))
			d[platform] = request

		d["timeframes"] = {p: t for p, t in zip(self.platforms, timeframes)}
		d["requestCount"] = len(d["timeframes"].get(d.get("currentPlatform"), []))

		return d


class HeatmapRequest(AbstractRequest):
	def __init__(self, platform):
		super().__init__(platform)

		self.timeframes = []
		self.types = []
		self.styles = []
		self.preferences = []

		self.currentTimeframe = None

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

	# async def add_timeframe(self, argument) -- inherited

	async def add_exchange(self, argument): raise NotImplementedError

	async def add_type(self, argument):
		heatmapStyleSupported, parsedHeatmapStyle, requiresPro = self.add_parameter(argument, "types")
		if parsedHeatmapStyle is not None and not self.has_parameter(parsedHeatmapStyle.id, self.types):
			if not heatmapStyleSupported:
				responseMessage = f"`{parsedHeatmapStyle.name.title()}` heatmap style is " + (f"only available with the {requiresPro} add-on." if requiresPro else f"not supported on {self.platform}.")
				return responseMessage, False
			self.types.append(parsedHeatmapStyle)
			return None, True
		return None, None

	# async def add_style(self, argument) -- inherited

	# async def add_preferences(self, argument) -- inherited

	def set_default_for(self, t):
		if t == "timeframes" and len(self.timeframes) == 0:
			for parameter in DEFAULTS.get(self.platform, {}).get(t, []):
				if not self.has_parameter(parameter.id, self.timeframes): self.timeframes.append(parameter)
		elif t == "types":
			for parameter in DEFAULTS.get(self.platform, {}).get(t, []):
				if not self.has_parameter(parameter.id, self.types): self.types.append(parameter)
		elif t == "style":
			for parameter in DEFAULTS.get(self.platform, {}).get(t, []):
				if not self.has_parameter(parameter.id, self.styles): self.styles.append(parameter)
		elif t == "preferences":
			for parameter in DEFAULTS.get(self.platform, {}).get(t, []):
				if not self.has_parameter(parameter.id, self.preferences): self.preferences.append(parameter)


	def to_dict(self):
		d = {
			"timeframes": [e.parsed[self.platform] for e in self.timeframes],
			"types": "".join([e.parsed[self.platform] for e in self.types]),
			"styles": [e.parsed[self.platform] for e in self.styles],
			"preferences": [{"id": e.id, "value": e.parsed[self.platform]} for e in self.preferences],
			"currentTimeframe": self.currentTimeframe
		}
		return d