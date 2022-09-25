from os import environ
environ["PRODUCTION"] = environ["PRODUCTION"] if "PRODUCTION" in environ and environ["PRODUCTION"] else ""

from fastapi import FastAPI, Request
from uvicorn import Config, Server
from asyncio import new_event_loop, set_event_loop
import ccxt
from ccxt.base import decimal_to_precision as dtp
from google.cloud.error_reporting import Client as ErrorReportingClient

from matching.exchanges import find_exchange
from matching.instruments import match_ticker, find_listings, find_venues, elasticsearch
from matching.autocomplete import *
from request import ChartRequestHandler
from request import HeatmapRequestHandler
from request import PriceRequestHandler
from request import DetailRequestHandler
from request import TradeRequestHandler


app = FastAPI()
logging = ErrorReportingClient(service="parser")
loop = new_event_loop()
set_event_loop(loop)


# -------------------------
# Endpoints
# -------------------------

@app.post("/parser/chart")
async def process_chart_request(req: Request):
	request = await req.json()
	arguments, platforms, tickerId = request["arguments"], request["platforms"], request["tickerId"]
	requestHandler = ChartRequestHandler(tickerId, platforms.copy())
	for argument in arguments:
		await requestHandler.parse_argument(argument)
	if tickerId is not None:
		await requestHandler.process_ticker()

	requestHandler.set_defaults()
	await requestHandler.find_caveats()
	responseMessage = requestHandler.get_preferred_platform()

	return {"message": responseMessage, "response": requestHandler.to_dict()}

@app.post("/parser/heatmap")
async def process_heatmap_request(req: Request):
	request = await req.json()
	arguments, platforms = request["arguments"], request["platforms"]
	requestHandler = HeatmapRequestHandler(platforms.copy())
	for argument in arguments:
		await requestHandler.parse_argument(argument)

	requestHandler.set_defaults()
	await requestHandler.find_caveats()
	responseMessage = requestHandler.get_preferred_platform()

	return {"message": responseMessage, "response": requestHandler.to_dict()}

@app.post("/parser/quote")
async def process_quote_request(req: Request):
	request = await req.json()
	arguments, platforms, tickerId = request["arguments"], request["platforms"], request["tickerId"]
	requestHandler = PriceRequestHandler(tickerId, platforms.copy())
	for argument in arguments:
		await requestHandler.parse_argument(argument)
	if tickerId is not None:
		await requestHandler.process_ticker()

	requestHandler.set_defaults()
	await requestHandler.find_caveats()
	responseMessage = requestHandler.get_preferred_platform()

	return {"message": responseMessage, "response": requestHandler.to_dict()}

@app.post("/parser/detail")
async def process_detail_request(req: Request):
	request = await req.json()
	arguments, platforms, tickerId = request["arguments"], request["platforms"], request["tickerId"]
	requestHandler = DetailRequestHandler(tickerId, platforms.copy())
	for argument in arguments:
		await requestHandler.parse_argument(argument)
	if tickerId is not None:
		await requestHandler.process_ticker()

	requestHandler.set_defaults()
	await requestHandler.find_caveats()
	responseMessage = requestHandler.get_preferred_platform()

	return {"message": responseMessage, "response": requestHandler.to_dict()}

@app.post("/parser/trade")
async def process_trade_request(req: Request):
	request = await req.json()
	arguments, platforms, tickerId = request["arguments"], request["platforms"], request["tickerId"]
	requestHandler = TradeRequestHandler(tickerId, platforms.copy())
	for argument in arguments:
		await requestHandler.parse_argument(argument)
	if tickerId is not None:
		await requestHandler.process_ticker()

	requestHandler.set_defaults()
	await requestHandler.find_caveats()
	responseMessage = requestHandler.get_preferred_platform()

	return {"message": responseMessage, "response": requestHandler.to_dict()}

@app.post("/parser/match_ticker")
async def run(req: Request):
	request = await req.json()
	message, response = await match_ticker(request["tickerId"], request["exchangeId"], request["platform"])
	return {"response": response, "message": message}

@app.post("/parser/find_exchange")
async def run(req: Request):
	request = await req.json()
	success, match = await find_exchange(request["raw"], request["platform"])
	return {"success": success, "match": match}

@app.post("/parser/autocomplete")
async def autocomplete(req: Request):
	request = await req.json()
	option = request["option"]
	showStockOptions = request["type"] in ["stocks", ""]
	showCryptoOptions = request["type"] in ["crypto", ""]
	if option == "timeframe":
		response = autocomplete_timeframe(request["timeframe"], showStockOptions, showCryptoOptions)
	elif option == "market":
		response = autocomplete_market(request["market"], showStockOptions, showCryptoOptions)
	elif option == "category":
		response = autocomplete_category(request["category"], showStockOptions, showCryptoOptions)
	elif option == "color":
		response = autocomplete_color(request["color"], showStockOptions, showCryptoOptions)
	elif option == "size":
		response = autocomplete_size(request["size"], showStockOptions, showCryptoOptions)
	elif option == "group":
		response = autocomplete_group(request["group"], showStockOptions, showCryptoOptions)
	else:
		response = []
	return {"response": response}

@app.post("/parser/get_listings")
async def get_listings(req: Request):
	request = await req.json()
	response, total = await find_listings(request["ticker"], request["platform"])
	return {"response": response, "total": total}	

@app.post("/parser/get_formatted_price_ccxt")
async def format_price(req: Request):
	request = await req.json()
	exchange = getattr(ccxt, request["exchangeId"])()
	await loop.run_in_executor(None, exchange.load_markets)
	precision = exchange.markets.get(request["symbol"], {}).get("precision", {}).get("price", 8)
	text = dtp.decimal_to_precision(request["price"], rounding_mode=dtp.ROUND, precision=precision, counting_mode=exchange.precisionMode, padding_mode=dtp.PAD_WITH_ZERO)
	return {"response": text.rstrip("0").rstrip(".")}

@app.post("/parser/get_formatted_amount_ccxt")
async def format_amount(req: Request):
	request = await req.json()
	exchange = getattr(ccxt, request["exchangeId"])()
	await loop.run_in_executor(None, exchange.load_markets)
	precision = exchange.markets.get(request["symbol"], {}).get("precision", {}).get("amount", 8)
	text = dtp.decimal_to_precision(request["amount"], rounding_mode=dtp.TRUNCATE, precision=precision, counting_mode=exchange.precisionMode, padding_mode=dtp.NO_PADDING)
	return {"response": text.rstrip("0").rstrip(".")}

@app.post("/parser/get_venues")
async def get_venues(req: Request):
	request = await req.json()
	venues = await find_venues(request["tickerId"], request["platforms"].split(","))
	return {"response": venues}


# -------------------------
# Startup
# -------------------------

if __name__ == "__main__":
	print("[Startup]: Ticker Parser is online")
	# config = Config(app=app, port=int(environ.get("PORT", 6900)), host="0.0.0.0", loop=loop)
	config = Config(app=app, port=6900, host="0.0.0.0", loop=loop)
	server = Server(config)
	loop.run_until_complete(server.serve())