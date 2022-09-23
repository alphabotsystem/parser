from request import HeatmapParameters


def autocomplete_timeframe(timeframe, showStockOptions, showCryptoOptions):
	options = []
	for option in HeatmapParameters["timeframes"]:
		if showStockOptions and option.parsed["TradingView Stock Heatmap"] is not None or showCryptoOptions and option.parsed["TradingView Crypto Heatmap"] is not None:
			for ph in option.parsablePhrases:
				if timeframe in ph:
					options.append(option.name)
					break
	return options

def autocomplete_market(market, showStockOptions, showCryptoOptions):
	options = []
	for option in HeatmapParameters["types"]:
		if option.id != "type": continue
		if showStockOptions and option.parsed["TradingView Stock Heatmap"] is not None or showCryptoOptions and option.parsed["TradingView Crypto Heatmap"] is not None:
			for ph in option.parsablePhrases:
				if market in ph:
					options.append(option.name)
					break
	return options

def autocomplete_category(category, showStockOptions, showCryptoOptions):
	options = []
	for option in HeatmapParameters["preferences"]:
		if option.id != "category": continue
		if showStockOptions and option.parsed["TradingView Stock Heatmap"] is not None or showCryptoOptions and option.parsed["TradingView Crypto Heatmap"] is not None:
			for ph in option.parsablePhrases:
				if category in ph:
					options.append(option.name)
					break
	return options

def autocomplete_color(color, showStockOptions, showCryptoOptions):
	options = []
	for option in HeatmapParameters["preferences"]:
		if option.id != "heatmap": continue
		if showStockOptions and option.parsed["TradingView Stock Heatmap"] is not None or showCryptoOptions and option.parsed["TradingView Crypto Heatmap"] is not None:
			for ph in option.parsablePhrases:
				if color in ph:
					options.append(option.name)
					break
	return options

def autocomplete_size(size, showStockOptions, showCryptoOptions):
	size = " ".join(ctx.options.get("size", "").lower().split())
	options = []
	for option in HeatmapParameters["preferences"]:
		if option.id != "size": continue
		if showStockOptions and option.parsed["TradingView Stock Heatmap"] is not None or showCryptoOptions and option.parsed["TradingView Crypto Heatmap"] is not None:
			for ph in option.parsablePhrases:
				if size in ph:
					options.append(option.name)
					break
	return options

def autocomplete_group(group, showStockOptions, showCryptoOptions):
	options = []
	for option in HeatmapParameters["preferences"]:
		if option.id != "group": continue
		if showStockOptions and option.parsed["TradingView Stock Heatmap"] is not None or showCryptoOptions and option.parsed["TradingView Crypto Heatmap"] is not None:
			for ph in option.parsablePhrases:
				if group in ph:
					options.append(option.name)
					break
	return options