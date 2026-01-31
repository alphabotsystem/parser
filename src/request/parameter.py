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
	def __init__(self, id, name, parsablePhrases, tradingview=None, premium=None, relay=None, alternativeme=None, cnnbusiness=None, dynamic=None):
		super().__init__(id, name, parsablePhrases)
		self.parsed = {
			"Alternative.me": alternativeme,
			"CNN Business": cnnbusiness,
			"TradingView Premium": premium,
			"TradingView Relay": relay,
			"TradingView": tradingview,
		}
		self.dynamic = dynamic

class HeatmapParameter(AbstractParameter):
	def __init__(self, id, name, parsablePhrases, tradingViewStockHeatmap=None, tradingViewEtfHeatmap=None, tradingViewCryptoHeatmap=None):
		super().__init__(id, name, parsablePhrases)
		self.parsed = {
			"TradingView Stock Heatmap": tradingViewStockHeatmap,
			"TradingView ETF Heatmap": tradingViewEtfHeatmap,
			"TradingView Crypto Heatmap": tradingViewCryptoHeatmap
		}

class PriceParameter(AbstractParameter):
	def __init__(self, id, name, parsablePhrases, coingecko=None, chain=None, ccxt=None, twelvedata=None, blockchair=None, alternativeme=None, cnnbusiness=None):
		super().__init__(id, name, parsablePhrases)
		self.parsed = {
			"Alternative.me": alternativeme,
			"Blockchair": blockchair,
			"CNN Business": cnnbusiness,
			"CoinGecko": coingecko,
			"On-Chain": chain,
			"CCXT": ccxt,
			"Twelvedata": twelvedata
		}

class DetailParameter(AbstractParameter):
	def __init__(self, id, name, parsablePhrases, coingecko=None, twelvedata=None):
		super().__init__(id, name, parsablePhrases)
		self.parsed = {
			"CoinGecko": coingecko,
			"Twelvedata": twelvedata
		}

class TradeParameter(AbstractParameter):
	def __init__(self, id, name, parsablePhrases, ichibot=None):
		super().__init__(id, name, parsablePhrases)
		self.parsed = {
			"Ichibot": ichibot
		}