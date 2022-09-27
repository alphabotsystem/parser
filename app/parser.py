from os import environ
environ["PRODUCTION"] = environ["PRODUCTION"] if "PRODUCTION" in environ and environ["PRODUCTION"] else ""

from fastapi import FastAPI, Request
from uvicorn import Config, Server
from asyncio import new_event_loop, set_event_loop, create_task, wait
import ccxt
from ccxt.base import decimal_to_precision as dtp
from google.cloud.error_reporting import Client as ErrorReportingClient

from helpers.constants import ASSET_CLASSES
from matching.exchanges import find_exchange
from matching.instruments import match_ticker, find_listings, autocomplete_ticker, autocomplete_venues, elasticsearch
from matching.autocomplete import *
from request import ChartRequestHandler
from request import HeatmapRequestHandler
from request import PriceRequestHandler
from request import DetailRequestHandler


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
	arguments, platforms = request["arguments"], request["platforms"]
	tickerParts = request["tickerId"].split("|")
	tickerId, assetClass = tickerParts[0].strip(), tickerParts[-1].title().strip()
	if assetClass not in ASSET_CLASSES: assetClass = None
	requestHandler = ChartRequestHandler(tickerId, platforms, assetClass=assetClass)

	tasks = []
	for argument in arguments:
		tasks.append(create_task(requestHandler.parse_argument(argument)))
	if tickerId is not None:
		tasks.append(create_task(requestHandler.process_ticker()))
	if len(tasks) > 0:
		await wait(tasks)

	requestHandler.set_defaults()
	await requestHandler.find_caveats()
	responseMessage = requestHandler.get_preferred_platform()

	return {"message": responseMessage, "response": requestHandler.to_dict()}

@app.post("/parser/heatmap")
async def process_heatmap_request(req: Request):
	request = await req.json()
	arguments, platforms = request["arguments"], request["platforms"]
	requestHandler = HeatmapRequestHandler(platforms)

	tasks = []
	for argument in arguments:
		tasks.append(create_task(requestHandler.parse_argument(argument)))
	if len(tasks) > 0:
		await wait(tasks)

	requestHandler.set_defaults()
	await requestHandler.find_caveats()
	responseMessage = requestHandler.get_preferred_platform()

	return {"message": responseMessage, "response": requestHandler.to_dict()}

@app.post("/parser/quote")
async def process_quote_request(req: Request):
	request = await req.json()
	arguments, platforms = request["arguments"], request["platforms"]
	tickerParts = request["tickerId"].split("|")
	tickerId, assetClass = tickerParts[0].strip(), tickerParts[-1].title().strip()
	if assetClass not in ASSET_CLASSES: assetClass = None
	requestHandler = PriceRequestHandler(tickerId, platforms, assetClass=assetClass)

	tasks = []
	for argument in arguments:
		tasks.append(create_task(requestHandler.parse_argument(argument)))
	if tickerId is not None:
		tasks.append(create_task(requestHandler.process_ticker()))
	if len(tasks) > 0:
		await wait(tasks)

	requestHandler.set_defaults()
	await requestHandler.find_caveats()
	responseMessage = requestHandler.get_preferred_platform()

	return {"message": responseMessage, "response": requestHandler.to_dict()}

@app.post("/parser/detail")
async def process_detail_request(req: Request):
	request = await req.json()
	arguments, platforms = request["arguments"], request["platforms"]
	tickerParts = request["tickerId"].split("|")
	tickerId, assetClass = tickerParts[0].strip(), tickerParts[-1].title().strip()
	if assetClass not in ASSET_CLASSES: assetClass = None
	requestHandler = DetailRequestHandler(tickerId, platforms, assetClass=assetClass)

	tasks = []
	for argument in arguments:
		tasks.append(create_task(requestHandler.parse_argument(argument)))
	if tickerId is not None:
		tasks.append(create_task(requestHandler.process_ticker()))
	if len(tasks) > 0:
		await wait(tasks)

	requestHandler.set_defaults()
	await requestHandler.find_caveats()
	responseMessage = requestHandler.get_preferred_platform()

	return {"message": responseMessage, "response": requestHandler.to_dict()}

@app.post("/parser/match_ticker")
async def run(req: Request):
	request = await req.json()
	message, response = await match_ticker(request["tickerId"], request["exchangeId"], request["platform"], request.get("assetClass"))
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
	if option == "ticker":
		response = await autocomplete_ticker(request["tickerId"], request["platforms"].split(","))
	elif option == "venues":
		response = await autocomplete_venues(request["tickerId"], request["platforms"].split(","))
	elif option == "timeframe":
		response = await autocomplete_timeframe(request["timeframe"], request["type"])
	elif option == "market":
		response = await autocomplete_market(request["market"], request["type"])
	elif option == "category":
		response = await autocomplete_category(request["category"], request["type"])
	elif option == "color":
		response = await autocomplete_color(request["color"], request["type"])
	elif option == "size":
		response = await autocomplete_size(request["size"], request["type"])
	elif option == "group":
		response = await autocomplete_group(request["group"], request["type"])
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


# -------------------------
# Startup
# -------------------------

if __name__ == "__main__":
	print("[Startup]: Ticker Parser is online")
	# config = Config(app=app, port=int(environ.get("PORT", 6900)), host="0.0.0.0", loop=loop)
	config = Config(app=app, port=6900, host="0.0.0.0", loop=loop)
	server = Server(config)
	loop.run_until_complete(server.serve())