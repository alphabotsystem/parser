import os, sys
from dotenv import load_dotenv
load_dotenv()
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../src'))

from unittest import main, TestCase
from parser import match_ticker, loop, elasticsearch


class TestMatchTicker(TestCase):
	def test1(self):
		match1 = loop.run_until_complete(match_ticker("AAPL", None, "IEXC", None))
		match2 = loop.run_until_complete(match_ticker("AAPL", None, "IEXC", "Common Stock"))
		match3 = loop.run_until_complete(match_ticker("AAPL", None, "CCXT", None))
		self.assertEqual(match1[0]["id"], "AAPL")
		self.assertEqual(match3[0], None)

	def test2(self):
		match1 = loop.run_until_complete(match_ticker("BTCUSD", None, "CCXT", None))
		match2 = loop.run_until_complete(match_ticker("BTC", None, "CCXT", None))
		match3 = loop.run_until_complete(match_ticker("BTC", None, "CCXT", "Crypto"))
		self.assertEqual(match1[0]["id"], "BTCUSDT")
		self.assertEqual(match1[0]["exchange"]["id"], "binance")
		self.assertEqual(match2[0]["id"], "BTCUSDT")
		self.assertEqual(match2[0]["exchange"]["id"], "binance")
		self.assertEqual(match3[0]["id"], "BTCUSDT")
		self.assertEqual(match3[0]["exchange"]["id"], "binance")

	def test3(self):
		match1 = loop.run_until_complete(match_ticker("EURUSD", None, "IEXC", None))
		match2 = loop.run_until_complete(match_ticker("EURUSD", None, "CCXT", None))
		self.assertEqual(match1[0]["id"], "EURUSD")
		self.assertEqual(match1[0]["exchange"]["id"], "forex")
		self.assertEqual(match2[0], None)

	def test4(self):
		match = loop.run_until_complete(match_ticker("NOK", None, "IEXC", None))
		self.assertEqual(match[0]["id"], "NOK")
		self.assertEqual(match[0]["exchange"]["id"], "xnys")

	def test5(self):
		match = loop.run_until_complete(match_ticker("AMC", None, "IEXC", None))
		self.assertEqual(match[0]["id"], "AMC")

	def test6(self):
		match1 = loop.run_until_complete(match_ticker("GBPUSD", None, "IEXC", None))
		match2 = loop.run_until_complete(match_ticker("GBPUSD", None, "CCXT", None))
		self.assertEqual(match1[0]["id"], "GBPUSD")
		self.assertEqual(match1[0]["exchange"]["id"], "forex")
		self.assertEqual(match2[0], None)

	def test7(self):
		match = loop.run_until_complete(match_ticker("XBT", None, "CCXT", None))
		self.assertEqual(match[0]["id"], "XBTUSD")
		self.assertEqual(match[0]["exchange"]["id"], "bitmex")

	def test8(self):
		match = loop.run_until_complete(match_ticker("X", None, "IEXC", None))
		self.assertEqual(match[0]["id"], "X")

	def test9(self):
		match1 = loop.run_until_complete(match_ticker("TESLA", None, "IEXC", None))
		match2 = loop.run_until_complete(match_ticker("TSLA", None, "IEXC", "Common Stock"))
		self.assertEqual(match1[0]["id"], "TSLA")
		self.assertEqual(match2[0]["id"], "TSLA")

	def test10(self):
		match = loop.run_until_complete(match_ticker("SPX", None, "TradingView", None))
		self.assertEqual(match[0]["id"], "SP:SPX")

	def test11(self):
		match = loop.run_until_complete(match_ticker("BTCUSD/SPY", None, "TradingView", None))
		self.assertEqual(match[0]["id"], "BINANCE:BTCUSDT/AMEX:SPY")


if __name__ == '__main__':
	main()