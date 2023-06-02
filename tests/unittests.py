import os, sys
from dotenv import load_dotenv
load_dotenv()
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../src'))

from unittest import main, TestCase
from parser import match_ticker, loop, elasticsearch


class TestMatchTicker(TestCase):
	def test1(self):
		match1 = loop.run_until_complete(match_ticker("AAPL", None, "Twelvedata", "Common Stock"))
		match2 = loop.run_until_complete(match_ticker("AAPL", None, "Twelvedata", None))
		match3 = loop.run_until_complete(match_ticker("APPLE", None, "Twelvedata", None))
		match4 = loop.run_until_complete(match_ticker("AAPL", None, "CCXT", None))
		self.assertNotEqual(match1[0], None)
		self.assertEqual(match1[0]["id"], "AAPL")
		self.assertNotEqual(match2[0], None)
		self.assertEqual(match2[0]["id"], "AAPL")
		self.assertNotEqual(match3[0], None)
		self.assertEqual(match3[0]["id"], "AAPL")
		self.assertEqual(match4[0], None)

	def test2(self):
		match1 = loop.run_until_complete(match_ticker("BITCOIN", None, "CCXT", None))
		match2 = loop.run_until_complete(match_ticker("BTCUSD", None, "CCXT", None))
		match3 = loop.run_until_complete(match_ticker("BTC", None, "CCXT", None))
		match4 = loop.run_until_complete(match_ticker("BTC", None, "CCXT", "Crypto"))
		self.assertNotEqual(match1[0], None)
		self.assertEqual(match1[0]["id"], "BTCUSDT")
		self.assertEqual(match1[0]["exchange"]["id"], "binance")
		self.assertNotEqual(match2[0], None)
		self.assertEqual(match2[0]["id"], "BTCUSDT")
		self.assertEqual(match2[0]["exchange"]["id"], "binance")
		self.assertNotEqual(match3[0], None)
		self.assertEqual(match3[0]["id"], "BTCUSDT")
		self.assertEqual(match3[0]["exchange"]["id"], "binance")
		self.assertNotEqual(match4[0], None)
		self.assertEqual(match4[0]["id"], "BTCUSDT")
		self.assertEqual(match4[0]["exchange"]["id"], "binance")

	def test3(self):
		match1 = loop.run_until_complete(match_ticker("EURUSD", None, "Twelvedata", None))
		match2 = loop.run_until_complete(match_ticker("EURUSD", None, "CCXT", None))
		self.assertNotEqual(match1[0], None)
		self.assertEqual(match1[0]["id"], "EURUSD")
		self.assertEqual(match1[0]["exchange"]["id"], "forex")
		self.assertEqual(match2[0], None)

	def test4(self):
		match = loop.run_until_complete(match_ticker("NOK", None, "Twelvedata", None))
		self.assertNotEqual(match[0], None)
		self.assertEqual(match[0]["id"], "NOK")
		self.assertEqual(match[0]["exchange"]["id"], "arcx")

	def test5(self):
		match = loop.run_until_complete(match_ticker("AMC", None, "Twelvedata", None))
		self.assertNotEqual(match[0], None)
		self.assertEqual(match[0]["id"], "AMC")

	def test6(self):
		match1 = loop.run_until_complete(match_ticker("GBPUSD", None, "Twelvedata", None))
		match2 = loop.run_until_complete(match_ticker("GBPUSD", None, "CCXT", None))
		self.assertNotEqual(match1[0], None)
		self.assertEqual(match1[0]["id"], "GBPUSD")
		self.assertEqual(match1[0]["exchange"]["id"], "forex")
		self.assertEqual(match2[0], None)

	def test7(self):
		match = loop.run_until_complete(match_ticker("XBT", None, "CCXT", None))
		self.assertNotEqual(match[0], None)
		self.assertEqual(match[0]["id"], "XBTUSD")
		self.assertEqual(match[0]["exchange"]["id"], "bitmex")

	def test8(self):
		match = loop.run_until_complete(match_ticker("X", None, "Twelvedata", None))
		self.assertNotEqual(match[0], None)
		self.assertEqual(match[0]["id"], "X")

	def test9(self):
		match1 = loop.run_until_complete(match_ticker("TSLA", None, "Twelvedata", "Common Stock"))
		match2 = loop.run_until_complete(match_ticker("TSLA", None, "Twelvedata", None))
		match3 = loop.run_until_complete(match_ticker("TESLA", None, "Twelvedata", None))
		self.assertNotEqual(match1[0], None)
		self.assertEqual(match1[0]["id"], "TSLA")
		self.assertNotEqual(match2[0], None)
		self.assertEqual(match2[0]["id"], "TSLA")
		self.assertNotEqual(match3[0], None)
		self.assertEqual(match3[0]["id"], "TSLA")

	def test10(self):
		match = loop.run_until_complete(match_ticker("SPX", None, "TradingView", None))
		self.assertNotEqual(match[0], None)
		self.assertEqual(match[0]["id"], "SP:SPX")

	def test11(self):
		match = loop.run_until_complete(match_ticker("BTCUSD/SPY", None, "TradingView", None))
		self.assertNotEqual(match[0], None)
		self.assertEqual(match[0]["id"], "BINANCE:BTCUSDT/AMEX:SPY")

	def test12(self):
		match = loop.run_until_complete(match_ticker("DIA", None, "TradingView", None))
		self.assertNotEqual(match[0], None)
		self.assertEqual(match[0]["id"], "AMEX:DIA")

	def test13(self):
		match = loop.run_until_complete(match_ticker("VIX", None, "TradingView", None))
		self.assertNotEqual(match[0], None)
		self.assertEqual(match[0]["id"], "TVC:VIX")


if __name__ == '__main__':
	main()
	loop.close()