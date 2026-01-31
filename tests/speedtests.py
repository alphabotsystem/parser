import os, sys
from dotenv import load_dotenv
load_dotenv()
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../src'))

from time import perf_counter
from asyncio import new_event_loop, set_event_loop, create_task, wait
from request import ChartRequestHandler

loop = new_event_loop()
set_event_loop(loop)

async def main():
	arguments = ["bitmex", "2h"]
	tickerId = "BTC"
	requestHandler = ChartRequestHandler(tickerId, ["TradingView", "TradingView Premium", "Alternative.me", "CNN Business"])

	tasks = []
	start = perf_counter()
	for argument in arguments:
		tasks.append(create_task(requestHandler.parse_argument(argument)))
	if len(tasks) > 0:
		await wait(tasks)
	end = perf_counter()
	print(f"Args: {end - start}")
	start = perf_counter()
	if tickerId is not None:
		await requestHandler.process_ticker()
	end = perf_counter()
	print(f"Ticker: {end - start}")

	requestHandler.set_defaults()
	await requestHandler.find_caveats()
	responseMessage = requestHandler.get_preferred_platform()


if __name__ == "__main__":
	start = perf_counter()
	loop.run_until_complete(main())
	end = perf_counter()
	print(f"Time taken: {end - start}")
	loop.close()