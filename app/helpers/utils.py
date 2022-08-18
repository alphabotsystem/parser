from math import ceil
from time import time, sleep
from requests import get
from traceback import format_exc


STRICT_MATCH = ["TradingLite", "Bookmap", "CoinGecko", "CCXT", "IEXC", "LLD", "Ichibot"]


class Utils(object):
	@staticmethod
	def is_tokenized_stock(e, symbol):
		ftxTokenizedStock = e.id == "ftx" and e.properties.markets[symbol]["info"].get("tokenizedEquity", False)
		bittrexTokenizedStock = e.id == "bittrex" and "TOKENIZED_SECURITY" in e.properties.markets[symbol]["info"].get("tags", [])
		return ftxTokenizedStock or bittrexTokenizedStock

	@staticmethod
	def generate_market_id(symbol, exchange):
		return exchange.properties.markets[symbol]["id"].replace("_", "").replace("/", "").replace("-", "").upper()

	@staticmethod
	def is_active(symbol, exchange):
		return exchange.properties.markets[symbol].get("active") is None or exchange.properties.markets[symbol].get("active")

	@staticmethod
	def seconds_until_cycle():
		return (time() + 60) // 60 * 60 - time()

	@staticmethod
	def get_accepted_timeframes(t):
		acceptedTimeframes = []
		for timeframe in ["1m", "2m", "3m", "5m", "10m", "15m", "20m", "30m", "1H", "2H", "3H", "4H", "6H", "8H", "12H", "1D"]:
			if t.second % 60 == 0 and (t.hour * 60 + t.minute) * 60 % Utils.get_frequency_time(timeframe) == 0:
				acceptedTimeframes.append(timeframe)
		return acceptedTimeframes

	@staticmethod
	def get_frequency_time(t):
		if t == "1D": return 86400
		elif t == "12H": return 43200
		elif t == "8H": return 28800
		elif t == "6H": return 21600
		elif t == "4H": return 14400
		elif t == "3H": return 10800
		elif t == "2H": return 7200
		elif t == "1H": return 3600
		elif t == "30m": return 1800
		elif t == "20m": return 1200
		elif t == "15m": return 900
		elif t == "10m": return 600
		elif t == "5m": return 300
		elif t == "3m": return 180
		elif t == "2m": return 120
		elif t == "1m": return 60

	@staticmethod
	def get_url(url):
		while True:
			try:
				return get(url).json()
			except:
				print(format_exc())
				sleep(10)

class TokenNotFoundException(Exception):
	def __init__(self, message):
		self.message = message
		super().__init__(message)