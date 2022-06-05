from os import environ
from parser import TickerParserServer

if __name__ == "__main__":
	environ["PRODUCTION_MODE"] = environ["PRODUCTION_MODE"] if "PRODUCTION_MODE" in environ and environ["PRODUCTION_MODE"] else ""
	tickerParser = TickerParserServer()
	tickerParser.run()