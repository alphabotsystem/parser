from sys import maxsize as MAXSIZE
from time import time
from traceback import format_exc

from .parameter import HeatmapParameter as Parameter
from .abstract import AbstractRequestHandler, AbstractRequest


PARAMETERS = {
	"timeframes": [
		Parameter(1, "1-minute performance", ["1-minuteperformance", "1", "1m", "1min", "1mins", "1minute", "1minutes", "min"]),
		Parameter(2, "2-minute performance", ["2-minuteperformance", "2", "2m", "2min", "2mins", "2minute", "2minutes"]),
		Parameter(3, "3-minute performance", ["3-minuteperformance", "3", "3m", "3min", "3mins", "3minute", "3minutes"]),
		Parameter(5, "5-minute performance", ["5-minuteperformance", "5", "5m", "5min", "5mins", "5minute", "5minutes"]),
		Parameter(10, "10-minute performance", ["10-minuteperformance", "10", "10m", "10min", "10mins", "10minute", "10minutes"]),
		Parameter(15, "15-minute performance", ["15-minuteperformance", "15", "15m", "15min", "15mins", "15minute", "15minutes"]),
		Parameter(20, "20-minute performance", ["20-minuteperformance", "20", "20m", "20min", "20mins", "20minute", "20minutes"]),
		Parameter(30, "30-minute performance", ["30-minuteperformance", "30", "30m", "30min", "30mins", "30minute", "30minutes"]),
		Parameter(45, "45-minute performance", ["45-minuteperformance", "45", "45m", "45min", "45mins", "45minute", "45minutes"]),
		Parameter(60, "1-hour performance", ["1-hourperformance", "60", "60m", "60min", "60mins", "60minute", "60minutes", "1", "1h", "1hr", "1hour", "1hours", "hourly", "hour", "hr", "h"], tradingViewStockHeatmap="?color=change%7C60", tradingViewCryptoHeatmap="?color=change%7C60"),
		Parameter(120, "2-hour performance", ["2-hourperformance", "120", "120m", "120min", "120mins", "120minute", "120minutes", "2", "2h", "2hr", "2hrs", "2hour", "2hours"]),
		Parameter(180, "3-hour performance", ["3-hourperformance", "180", "180m", "180min", "180mins", "180minute", "180minutes", "3", "3h", "3hr", "3hrs", "3hour", "3hours"]),
		Parameter(240, "4-hour performance", ["4-hourperformance", "240", "240m", "240min", "240mins", "240minute", "240minutes", "4", "4h", "4hr", "4hrs", "4hour", "4hours"], tradingViewStockHeatmap="?color=change%7C240", tradingViewCryptoHeatmap="?color=change%7C240"),
		Parameter(360, "6-hour performance", ["6-hourperformance", "360", "360m", "360min", "360mins", "360minute", "360minutes", "6", "6h", "6hr", "6hrs", "6hour", "6hours"]),
		Parameter(480, "8-hour performance", ["8-hourperformance", "480", "480m", "480min", "480mins", "480minute", "480minutes", "8", "8h", "8hr", "8hrs", "8hour", "8hours"]),
		Parameter(720, "12-hour performance", ["12-hourperformance", "720", "720m", "720min", "720mins", "720minute", "720minutes", "12", "12h", "12hr", "12hrs", "12hour", "12hours"]),
		Parameter(1440, "1-day performance", ["1-dayperformance", "24", "24h", "24hr", "24hrs", "24hour", "24hours", "d", "day", "1", "1d", "1day", "daily", "1440", "1440m", "1440min", "1440mins", "1440minute", "1440minutes"], tradingViewStockHeatmap="?color=change", tradingViewCryptoHeatmap="?color=change"),
		Parameter(2880, "2-day performance", ["2-dayperformance", "48", "48h", "48hr", "48hrs", "48hour", "48hours", "2", "2d", "2day", "2880", "2880m", "2880min", "2880mins", "2880minute", "2880minutes"]),
		Parameter(3420, "3-day performance", ["3-dayperformance", "72", "72h", "72hr", "72hrs", "72hour", "72hours", "3", "3d", "3day", "3420", "3420m", "3420min", "3420mins", "3420minute", "3420minutes"]),
		Parameter(10080, "1-week performance", ["1-weekperformance", "7", "7d", "7day", "7days", "w", "week", "1w", "1week", "weekly"], tradingViewStockHeatmap="?color=Perf.W", tradingViewCryptoHeatmap="?color=Perf.W"),
		Parameter(20160, "2-week performance", ["2-weekperformance", "14", "14d", "14day", "14days", "2w", "2week"]),
		Parameter(43829, "1-month performance", ["1-monthperformance", "30d", "30day", "30days", "1", "1m", "m", "mo", "month", "1mo", "1month", "monthly"], tradingViewStockHeatmap="?color=Perf.1M", tradingViewCryptoHeatmap="?color=Perf.1M"),
		Parameter(87658, "2-month performance", ["2-monthperformance", "2", "2m", "2m", "2mo", "2month", "2months"]),
		Parameter(131487, "3-month performance", ["3-monthperformance", "3", "3m", "3m", "3mo", "3month", "3months"], tradingViewStockHeatmap="?color=Perf.3M", tradingViewCryptoHeatmap="?color=Perf.3M"),
		Parameter(175316, "4-month performance", ["4-monthperformance", "4", "4m", "4m", "4mo", "4month", "4months"]),
		Parameter(262974, "6-month performance", ["6-monthperformance", "6", "6m", "5m", "6mo", "6month", "6months"], tradingViewStockHeatmap="?color=Perf.6M", tradingViewCryptoHeatmap="?color=Perf.6M"),
		Parameter(525949, "1-year performance", ["1-yearperformance", "12", "12m", "12mo", "12month", "12months", "year", "yearly", "1year", "1y", "y", "annual", "annually"], tradingViewStockHeatmap="?color=Perf.Y", tradingViewCryptoHeatmap="?color=Perf.Y"),
		Parameter(1051898, "2-year performance", ["2-yearperformance", "24", "24m", "24mo", "24month", "24months", "2year", "2y"]),
		Parameter(1577847, "3-year performance", ["3-yearperformance", "36", "36m", "36mo", "36month", "36months", "3year", "3y"]),
		Parameter(2103796, "4-year performance", ["4-yearperformance", "48", "48m", "48mo", "48month", "48months", "4year", "4y"]),
		Parameter("ytd", "YTD performance", ["ytdperformance", "ytd"], tradingViewStockHeatmap="?color=Perf.Y", tradingViewCryptoHeatmap="?color=Perf.Y"),
		Parameter("color", "Pre-market change", ["pre-marketchange", "premarketchange", "premarketperformance"], tradingViewStockHeatmap="?color=premarket_change"),
		Parameter("color", "Post-market change", ["post-marketchange", "postmarketchange", "postmarketperformance"], tradingViewStockHeatmap="?color=postmarket_change"),
		Parameter("color", "10-day relative volume", ["10-dayrelativevolume", "relativevolume", "volume"], tradingViewStockHeatmap="?color=relative_volume_10d_calc"),
		Parameter("color", "Gap", ["gap"], tradingViewStockHeatmap="?color=gap", tradingViewCryptoHeatmap="?color=gap"),
		Parameter("color", "1-day volatility", ["1-dayvolatility", "volatility", "vol", "v"], tradingViewStockHeatmap="?color=Volatility.D", tradingViewCryptoHeatmap="?color=Volatility.D"),
	],
	"style": [
		Parameter("dataset", "Nasdaq 100 Index", ["nasdaq100index", "nasdaq", "nasdaq100"], tradingViewStockHeatmap={"dataset": "NASDAQ100"}),
		Parameter("dataset", "Nasdaq Composite Index", ["nasdaqcompositeindex", "nasdaqcomposite"], tradingViewStockHeatmap={"dataset": "NASDAQCOMPOSITE"}),
		Parameter("dataset", "Dow Jones Composite Average Index", ["dowjonescompositeaverageindex", "dji", "dowjones", "dowjonescompositeaverage", "djca"], tradingViewStockHeatmap={"dataset": "DJCA"}),
		Parameter("dataset", "Dow Jones Industrial Average Index", ["dowjonesindustrialaverageindex", "dowjonesindustrialaverage"], tradingViewStockHeatmap={"dataset": "DJDJI"}),
		Parameter("dataset", "Dow Jones Transportation Average Index", ["dowjonestransportationaverageindex", "dowjonestransportationaverage"], tradingViewStockHeatmap={"dataset": "DJDJT"}),
		Parameter("dataset", "Dow Jones Utility Average Index", ["dowjonesutilityaverageindex", "dowjonesutilityaverage"], tradingViewStockHeatmap={"dataset": "DJDJU"}),
		Parameter("dataset", "KBW Nasdaq Bank Index", ["kbwnasdaqbankindex", "kbwnasdaqbank"], tradingViewStockHeatmap={"dataset": "NASDAQBKX"}),
		Parameter("dataset", "Mini Russell 2000 Index", ["minirussell2000index", "minirussell2000"], tradingViewStockHeatmap={"dataset": "CBOEFTSEMRUT"}),
		Parameter("dataset", "Russell 1000", ["russell1000", "russell1000"], tradingViewStockHeatmap={"dataset": "TVCRUI"}),
		Parameter("dataset", "Russell 2000", ["russell2000", "russell2000"], tradingViewStockHeatmap={"dataset": "TVCRUT"}),
		Parameter("dataset", "Russell 3000", ["russell3000", "russell3000"], tradingViewStockHeatmap={"dataset": "TVCRUA"}),
		Parameter("dataset", "S&P 500 Index", ["s&p500index", "s&p500", "s&p", "sp500", "sap500", "sap", "spx", "spx500"], tradingViewStockHeatmap={"dataset": "SPX500"}),
		Parameter("dataset", "All US companies", ["alluscompanies", "us", "usa", "uscompanies", "allusa"], tradingViewStockHeatmap={"dataset": "AllUSA"}),
		Parameter("dataset", "MERVAL Index", ["mervalindex", "merval"], tradingViewStockHeatmap={"dataset": "BCBAIMV"}),
		Parameter("dataset", "All Argentinean companies", ["allargentineancompanies", "allargentineancompanies"], tradingViewStockHeatmap={"dataset": "AllAR"}),
		Parameter("dataset", "S&P/ASX 200 Index", ["s&p/asx200index", "s&p/asx200", "asx200", "asx", "spasx", "sapasx", "sp200", "sap200"], tradingViewStockHeatmap={"dataset": "ASX200"}),
		Parameter("dataset", "All Australian companies", ["allaustraliancompanies", "australiancompanies", "au", "allau"], tradingViewStockHeatmap={"dataset": "AllAU"}),
		Parameter("dataset", "BEL 20 Index", ["bel20index", "bel20"], tradingViewStockHeatmap={"dataset": "BEL20"}),
		Parameter("dataset", "All Belgian companies", ["allbelgiancompanies", "belgiancompanies", "be", "allbe"], tradingViewStockHeatmap={"dataset": "AllBE"}),
		Parameter("dataset", "IBovespa Index", ["ibovespaindex", "ibovespa"], tradingViewStockHeatmap={"dataset": "IBOV"}),
		Parameter("dataset", "IBRX 50 Index", ["ibrx50index", "ibrx50"], tradingViewStockHeatmap={"dataset": "IBXL"}),
		Parameter("dataset", "All Brazilian companies", ["allbraziliancompanies", "allbraziliancompanies"], tradingViewStockHeatmap={"dataset": "AllBR"}),
		Parameter("dataset", "S&P/TSX Composite Index", ["s&p/tsxcompositeindex", "s&p/tsxcomposite"], tradingViewStockHeatmap={"dataset": "TSX"}),
		Parameter("dataset", "All Canadian companies", ["allcanadiancompanies", "allcanadiancompanies"], tradingViewStockHeatmap={"dataset": "AllCA"}),
		Parameter("dataset", "S&P IPSA", ["s&pipsa", "s&pipsa"], tradingViewStockHeatmap={"dataset": "BCSSPIPSA"}),
		Parameter("dataset", "All Chilean companies", ["allchileancompanies", "allchileancompanies"], tradingViewStockHeatmap={"dataset": "AllCL"}),
		Parameter("dataset", "SZSE Component Index", ["szsecomponentindex", "szsecomponent", "shenzhencomponentindex", "sci", "szse399001", "szse"], tradingViewStockHeatmap={"dataset": "SZSE399001"}),
		Parameter("dataset", "All Chinese companies", ["allchinesecompanies", "chinesecompanies", "cn", "allcn"], tradingViewStockHeatmap={"dataset": "AllCN"}),
		Parameter("dataset", "INDICE DE CAPITALIZACION BURSATIL", ["indicedecapitalizacionbursatil", "indicedecapitalizacionbursatil"], tradingViewStockHeatmap={"dataset": "BVCICAP"}),
		Parameter("dataset", "All Colombian companies", ["allcolombiancompanies", "allcolombiancompanies"], tradingViewStockHeatmap={"dataset": "AllCO"}),
		Parameter("dataset", "Alternative Market Index CSE", ["alternativemarketindexcse", "alternativemarketindexcse"], tradingViewStockHeatmap={"dataset": "CSECYALTE"}),
		Parameter("dataset", "Main Market Index CSE", ["mainmarketindexcse", "mainmarketindexcse"], tradingViewStockHeatmap={"dataset": "CSECYMAIN"}),
		Parameter("dataset", "General Index CSE", ["generalindexcse", "generalindexcse"], tradingViewStockHeatmap={"dataset": "CSECYGEN"}),
		Parameter("dataset", "Investment Market Index CSE", ["investmentmarketindexcse", "investmentmarketindexcse"], tradingViewStockHeatmap={"dataset": "CSECYINVE"}),
		Parameter("dataset", "Hotel Index CSE", ["hotelindexcse", "hotelindexcse"], tradingViewStockHeatmap={"dataset": "CSECYHOTEL"}),
		Parameter("dataset", "FTSE/CYSE 20", ["ftse/cyse20", "ftse/cyse20"], tradingViewStockHeatmap={"dataset": "CSECYFTSE20"}),
		Parameter("dataset", "All Cyprus companies", ["allcypruscompanies", "allcypruscompanies"], tradingViewStockHeatmap={"dataset": "AllCY"}),
		Parameter("dataset", "OMX Copenhagen 25 Index", ["omxcopenhagen25index", "omxcopenhagen25"], tradingViewStockHeatmap={"dataset": "OMXCOPOMXC25"}),
		Parameter("dataset", "All Danish companies", ["alldanishcompanies", "alldanishcompanies"], tradingViewStockHeatmap={"dataset": "AllDK"}),
		Parameter("dataset", "EGX 30 Price Return Index", ["egx30pricereturnindex", "egx30pricereturn"], tradingViewStockHeatmap={"dataset": "EGXEGX30"}),
		Parameter("dataset", "All Egyptian companies", ["allegyptiancompanies", "allegyptiancompanies"], tradingViewStockHeatmap={"dataset": "AllEG"}),
		Parameter("dataset", "OMX Tallinn GI", ["omxtallinngi", "omxtallinngi"], tradingViewStockHeatmap={"dataset": "OMXTSEOMXTGI"}),
		Parameter("dataset", "All Estonian companies", ["allestoniancompanies", "allestoniancompanies"], tradingViewStockHeatmap={"dataset": "AllEE"}),
		Parameter("dataset", "Euro Stoxx 50 Index", ["eurostoxx50index", "eurostoxx50", "stoxx50", "sx5e"], tradingViewStockHeatmap={"dataset": "SX5E"}),
		Parameter("dataset", "STOXX 600", ["stoxx600", "sxxp"], tradingViewStockHeatmap={"dataset": "SXXP"}),
		Parameter("dataset", "All European Union companies", ["alleuropeanunioncompanies", "europeanunioncompanies", "eu", "alleu"], tradingViewStockHeatmap={"dataset": "AllEUN"}),
		Parameter("dataset", "All European companies", ["alleuropeancompanies", "europeancompanies"], tradingViewStockHeatmap={"dataset": "AllEU"}),
		Parameter("dataset", "OMX Helsinki 25 Index", ["omxhelsinki25index", "omxhelsinki25", "omx", "helsinki", "helsinki25"], tradingViewStockHeatmap={"dataset": "HELSINKI25"}),
		Parameter("dataset", "All Finnish companies", ["allfinnishcompanies", "fi", "allfi", "finnishcompanies"], tradingViewStockHeatmap={"dataset": "AllFI"}),
		Parameter("dataset", "CAC 40 Index", ["cac40index", "cac40", "cac"], tradingViewStockHeatmap={"dataset": "CAC40"}),
		Parameter("dataset", "All French companies", ["allfrenchcompanies", "fr", "allfr", "frenchcompanies"], tradingViewStockHeatmap={"dataset": "AllFR"}),
		Parameter("dataset", "DAX Index", ["daxindex", "dax"], tradingViewStockHeatmap={"dataset": "DAX"}),
		Parameter("dataset", "MDAX Performance", ["mdax", "mdaxperformance"], tradingViewStockHeatmap={"dataset": "MDAX"}),
		Parameter("dataset", "SDAX Performance", ["sdax", "sdaxperformance"], tradingViewStockHeatmap={"dataset": "SDAX"}),
		Parameter("dataset", "TECDAX TR", ["tecdax", "tecdaxtr"], tradingViewStockHeatmap={"dataset": "TECDAX"}),
		Parameter("dataset", "All German companies", ["allgermancompanies", "de", "allde", "germancompanies"], tradingViewStockHeatmap={"dataset": "AllDE"}),
		Parameter("dataset", "Composite Index", ["compositeindex", "composite"], tradingViewStockHeatmap={"dataset": "ATHEXGD"}),
		Parameter("dataset", "FTSE/ATHEX Market Index", ["ftse/athexmarketindex", "ftse/athexmarket"], tradingViewStockHeatmap={"dataset": "ATHEXFTSEA"}),
		Parameter("dataset", "FTSE/ATHEX Mid Cap Index", ["ftse/athexmidcapindex", "ftse/athexmidcap"], tradingViewStockHeatmap={"dataset": "ATHEXFTSEM"}),
		Parameter("dataset", "FTSE/ATHEX Large Cap Index", ["ftse/athexlargecapindex", "ftse/athexlargecap"], tradingViewStockHeatmap={"dataset": "ATHEXFTSE"}),
		Parameter("dataset", "FTSE/ATHEX Mid & Small Cap Factor-Weighted Index", ["ftse/athexmid&smallcapfactor-weightedindex", "ftse/athexmid&smallcapfactor-weighted"], tradingViewStockHeatmap={"dataset": "ATHEXFTSEMSFW"}),
		Parameter("dataset", "FTSE/ATHEX Global Traders Index Plus", ["ftse/athexglobaltradersindexplus", "ftse/athexglobaltradersindexplus"], tradingViewStockHeatmap={"dataset": "ATHEXFTSEGTI"}),
		Parameter("dataset", "All Greek companies", ["allgreekcompanies", "allgreekcompanies"], tradingViewStockHeatmap={"dataset": "AllGRC"}),
		Parameter("dataset", "Hang Seng Index", ["hangsengindex", "hangseng"], tradingViewStockHeatmap={"dataset": "HSI"}),
		Parameter("dataset", "All Hong Kong companies", ["allhongkongcompanies", "allhongkongcompanies"], tradingViewStockHeatmap={"dataset": "AllHK"}),
		Parameter("dataset", "Budapest Stock Index", ["budapeststockindex", "budapeststock"], tradingViewStockHeatmap={"dataset": "BETBUX"}),
		Parameter("dataset", "All Hungarian companies", ["allhungariancompanies", "allhungariancompanies"], tradingViewStockHeatmap={"dataset": "AllHU"}),
		Parameter("dataset", "OMX Iceland 10", ["omxiceland10", "omxiceland10"], tradingViewStockHeatmap={"dataset": "OMXICEOMXI10"}),
		Parameter("dataset", "All Icelandic companies", ["allicelandiccompanies", "allicelandiccompanies"], tradingViewStockHeatmap={"dataset": "AllIS"}),
		Parameter("dataset", "Nifty 50 Index", ["nifty50index", "nifty50", "nifty"], tradingViewStockHeatmap={"dataset": "NIFTY50"}),
		Parameter("dataset", "S&P BSE Sensex Index", ["s&pbsesensexindex", "s&pbsesensex", "sensex"], tradingViewStockHeatmap={"dataset": "SENSEX"}),
		Parameter("dataset", "All Indian companies", ["allindiancompanies", "in", "allin", "indiancompanies"], tradingViewStockHeatmap={"dataset": "AllIN"}),
		Parameter("dataset", "IDX30 INDEX", ["idx30index", "idx30"], tradingViewStockHeatmap={"dataset": "IDX30"}),
		Parameter("dataset", "All Indonesian companies", ["allindonesiancompanies", "allindonesiancompanies"], tradingViewStockHeatmap={"dataset": "AllID"}),
		Parameter("dataset", "TA-35 Index", ["ta-35index", "ta-35"], tradingViewStockHeatmap={"dataset": "TA35"}),
		Parameter("dataset", "TA-125", ["ta-125", "ta-125"], tradingViewStockHeatmap={"dataset": "TA125"}),
		Parameter("dataset", "All Israeli companies", ["allisraelicompanies", "allisraelicompanies"], tradingViewStockHeatmap={"dataset": "AllIL"}),
		Parameter("dataset", "FTSE MIB INDEX", ["ftsemib", "ftsemibindex", "ftse"], tradingViewStockHeatmap={"dataset": "FTSEMIB"}),
		Parameter("dataset", "All Italian companies", ["allitaliancompanies", "it", "allit", "italiancompanies"], tradingViewStockHeatmap={"dataset": "AllIT"}),
		Parameter("dataset", "Nikkei 225 Index", ["nikkei225index", "nikkei225"], tradingViewStockHeatmap={"dataset": "NI225"}),
		Parameter("dataset", "All Japanese companies", ["alljapanesecompanies", "alljapanesecompanies"], tradingViewStockHeatmap={"dataset": "AllJP"}),
		Parameter("dataset", "All-Share Index (PR)", ["all-shareindex(pr)", "all-shareindex(pr)"], tradingViewStockHeatmap={"dataset": "KSEBKA"}),
		Parameter("dataset", "All-Share Index (TR)", ["all-shareindex(tr)", "all-shareindex(tr)"], tradingViewStockHeatmap={"dataset": "KSEBKAT"}),
		Parameter("dataset", "Boursa Kuwait Main Market 50 Index", ["boursakuwaitmainmarket50index", "boursakuwaitmainmarket50"], tradingViewStockHeatmap={"dataset": "KSEBKM50"}),
		Parameter("dataset", "Main Market Index (PR)", ["mainmarketindex(pr)", "mainmarketindex(pr)"], tradingViewStockHeatmap={"dataset": "KSEBKM"}),
		Parameter("dataset", "Main Market Index (TR)", ["mainmarketindex(tr)", "mainmarketindex(tr)"], tradingViewStockHeatmap={"dataset": "KSEBKMT"}),
		Parameter("dataset", "Premier Market Index (PR)", ["premiermarketindex(pr)", "premiermarketindex(pr)"], tradingViewStockHeatmap={"dataset": "KSEBKP"}),
		Parameter("dataset", "Premier Market Index (TR)", ["premiermarketindex(tr)", "premiermarketindex(tr)"], tradingViewStockHeatmap={"dataset": "KSEBKPT"}),
		Parameter("dataset", "All Kuwaiti companies", ["allkuwaiticompanies", "allkuwaiticompanies"], tradingViewStockHeatmap={"dataset": "AllKW"}),
		Parameter("dataset", "OMX Riga GI", ["omxrigagi", "omxrigagi"], tradingViewStockHeatmap={"dataset": "OMXRSEOMXRGI"}),
		Parameter("dataset", "All Latvian companies", ["alllatviancompanies", "alllatviancompanies"], tradingViewStockHeatmap={"dataset": "AllLV"}),
		Parameter("dataset", "OMX Vilnius GI", ["omxvilniusgi", "omxvilniusgi"], tradingViewStockHeatmap={"dataset": "OMXVSEOMXVGI"}),
		Parameter("dataset", "All Lithuanian companies", ["alllithuaniancompanies", "alllithuaniancompanies"], tradingViewStockHeatmap={"dataset": "AllLT"}),
		Parameter("dataset", "All Malaysian companies", ["allmalaysiancompanies", "my", "allmy", "malaysiancompanies"], tradingViewStockHeatmap={"dataset": "AllMY"}),
		Parameter("dataset", "IPC Mexico Index", ["ipcmexicoindex", "ipcmexico"], tradingViewStockHeatmap={"dataset": "BMVME"}),
		Parameter("dataset", "All Mexican companies", ["allmexicancompanies", "allmexicancompanies"], tradingViewStockHeatmap={"dataset": "AllMX"}),
		Parameter("dataset", "All Moroccan companies", ["allmoroccancompanies", "allmoroccancompanies"], tradingViewStockHeatmap={"dataset": "AllMA"}),
		Parameter("dataset", "AEX Index", ["aexindex", "aex"], tradingViewStockHeatmap={"dataset": "AEX"}),
		Parameter("dataset", "All Dutch companies", ["alldutchcompanies", "alldutchcompanies"], tradingViewStockHeatmap={"dataset": "AllNL"}),
		Parameter("dataset", "S&P / NZX 50 Index Gross", ["s&p/nzx50indexgross", "s&p/nzx50indexgross"], tradingViewStockHeatmap={"dataset": "NZXNZ50G"}),
		Parameter("dataset", "All New Zealand companies", ["allnewzealandcompanies", "allnewzealandcompanies"], tradingViewStockHeatmap={"dataset": "AllNZ"}),
		Parameter("dataset", "NGX 30 Index", ["ngx30index", "ngx30"], tradingViewStockHeatmap={"dataset": "NSENGNGX30"}),
		Parameter("dataset", "All Nigerian companies", ["allnigeriancompanies", "allnigeriancompanies"], tradingViewStockHeatmap={"dataset": "AllNGA"}),
		Parameter("dataset", "All Norwegian companies", ["allnorwegiancompanies", "allnorwegiancompanies"], tradingViewStockHeatmap={"dataset": "AllNO"}),
		Parameter("dataset", "Banking Tradable Index", ["bankingtradableindex", "bankingtradable"], tradingViewStockHeatmap={"dataset": "PSXBKTI"}),
		Parameter("dataset", "JS Momentum Factor Index", ["jsmomentumfactorindex", "jsmomentumfactor"], tradingViewStockHeatmap={"dataset": "PSXJSMFI"}),
		Parameter("dataset", "KMI 30 Index", ["kmi30index", "kmi30"], tradingViewStockHeatmap={"dataset": "PSXKMI30"}),
		Parameter("dataset", "KMI All Share Index", ["kmiallshareindex", "kmiallshare"], tradingViewStockHeatmap={"dataset": "PSXKMIALLSHR"}),
		Parameter("dataset", "KSE 30 Index", ["kse30index", "kse30"], tradingViewStockHeatmap={"dataset": "PSXKSE30"}),
		Parameter("dataset", "KSE 100 Index", ["kse100index", "kse100"], tradingViewStockHeatmap={"dataset": "PSXKSE100"}),
		Parameter("dataset", "KSE All Share Index", ["kseallshareindex", "kseallshare"], tradingViewStockHeatmap={"dataset": "PSXALLSHR"}),
		Parameter("dataset", "Meezan Pakistan Index", ["meezanpakistanindex", "meezanpakistan"], tradingViewStockHeatmap={"dataset": "PSXMZNPI"}),
		Parameter("dataset", "NBP Pakistan Growth Index", ["nbppakistangrowthindex", "nbppakistangrowth"], tradingViewStockHeatmap={"dataset": "PSXNBPPGI"}),
		Parameter("dataset", "NIT Pakistan Gateway Index", ["nitpakistangatewayindex", "nitpakistangateway"], tradingViewStockHeatmap={"dataset": "PSXNITPGI"}),
		Parameter("dataset", "Oil & Gas Tradable Index", ["oil&gastradableindex", "oil&gastradable"], tradingViewStockHeatmap={"dataset": "PSXOGTI"}),
		Parameter("dataset", "UBL Pakistan Enterprise Index", ["ublpakistanenterpriseindex", "ublpakistanenterprise"], tradingViewStockHeatmap={"dataset": "PSXUPP9"}),
		Parameter("dataset", "All Pakistani companies", ["allpakistanicompanies", "allpakistanicompanies"], tradingViewStockHeatmap={"dataset": "AllPK"}),
		Parameter("dataset", "S&P / BVL Peru General Index (PEN)", ["s&p/bvlperugeneralindex(pen)", "s&p/bvlperugeneralindex(pen)"], tradingViewStockHeatmap={"dataset": "BVLSPBLPGPT"}),
		Parameter("dataset", "All Peruvian companies", ["allperuviancompanies", "allperuviancompanies"], tradingViewStockHeatmap={"dataset": "AllPE"}),
		Parameter("dataset", "All Philippine companies", ["allphilippinecompanies", "allphilippinecompanies"], tradingViewStockHeatmap={"dataset": "AllPH"}),
		Parameter("dataset", "WIG20 Index", ["wig20index", "wig20"], tradingViewStockHeatmap={"dataset": "GPWWIG20"}),
		Parameter("dataset", "All Polish companies", ["allpolishcompanies", "allpolishcompanies"], tradingViewStockHeatmap={"dataset": "AllPO"}),
		Parameter("dataset", "PSI", ["psi", "psi"], tradingViewStockHeatmap={"dataset": "EURONEXTPSI20"}),
		Parameter("dataset", "All Portuguese companies", ["allportuguesecompanies", "allportuguesecompanies"], tradingViewStockHeatmap={"dataset": "AllPRT"}),
		Parameter("dataset", "QE Index", ["qeindex", "qe"], tradingViewStockHeatmap={"dataset": "QSEGNRI"}),
		Parameter("dataset", "All Qatar companies", ["allqatarcompanies", "allqatarcompanies"], tradingViewStockHeatmap={"dataset": "AllQA"}),
		Parameter("dataset", "Bucharest Exchange Trading", ["bucharestexchangetrading", "bucharestexchangetrading"], tradingViewStockHeatmap={"dataset": "BVBBET"}),
		Parameter("dataset", "All Romanian companies", ["allromaniancompanies", "allromaniancompanies"], tradingViewStockHeatmap={"dataset": "AllRO"}),
		Parameter("dataset", "MOEX Russia Index", ["moexrussiaindex", "moex", "moexrussia"], tradingViewStockHeatmap={"dataset": "MOEXRUSSIA"}),
		Parameter("dataset", "MOEX BROAD MARKET (RUB)", ["moexbroadmarket(rub)", "moexrub", "moexbroad"], tradingViewStockHeatmap={"dataset": "MOEXBROAD"}),
		Parameter("dataset", "MOEX SMID", ["moexsmid"], tradingViewStockHeatmap={"dataset": "MOEXSMID"}),
		Parameter("dataset", "RTS Index", ["rtsindex", "rts"], tradingViewStockHeatmap={"dataset": "RTS"}),
		Parameter("dataset", "RTS BROAD MARKET", ["rtsbroadmarket", "rtsbroad"], tradingViewStockHeatmap={"dataset": "RTSBROAD"}),
		Parameter("dataset", "All Russian companies", ["allrussiancompanies", "ru", "allru", "russiancompanies"], tradingViewStockHeatmap={"dataset": "AllRU"}),
		Parameter("dataset", "Banks Index", ["banksindex", "banks"], tradingViewStockHeatmap={"dataset": "TADAWULTBNI"}),
		Parameter("dataset", "Capital Goods Index", ["capitalgoodsindex", "capitalgoods"], tradingViewStockHeatmap={"dataset": "TADAWULTCGI"}),
		Parameter("dataset", "Consumer Durables & Apparel Index", ["consumerdurables&apparelindex", "consumerdurables&apparel"], tradingViewStockHeatmap={"dataset": "TADAWULTDAI"}),
		Parameter("dataset", "Energy Index", ["energyindex", "energy"], tradingViewStockHeatmap={"dataset": "TADAWULTENI"}),
		Parameter("dataset", "Food & Beverages Index", ["food&beveragesindex", "food&beverages"], tradingViewStockHeatmap={"dataset": "TADAWULTFBI"}),
		Parameter("dataset", "Health Care Equipment & SVC Index", ["healthcareequipment&svcindex", "healthcareequipment&svc"], tradingViewStockHeatmap={"dataset": "TADAWULTHEI"}),
		Parameter("dataset", "Insurance Index", ["insuranceindex", "insurance"], tradingViewStockHeatmap={"dataset": "TADAWULTISI"}),
		Parameter("dataset", "Materials Index", ["materialsindex", "materials"], tradingViewStockHeatmap={"dataset": "TADAWULTMTI"}),
		Parameter("dataset", "Real Estate MGMT & Dev't Index", ["realestatemgmt&dev'tindex", "realestatemgmt&dev't"], tradingViewStockHeatmap={"dataset": "TADAWULTRMI"}),
		Parameter("dataset", "Retailing Index", ["retailingindex", "retailing"], tradingViewStockHeatmap={"dataset": "TADAWULTRLI"}),
		Parameter("dataset", "Tadawul All Shares Index", ["tadawulallsharesindex", "tadawulallshares"], tradingViewStockHeatmap={"dataset": "TADAWULTASI"}),
		Parameter("dataset", "Telecommunication SVC Index", ["telecommunicationsvcindex", "telecommunicationsvc"], tradingViewStockHeatmap={"dataset": "TADAWULTTSI"}),
		Parameter("dataset", "All Saudi Arabian companies", ["allsaudiarabiancompanies", "allsaudiarabiancompanies"], tradingViewStockHeatmap={"dataset": "AllSA"}),
		Parameter("dataset", "All Serbian companies", ["allserbiancompanies", "allserbiancompanies"], tradingViewStockHeatmap={"dataset": "AllRS"}),
		Parameter("dataset", "Straits Times Index", ["straitstimesindex", "straitstimes"], tradingViewStockHeatmap={"dataset": "TVCSTI"}),
		Parameter("dataset", "All Singapore companies", ["allsingaporecompanies", "allsingaporecompanies"], tradingViewStockHeatmap={"dataset": "AllSGP"}),
		Parameter("dataset", "South Africa Top 40 Index", ["southafricatop40index", "southafricatop40"], tradingViewStockHeatmap={"dataset": "SA40"}),
		Parameter("dataset", "All South African companies", ["allsouthafricancompanies", "allsouthafricancompanies"], tradingViewStockHeatmap={"dataset": "AllZA"}),
		Parameter("dataset", "All South Korean companies", ["allsouthkoreancompanies", "allsouthkoreancompanies"], tradingViewStockHeatmap={"dataset": "AllKR"}),
		Parameter("dataset", "IBEX 35 Index", ["ibex35index", "ibex35"], tradingViewStockHeatmap={"dataset": "IBEX35"}),
		Parameter("dataset", "IBEX Small Cap", ["ibexsmallcap", "ibexsmallcap"], tradingViewStockHeatmap={"dataset": "BMEIS"}),
		Parameter("dataset", "IBEX Medium Cap", ["ibexmediumcap", "ibexmediumcap"], tradingViewStockHeatmap={"dataset": "BMEICC"}),
		Parameter("dataset", "IBEX Growth Market 15", ["ibexgrowthmarket15", "ibexgrowthmarket15"], tradingViewStockHeatmap={"dataset": "BMEINDGRO15"}),
		Parameter("dataset", "IBEX Growth Market All Share", ["ibexgrowthmarketallshare", "ibexgrowthmarketallshare"], tradingViewStockHeatmap={"dataset": "BMEINDGROAS"}),
		Parameter("dataset", "All Spanish companies", ["allspanishcompanies", "es", "alles", "spanishcompanies"], tradingViewStockHeatmap={"dataset": "AllES"}),
		Parameter("dataset", "OMX Stockholm 30 Index", ["omxstockholm30index", "omxstockholm30"], tradingViewStockHeatmap={"dataset": "OMXS30"}),
		Parameter("dataset", "All Swedish companies", ["allswedishcompanies", "allswedishcompanies"], tradingViewStockHeatmap={"dataset": "AllSWE"}),
		Parameter("dataset", "Swiss Market Index", ["swissmarketindex", "swissmarket"], tradingViewStockHeatmap={"dataset": "SIXSMI"}),
		Parameter("dataset", "All Swiss companies", ["allswisscompanies", "allswisscompanies"], tradingViewStockHeatmap={"dataset": "AllCHE"}),
		Parameter("dataset", "GRETAI 50 INDEX", ["gretai50index", "gretai50"], tradingViewStockHeatmap={"dataset": "GTSM50"}),
		Parameter("dataset", "TWSE TAIWAN 50 INDEX", ["twsetaiwan50index", "twsetaiwan50"], tradingViewStockHeatmap={"dataset": "TW50"}),
		Parameter("dataset", "All Taiwan companies", ["alltaiwancompanies", "alltaiwancompanies"], tradingViewStockHeatmap={"dataset": "AllTW"}),
		Parameter("dataset", "SET100 INDEX", ["set100index", "set100"], tradingViewStockHeatmap={"dataset": "SET100"}),
		Parameter("dataset", "All Thai companies", ["allthaicompanies", "allthaicompanies"], tradingViewStockHeatmap={"dataset": "AllTH"}),
		Parameter("dataset", "BIST 100 Index", ["bist100index", "bist100"], tradingViewStockHeatmap={"dataset": "BIST100"}),
		Parameter("dataset", "BIST TUM", ["bisttum", "bisttum"], tradingViewStockHeatmap={"dataset": "BISTTUM"}),
		Parameter("dataset", "All Turkish companies", ["allturkishcompanies", "tr", "alltr", "turkishcompanies"], tradingViewStockHeatmap={"dataset": "ALLTR"}),
		Parameter("dataset", "FTSE ADX 15 Index", ["ftseadx15index", "ftseadx15"], tradingViewStockHeatmap={"dataset": "ADXFADX15"}),
		Parameter("dataset", "DFM Index", ["dfmindex", "dfm"], tradingViewStockHeatmap={"dataset": "DFMDFMGI"}),
		Parameter("dataset", "All UAE companies", ["alluaecompanies", "alluaecompanies"], tradingViewStockHeatmap={"dataset": "AllARE"}),
		Parameter("dataset", "UK 100 Index", ["uk100index", "uk100"], tradingViewStockHeatmap={"dataset": "UK100"}),
		Parameter("dataset", "All UK companies", ["allukcompanies", "uk", "alluk", "ukcompanies"], tradingViewStockHeatmap={"dataset": "AllUK"}),
		Parameter("dataset", "All Vietnamese companies", ["allvietnamesecompanies", "allvietnamesecompanies"], tradingViewStockHeatmap={"dataset": "AllVN"}),
		Parameter("dataset", "Crypto in USD (excluding Bitcoin)", ["cryptoinusd(excludingbitcoin)"], tradingViewCryptoHeatmap={"dataset": "CryptoWithoutBTC"}),
		Parameter("dataset", "Crypto in BTC", ["cryptoinbtc"], tradingViewCryptoHeatmap={"dataset": "CryptoInBTC"}),
		Parameter("dataset", "Crypto DeFi", ["cryptodefi"], tradingViewCryptoHeatmap={"dataset": "CryptoDeFi"}),
		Parameter("dataset", "Crypto in USD", ["full", "all", "every", "everything", "cryptoinusd"], tradingViewCryptoHeatmap={"dataset": "Crypto"}),
		Parameter("theme", "Light theme", ["light", "white"], tradingViewStockHeatmap={"theme": "light"}, tradingViewCryptoHeatmap={"theme": "light"}),
		Parameter("theme", "Dark theme", ["dark", "black"], tradingViewStockHeatmap={"theme": "dark"}, tradingViewCryptoHeatmap={"theme": "dark"}),
	],
	"preferences": [
		Parameter("size", "Market cap", ["marketcap", "mcap"], tradingViewStockHeatmap="&size=market_cap_basic", tradingViewCryptoHeatmap="&size=market_cap_calc"),
		Parameter("size", "Traded volume", ["tradedvolume", "volume"], tradingViewCryptoHeatmap="&size=total_value_traded"),
		Parameter("size", "Number of employees", ["numberofemployees", "employees"], tradingViewStockHeatmap="&size=number_of_employees"),
		Parameter("size", "Dividend yield", ["dividendyield", "dividendyield"], tradingViewStockHeatmap="&size=dividend_yield_recent"),
		Parameter("size", "Price to earnings ratio (TTM)", ["pricetoearningsratio(ttm)", "pricetoearningsratio", "pricetoearnings"], tradingViewStockHeatmap="&size=price_earnings_ttm"),
		Parameter("size", "Price to sales (FY)", ["pricetosales(fy)", "pricetosales"], tradingViewStockHeatmap="&size=price_sales_ratio"),
		Parameter("size", "Price to book (FY)", ["pricetobook(fy)", "pricetobook"], tradingViewStockHeatmap="&size=price_book_ratio"),
		Parameter("size", "Price to book (MRQ)", ["pricetoboo(mrq)", "mrq"], tradingViewStockHeatmap="&size=price_book_fq"),
		Parameter("group", "No group", ["nogroup"], tradingViewStockHeatmap="&group=no_group", tradingViewCryptoHeatmap="&group=no_group"),
		Parameter("group", "Sector", ["sector"], tradingViewStockHeatmap="&group=sector"),
		Parameter("category", "Commercial services", ["commercialservices"], tradingViewStockHeatmap="&activeGroup=Commercial%20Services"),
		Parameter("category", "Communications", ["communications"], tradingViewStockHeatmap="&activeGroup=Communications"),
		Parameter("category", "Consumer durables", ["consumerdurables"], tradingViewStockHeatmap="&activeGroup=Consumer%20Durables"),
		Parameter("category", "Consumer non-durables", ["consumernon-durables"], tradingViewStockHeatmap="&activeGroup=Consumer%20Non-Durables"),
		Parameter("category", "Consumer services", ["consumerservices"], tradingViewStockHeatmap="&activeGroup=Consumer%20Services"),
		Parameter("category", "Distribution services", ["distributionservices"], tradingViewStockHeatmap="&activeGroup=Distribution%20Services"),
		Parameter("category", "Electronic technology", ["electronictechnology"], tradingViewStockHeatmap="&activeGroup=Electronic%20Technology"),
		Parameter("category", "Energy minerals", ["energyminerals"], tradingViewStockHeatmap="&activeGroup=Energy%20Minerals"),
		Parameter("category", "Finance", ["finance", "financialservices"], tradingViewStockHeatmap="&activeGroup=Finance"),
		Parameter("category", "Health services", ["healthservices"], tradingViewStockHeatmap="&activeGroup=Health%20Services"),
		Parameter("category", "Health technology", ["health", "healthtechnology", "healthcare"], tradingViewStockHeatmap="&activeGroup=Health%20Technology"),
		Parameter("category", "Industrial services", ["industrialservices"], tradingViewStockHeatmap="&activeGroup=Industrial%20Services"),
		Parameter("category", "Miscellaneous", ["miscellaneous"], tradingViewStockHeatmap="&activeGroup=Miscellaneous"),
		Parameter("category", "Non-energy minerals", ["non-energyminerals"], tradingViewStockHeatmap="&activeGroup=Non-Energy%20Minerals"),
		Parameter("category", "Process industries", ["processindustries"], tradingViewStockHeatmap="&activeGroup=Process%20Industries"),
		Parameter("category", "Producer manufacturing", ["producermanufacturing"], tradingViewStockHeatmap="&activeGroup=Producer%20Manufacturing"),
		Parameter("category", "Retail trade", ["retailtrade"], tradingViewStockHeatmap="&activeGroup=Retail%20Trade"),
		Parameter("category", "Technology services", ["technologyservices"], tradingViewStockHeatmap="&activeGroup=Technology%20Services"),
		Parameter("category", "Transportation", ["transportation"], tradingViewStockHeatmap="&activeGroup=Transportation"),
		Parameter("category", "Utilities", ["utilities"], tradingViewStockHeatmap="&activeGroup=Utilities"),
		Parameter("forcePlatform", "stocks heatmap", ["stocks"], tradingViewStockHeatmap=True),
		Parameter("forcePlatform", "crypto heatmap", ["crypto"], tradingViewCryptoHeatmap=True),
	]
}
DEFAULTS = {
	"TradingView Stock Heatmap": {
		"timeframes": [
			AbstractRequest.find_parameter_by_id(1440, PARAMETERS, "TradingView Stock Heatmap", parameterType="timeframes")
		],
		"style": [
			AbstractRequest.find_parameter_by_id("theme", PARAMETERS, "TradingView Stock Heatmap", name="Dark theme", parameterType="style"),
			AbstractRequest.find_parameter_by_id("dataset", PARAMETERS, "TradingView Stock Heatmap", name="S&P 500 Index", parameterType="style")
		],
		"preferences": []
	},
	"TradingView Crypto Heatmap": {
		"timeframes": [
			AbstractRequest.find_parameter_by_id(1440, PARAMETERS, "TradingView Crypto Heatmap", parameterType="timeframes")
		],
		"style": [
			AbstractRequest.find_parameter_by_id("theme", PARAMETERS, "TradingView Crypto Heatmap", name="Dark theme", parameterType="style"),
			AbstractRequest.find_parameter_by_id("dataset", PARAMETERS, "TradingView Crypto Heatmap", name="Crypto in USD", parameterType="style")
		],
		"preferences": []
	}
}


class HeatmapRequestHandler(AbstractRequestHandler):
	def __init__(self, platforms):
		super().__init__(platforms, None)
		for platform in platforms:
			self.requests[platform] = HeatmapRequest(platform)

	async def process_ticker(self): raise NotImplementedError

	def set_defaults(self):
		for platform, request in self.requests.items():
			if request.errorIsFatal: continue
			for parameterType in PARAMETERS:
				request.set_default_for(parameterType)

	async def find_caveats(self):
		for platform, request in self.requests.items():
			if request.errorIsFatal: continue

			styles = request.prepare_styles()
			preferences = request.prepare_preferences()

			if platform == "TradingView Stock Heatmap":
				size = preferences.get("size")
				group = preferences.get("group")

				theme = styles.get("theme")
				_type = styles.get("dataset")

				if size is None:
					request.preferences.append(AbstractRequest.find_parameter_by_id("size", PARAMETERS, platform, name="Market cap", parameterType="preferences"))
				if group is None:
					request.preferences.append(AbstractRequest.find_parameter_by_id("group", PARAMETERS, platform, name="Sector", parameterType="preferences"))

				if theme is None:
					request.styles.append(AbstractRequest.find_parameter_by_id("theme", PARAMETERS, platform, name="Dark theme", parameterType="style"))
				if _type is None:
					request.styles.append(AbstractRequest.find_parameter_by_id("dataset", PARAMETERS, platform, name="S&P 500 Index", parameterType="style"))
			elif platform == "TradingView Crypto Heatmap":
				size = preferences.get("size")
				group = preferences.get("group")

				theme = styles.get("theme")
				_type = styles.get("dataset")

				if size is None:
					request.preferences.append(AbstractRequest.find_parameter_by_id("size", PARAMETERS, platform, name="Market cap", parameterType="preferences"))
				if group is None:
					request.preferences.append(AbstractRequest.find_parameter_by_id("group", PARAMETERS, platform, name="No group", parameterType="preferences"))

				if theme is None:
					request.styles.append(AbstractRequest.find_parameter_by_id("theme", PARAMETERS, platform, name="Dark theme", parameterType="style"))
				if _type is None:
					request.styles.append(AbstractRequest.find_parameter_by_id("dataset", PARAMETERS, platform, name="Crypto in USD", parameterType="style"))

	def to_dict(self):
		d = {
			"platforms": self.platforms,
			"currentPlatform": self.currentPlatform
		}

		timeframes = []

		for platform in self.platforms:
			request = self.requests[platform].to_dict()
			timeframes.append(request.get("timeframes"))
			d[platform] = request

		d["timeframes"] = {p: t for p, t in zip(self.platforms, timeframes)}
		d["requestCount"] = len(d["timeframes"].get(d.get("currentPlatform"), []))

		return d


class HeatmapRequest(AbstractRequest):
	def __init__(self, platform):
		super().__init__(platform)

		self.timeframes = []
		self.styles = []
		self.preferences = []

		self.currentTimeframe = None

	async def process_argument(self, argument):
		# None None - No successeful parse
		# None True - Successful parse and add
		# "" False - Successful parse and error
		# None False - Successful parse and breaking error

		finalOutput = None

		responseMessage, success = await self.add_timeframe(argument)
		if responseMessage is not None: finalOutput = responseMessage
		elif success: return

		responseMessage, success = await self.add_style(argument)
		if responseMessage is not None: finalOutput = responseMessage
		elif success: return

		responseMessage, success = await self.add_preferences(argument)
		if responseMessage is not None: finalOutput = responseMessage
		elif success: return

		if finalOutput is None:
			self.set_error(f"`{argument[:229]}` is not a valid argument.", isFatal=True)
		elif finalOutput.startswith("`Stocks Heatmap") or finalOutput.startswith("`Crypto Heatmap"):
			self.set_error(None, isFatal=True)
		else:
			self.set_error(finalOutput)

	def add_parameter(self, argument, type):
		isSupported = None
		parsedParameter = None
		requiresPro = None
		for param in PARAMETERS[type]:
			if argument in param.parsablePhrases:
				parsedParameter = param
				isSupported = param.supports(self.platform)
				if isSupported: break
		return isSupported, parsedParameter, requiresPro

	# async def add_timeframe(self, argument) -- inherited

	async def add_exchange(self, argument): raise NotImplementedError

	# async def add_style(self, argument) -- inherited

	# async def add_preferences(self, argument) -- inherited

	def set_default_for(self, t):
		if t == "timeframes" and len(self.timeframes) == 0:
			for parameter in DEFAULTS.get(self.platform, {}).get(t, []):
				if not self.has_parameter(parameter.id, self.timeframes): self.timeframes.append(parameter)
		elif t == "style":
			for parameter in DEFAULTS.get(self.platform, {}).get(t, []):
				if not self.has_parameter(parameter.id, self.styles): self.styles.append(parameter)
		elif t == "preferences":
			for parameter in DEFAULTS.get(self.platform, {}).get(t, []):
				if not self.has_parameter(parameter.id, self.preferences): self.preferences.append(parameter)


	def to_dict(self):
		d = {
			"timeframes": [e.parsed[self.platform] for e in self.timeframes],
			"styles": self.prepare_styles(),
			"preferences": self.prepare_preferences(),
			"currentTimeframe": self.currentTimeframe
		}
		return d