STRICT_MATCH = ["TradingLite", "Bookmap", "CoinGecko", "CCXT", "IEXC", "LLD", "Ichibot"]

EXCHANGE_SHORTCUTS = {
	"crypto": {
		# Binance
		"bin": "binance",
		"nance": "binance",
		# BitMEX
		"bmx": "bitmex",
		"mex": "bitmex",
		"btmx": "bitmex",
		# Binance Futures
		"binancefutures": "binanceusdm",
		"binancef": "binanceusdm",
		"fbin": "binanceusdm",
		"binf": "binanceusdm",
		"bif": "binanceusdm",
		"bnf": "binanceusdm",
		# Coinbase Pro
		"cbp": "coinbasepro",
		"coin": "coinbasepro",
		"base": "coinbasepro",
		"cb": "coinbasepro",
		"coinbase": "coinbasepro",
		"coinbasepro": "coinbasepro",
		"cbpro": "coinbasepro",
		# Bitfinex
		"bfx": "bitfinex2",
		"finex": "bitfinex2"
	},
	"traditional": {}
}

EXCHANGE_TO_TRADINGVIEW = {
	"arcx": "AMEX", "xnys": "NYSE", "otcm": "OTC", "asex": "ATHEX", "bvca": "BVCV", "dsmd": "QSE", "hstc": "HNX",
	"neoe": "NEO", "roco": "TPEX", "rtsx": "MOEX", "xads": "ADX", "xams": "EURONEXTAMS", "xbah": "BAHRAIN",
	"xbel": "BELEX", "xber": "BER", "xbog": "BVC", "xbom": "BSE", "xbra": "BSSE", "xbru": "EURONEXTBRU", "xbud": "BET",
	"xcai": "EGX", "xcnq": "CSE", "xcse": "OMXCOP", "xdfm": "DFM", "xham": "HAM", "xhel": "OMXHEX", "xhkg": "HKEX",
	"xice": "OMXICE", "xidx": "IDX", "xist": "BIST", "xkrx": "KRX", "xlim": "BVL", "xlis": "EURONEXTLIS",
	"xlit": "OMXVSE", "xlon": "LSE", "xlux": "LUXSE", "xmad": "BME", "xmex": "BMV", "xnas": "NASDAQ", "xngm": "NGM",
	"xnsa": "NSENG", "xnse": "NSE", "xose": "OSE", "xpar": "EURONEXTPAR", "xris": "OMXRSE", "xsau": "TADAWUL",
	"xshe": "SZSE", "xshg": "SSE", "xsto": "OMXSTO", "xstu": "SWB", "xswx": "BX", "xtae": "TASE", "xtai": "TWSE",
	"xtal": "OMXTSE", "xtse": "TSX", "xwar": "GPW", "bitpanda": "BITPANDAPRO", "cex": "CEXIO", "coinbasepro": "COINBASE",
	"therock": "THEROCKTRADING", "gate": "GATEIO", "bitfinex2": "BITFINEX", "binanceusdm": "BINANCE",
	"binancecoinm": "BINANCE"
}