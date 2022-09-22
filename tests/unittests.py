import os, sys
from dotenv import load_dotenv
load_dotenv()
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../app'))

from unittest import main, TestCase
from parser import match_ticker, loop, elasticsearch


class TestMatchTicker(TestCase):
	def test1(self):
		match1 = loop.run_until_complete(match_ticker("AAPL", None, "IEXC", "traditional"))
		match2 = loop.run_until_complete(match_ticker("AAPL", None, "IEXC", "crypto"))
		self.assertEqual(match1["response"]["id"], "AAPL")
		self.assertEqual(match2["response"]["id"], "AAPL")

	def test2(self):
		match1 = loop.run_until_complete(match_ticker("BTCUSD", None, "CCXT", "traditional"))
		match2 = loop.run_until_complete(match_ticker("BTC", None, "CCXT", "crypto"))
		self.assertEqual(match1["response"]["id"], "BTCUSDT")
		self.assertEqual(match1["response"]["exchange"]["id"], "binance")
		self.assertEqual(match2["response"]["id"], "BTCUSDT")
		self.assertEqual(match2["response"]["exchange"]["id"], "binance")

	def test3(self):
		match1 = loop.run_until_complete(match_ticker("EURUSD", None, "IEXC", "traditional"))
		match2 = loop.run_until_complete(match_ticker("EURUSD", None, "IEXC", "crypto"))
		self.assertEqual(match1["response"]["id"], "EURUSD")
		self.assertEqual(match1["response"]["exchange"]["id"], "forex")
		self.assertEqual(match2["response"]["id"], "EURUSD")
		self.assertEqual(match2["response"]["exchange"]["id"], "forex")

	def test4(self):
		match = loop.run_until_complete(match_ticker("NOK", None, "IEXC", "traditional"))
		self.assertEqual(match["response"]["id"], "NOK")
		self.assertEqual(match["response"]["exchange"]["id"], "xnys")

	def test5(self):
		match1 = loop.run_until_complete(match_ticker("AMC", None, "IEXC", "traditional"))
		match2 = loop.run_until_complete(match_ticker("AMC", None, "IEXC", "crypto"))
		self.assertEqual(match1["response"]["id"], "AMC")
		self.assertEqual(match2["response"]["id"], "AMC")

	def test6(self):
		match1 = loop.run_until_complete(match_ticker("GBPUSD", None, "IEXC", "traditional"))
		match2 = loop.run_until_complete(match_ticker("GBPUSD", None, "IEXC", "crypto"))
		self.assertEqual(match1["response"]["id"], "GBPUSD")
		self.assertEqual(match1["response"]["exchange"]["id"], "forex")
		self.assertEqual(match2["response"]["id"], "GBPUSD")
		self.assertEqual(match2["response"]["exchange"]["id"], "forex")

	def test7(self):
		match1 = loop.run_until_complete(match_ticker("XBT", None, "CCXT", "crypto"))
		match2 = loop.run_until_complete(match_ticker("XBT", None, "CCXT", "crypto"))
		self.assertEqual(match1["response"]["id"], "XBTUSD")
		self.assertEqual(match1["response"]["exchange"]["id"], "bitmex")
		self.assertEqual(match2["response"]["id"], "XBTUSD")
		self.assertEqual(match2["response"]["exchange"]["id"], "bitmex")

	def test8(self):
		match1 = loop.run_until_complete(match_ticker("X", None, "IEXC", "traditional"))
		match2 = loop.run_until_complete(match_ticker("X", None, "IEXC", "crypto"))
		self.assertEqual(match1["response"]["id"], "X")
		self.assertEqual(match2["response"]["id"], "X")

	def test9(self):
		match1 = loop.run_until_complete(match_ticker("TESLA", None, "IEXC", "traditional"))
		match2 = loop.run_until_complete(match_ticker("TESLA", None, "IEXC", "crypto"))
		self.assertEqual(match1["response"]["id"], "TSLA")
		self.assertEqual(match2["response"]["id"], "TSLA")


if __name__ == '__main__':
	main()