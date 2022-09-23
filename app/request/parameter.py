class AbstractParameter(object):
	def __init__(self, id, name, parsablePhrases):
		self.id = id
		self.name = name
		self.parsablePhrases = parsablePhrases
		self.parsed = {}
		self.dynamic = {}

	def supports(self, platform):
		return self.parsed[platform] is not None

	def to_dict(self):
		return {
			"id": self.id,
			"name": self.name,
			"parsablePhrases": self.parsablePhrases,
			"parsed": self.parsed,
			"dynamic": self.dynamic
		}

	@staticmethod
	def from_dict(d):
		parameter = AbstractParameter(d.get("id"), d.get("name"), d.get("parsablePhrases", []))
		parameter.parsed = d.get("parsed", {})
		parameter.dynamic = d.get("dynamic", {})
		return parameter

class ChartParameter(AbstractParameter):
	def __init__(self, id, name, parsablePhrases, tradinglite=None, tradingview=None, premium=None, bookmap=None, gocharting=None, finviz=None, alternativeme=None, cnnbusiness=None, dynamic=None):
		super().__init__(id, name, parsablePhrases)
		self.parsed = {
			"Alternative.me": alternativeme,
			"Bookmap": bookmap,
			"CNN Business": cnnbusiness,
			"Finviz": finviz,
			"GoCharting": gocharting,
			"TradingView Premium": premium,
			"TradingLite": tradinglite,
			"TradingView": tradingview,
		}
		self.dynamic = dynamic

class HeatmapParameter(AbstractParameter):
	def __init__(self, id, name, parsablePhrases, tradingViewStockHeatmap=None, tradingViewCryptoHeatmap=None):
		super().__init__(id, name, parsablePhrases)
		self.parsed = {
			"TradingView Stock Heatmap": tradingViewStockHeatmap,
			"TradingView Crypto Heatmap": tradingViewCryptoHeatmap
		}

class PriceParameter(AbstractParameter):
	def __init__(self, id, name, parsablePhrases, coingecko=None, ccxt=None, iexc=None, alternativeme=None, cnnbusiness=None, lld=None):
		super().__init__(id, name, parsablePhrases)
		self.parsed = {
			"Alternative.me": alternativeme,
			"CNN Business": cnnbusiness,
			"CoinGecko": coingecko,
			"CCXT": ccxt,
			"IEXC": iexc,
			"LLD": lld
		}

class DetailParameter(AbstractParameter):
	def __init__(self, id, name, parsablePhrases, coingecko=None, iexc=None):
		super().__init__(id, name, parsablePhrases)
		self.parsed = {
			"CoinGecko": coingecko,
			"IEXC": iexc
		}

class TradeParameter(AbstractParameter):
	def __init__(self, id, name, parsablePhrases, ichibot=None):
		super().__init__(id, name, parsablePhrases)
		self.parsed = {
			"Ichibot": ichibot
		}