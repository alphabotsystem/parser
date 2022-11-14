from request import HeatmapParameters


async def autocomplete_timeframe(timeframe, heatmapType):
	options = []
	for option in HeatmapParameters["timeframes"]:
		if heatmapType == "" or heatmapType == "stocks" and option.parsed["TradingView Stock Heatmap"] is not None or heatmapType == "crypto" and option.parsed["TradingView Crypto Heatmap"] is not None:
			for ph in option.parsablePhrases:
				if timeframe in ph:
					options.append(option.name)
					break
	return options

async def autocomplete_market(market, heatmapType):
	options = []
	for option in HeatmapParameters["types"]:
		if option.id != "type": continue
		if heatmapType == "" or heatmapType == "stocks" and option.parsed["TradingView Stock Heatmap"] is not None or heatmapType == "crypto" and option.parsed["TradingView Crypto Heatmap"] is not None:
			for ph in option.parsablePhrases:
				if market in ph:
					options.append(option.name)
					break
	return options

async def autocomplete_category(category, heatmapType):
	options = []
	for option in HeatmapParameters["preferences"]:
		if option.id != "category": continue
		if heatmapType == "" or heatmapType == "stocks" and option.parsed["TradingView Stock Heatmap"] is not None or heatmapType == "crypto" and option.parsed["TradingView Crypto Heatmap"] is not None:
			for ph in option.parsablePhrases:
				if category in ph:
					options.append(option.name)
					break
	return options

async def autocomplete_color(color, heatmapType):
	options = []
	for option in HeatmapParameters["preferences"]:
		if option.id != "heatmap": continue
		if heatmapType == "" or heatmapType == "stocks" and option.parsed["TradingView Stock Heatmap"] is not None or heatmapType == "crypto" and option.parsed["TradingView Crypto Heatmap"] is not None:
			for ph in option.parsablePhrases:
				if color in ph:
					options.append(option.name)
					break
	return options

async def autocomplete_size(size, heatmapType):
	options = []
	for option in HeatmapParameters["preferences"]:
		if option.id != "size": continue
		if heatmapType == "" or heatmapType == "stocks" and option.parsed["TradingView Stock Heatmap"] is not None or heatmapType == "crypto" and option.parsed["TradingView Crypto Heatmap"] is not None:
			for ph in option.parsablePhrases:
				if size in ph:
					options.append(option.name)
					break
	return options

async def autocomplete_group(group, heatmapType):
	options = []
	for option in HeatmapParameters["preferences"]:
		if option.id != "group": continue
		if heatmapType == "" or heatmapType == "stocks" and option.parsed["TradingView Stock Heatmap"] is not None or heatmapType == "crypto" and option.parsed["TradingView Crypto Heatmap"] is not None:
			for ph in option.parsablePhrases:
				if group in ph:
					options.append(option.name)
					break
	return options