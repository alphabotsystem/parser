from request import ChartParameters
from request import HeatmapParameters


async def autocomplete_hmap_timeframe(timeframe, heatmapType):
	options = []
	for option in HeatmapParameters["timeframes"]:
		noneOrStocks = heatmapType == "" or heatmapType == "stocks"
		noneOrCrypto = heatmapType == "" or heatmapType == "crypto"
		noneOfEtf = heatmapType == "" or heatmapType == "etf"
		if noneOrStocks and option.parsed["TradingView Stock Heatmap"] is not None or noneOrCrypto and option.parsed["TradingView ETF Heatmap"] is not None or noneOrCrypto and option.parsed["TradingView Crypto Heatmap"] is not None:
			for ph in option.parsablePhrases:
				if timeframe in ph:
					options.append(option.name)
					break
	return options

async def autocomplete_layout_timeframe(timeframe):
	options = []
	for option in ChartParameters["timeframes"]:
		if option.parsed["TradingView Relay"] is not None:
			for ph in option.parsablePhrases:
				if timeframe in ph:
					options.append(option.name)
					break
	return options

async def autocomplete_market(market, heatmapType):
	options = []
	for option in HeatmapParameters["style"]:
		if option.id != "dataset": continue
		noneOrStocks = heatmapType == "" or heatmapType == "stocks"
		noneOrCrypto = heatmapType == "" or heatmapType == "crypto"
		noneOfEtf = heatmapType == "" or heatmapType == "etf"
		if noneOrStocks and option.parsed["TradingView Stock Heatmap"] is not None or noneOrCrypto and option.parsed["TradingView ETF Heatmap"] is not None or noneOrCrypto and option.parsed["TradingView Crypto Heatmap"] is not None:
			for ph in option.parsablePhrases:
				if market in ph:
					options.append(option.name)
					break
	return options

async def autocomplete_category(category, heatmapType):
	options = []
	for option in HeatmapParameters["preferences"]:
		if option.id != "category": continue
		noneOrStocks = heatmapType == "" or heatmapType == "stocks"
		noneOrCrypto = heatmapType == "" or heatmapType == "crypto"
		noneOfEtf = heatmapType == "" or heatmapType == "etf"
		if noneOrStocks and option.parsed["TradingView Stock Heatmap"] is not None or noneOrCrypto and option.parsed["TradingView ETF Heatmap"] is not None or noneOrCrypto and option.parsed["TradingView Crypto Heatmap"] is not None:
			for ph in option.parsablePhrases:
				if category in ph:
					options.append(option.name)
					break
	return options

async def autocomplete_size(size, heatmapType):
	options = []
	for option in HeatmapParameters["preferences"]:
		if option.id != "size": continue
		noneOrStocks = heatmapType == "" or heatmapType == "stocks"
		noneOrCrypto = heatmapType == "" or heatmapType == "crypto"
		noneOfEtf = heatmapType == "" or heatmapType == "etf"
		if noneOrStocks and option.parsed["TradingView Stock Heatmap"] is not None or noneOrCrypto and option.parsed["TradingView ETF Heatmap"] is not None or noneOrCrypto and option.parsed["TradingView Crypto Heatmap"] is not None:
			for ph in option.parsablePhrases:
				if size in ph:
					options.append(option.name)
					break
	return options

async def autocomplete_group(group, heatmapType):
	options = []
	for option in HeatmapParameters["preferences"]:
		if option.id != "group": continue
		noneOrStocks = heatmapType == "" or heatmapType == "stocks"
		noneOrCrypto = heatmapType == "" or heatmapType == "crypto"
		noneOfEtf = heatmapType == "" or heatmapType == "etf"
		if noneOrStocks and option.parsed["TradingView Stock Heatmap"] is not None or noneOrCrypto and option.parsed["TradingView ETF Heatmap"] is not None or noneOrCrypto and option.parsed["TradingView Crypto Heatmap"] is not None:
			for ph in option.parsablePhrases:
				if group in ph:
					options.append(option.name)
					break
	return options