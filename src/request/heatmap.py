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
		Parameter(60, "1-hour performance", ["1-hourperformance", "60", "60m", "60min", "60mins", "60minute", "60minutes", "1", "1h", "1hr", "1hour", "1hours", "hourly", "hour", "hr", "h"], tradingViewStockHeatmap="change|60", tradingViewCryptoHeatmap="change|60"),
		Parameter(120, "2-hour performance", ["2-hourperformance", "120", "120m", "120min", "120mins", "120minute", "120minutes", "2", "2h", "2hr", "2hrs", "2hour", "2hours"]),
		Parameter(180, "3-hour performance", ["3-hourperformance", "180", "180m", "180min", "180mins", "180minute", "180minutes", "3", "3h", "3hr", "3hrs", "3hour", "3hours"]),
		Parameter(240, "4-hour performance", ["4-hourperformance", "240", "240m", "240min", "240mins", "240minute", "240minutes", "4", "4h", "4hr", "4hrs", "4hour", "4hours"], tradingViewStockHeatmap="change|240", tradingViewCryptoHeatmap="change|240"),
		Parameter(360, "6-hour performance", ["6-hourperformance", "360", "360m", "360min", "360mins", "360minute", "360minutes", "6", "6h", "6hr", "6hrs", "6hour", "6hours"]),
		Parameter(480, "8-hour performance", ["8-hourperformance", "480", "480m", "480min", "480mins", "480minute", "480minutes", "8", "8h", "8hr", "8hrs", "8hour", "8hours"]),
		Parameter(720, "12-hour performance", ["12-hourperformance", "720", "720m", "720min", "720mins", "720minute", "720minutes", "12", "12h", "12hr", "12hrs", "12hour", "12hours"]),
		Parameter(1440, "1-day performance", ["1-dayperformance", "24", "24h", "24hr", "24hrs", "24hour", "24hours", "d", "day", "1", "1d", "1day", "daily", "1440", "1440m", "1440min", "1440mins", "1440minute", "1440minutes"], tradingViewStockHeatmap="change", tradingViewEtfHeatmap="change", tradingViewCryptoHeatmap="change"),
		Parameter(2880, "2-day performance", ["2-dayperformance", "48", "48h", "48hr", "48hrs", "48hour", "48hours", "2", "2d", "2day", "2880", "2880m", "2880min", "2880mins", "2880minute", "2880minutes"]),
		Parameter(3420, "3-day performance", ["3-dayperformance", "72", "72h", "72hr", "72hrs", "72hour", "72hours", "3", "3d", "3day", "3420", "3420m", "3420min", "3420mins", "3420minute", "3420minutes"]),
		Parameter(10080, "1-week performance", ["1-weekperformance", "7", "7d", "7day", "7days", "w", "week", "1w", "1week", "weekly"], tradingViewStockHeatmap="Perf.W", tradingViewEtfHeatmap="Perf.W", tradingViewCryptoHeatmap="Perf.W"),
		Parameter(20160, "2-week performance", ["2-weekperformance", "14", "14d", "14day", "14days", "2w", "2week"]),
		Parameter(43829, "1-month performance", ["1-monthperformance", "30d", "30day", "30days", "1", "1m", "m", "mo", "month", "1mo", "1month", "monthly"], tradingViewStockHeatmap="Perf.1M", tradingViewEtfHeatmap="Perf.1M", tradingViewCryptoHeatmap="Perf.1M"),
		Parameter(87658, "2-month performance", ["2-monthperformance", "2", "2m", "2m", "2mo", "2month", "2months"]),
		Parameter(131487, "3-month performance", ["3-monthperformance", "3", "3m", "3m", "3mo", "3month", "3months"], tradingViewStockHeatmap="Perf.3M", tradingViewEtfHeatmap="Perf.3M", tradingViewCryptoHeatmap="Perf.3M"),
		Parameter(175316, "4-month performance", ["4-monthperformance", "4", "4m", "4m", "4mo", "4month", "4months"]),
		Parameter(262974, "6-month performance", ["6-monthperformance", "6", "6m", "5m", "6mo", "6month", "6months"], tradingViewStockHeatmap="Perf.6M", tradingViewEtfHeatmap="Perf.6M", tradingViewCryptoHeatmap="Perf.6M"),
		Parameter(525949, "1-year performance", ["1-yearperformance", "12", "12m", "12mo", "12month", "12months", "year", "yearly", "1year", "1y", "y", "annual", "annually"], tradingViewStockHeatmap="Perf.Y", tradingViewEtfHeatmap="Perf.Y", tradingViewCryptoHeatmap="Perf.Y"),
		Parameter(1051898, "2-year performance", ["2-yearperformance", "24", "24m", "24mo", "24month", "24months", "2year", "2y"]),
		Parameter(1577847, "3-year performance", ["3-yearperformance", "36", "36m", "36mo", "36month", "36months", "3year", "3y"]),
		Parameter(2103796, "4-year performance", ["4-yearperformance", "48", "48m", "48mo", "48month", "48months", "4year", "4y"]),
		Parameter("color", "YTD performance", ["ytdperformance", "ytd"], tradingViewStockHeatmap="Perf.YTD", tradingViewCryptoHeatmap="Perf.YTD"),
		Parameter("color", "pre-market change", ["pre-marketchange", "premarketchange", "premarketperformance"], tradingViewStockHeatmap="premarket_change"),
		Parameter("color", "post-market change", ["post-marketchange", "postmarketchange", "postmarketperformance"], tradingViewStockHeatmap="postmarket_change"),
		Parameter("color", "10-day relative volume", ["10-dayrelativevolume", "relativevolume", "volume"], tradingViewStockHeatmap="relative_volume_10d_calc"),
		Parameter("color", "gap", ["gap"], tradingViewStockHeatmap="gap", tradingViewCryptoHeatmap="gap"),
		Parameter("color", "1-day volatility", ["1-dayvolatility", "volatility", "vol", "v"], tradingViewStockHeatmap="Volatility.D", tradingViewCryptoHeatmap="Volatility.D"),
		Parameter("color", "1-month volatility", ["1-monthvolatility", "monthlyvolatility", "mvol", "mv"], tradingViewEtfHeatmap="Volatility.M"),
		Parameter("color", "1-month NAV total return", ["1-monthnavtotalreturn", "1-monthnav"], tradingViewEtfHeatmap="nav_total_return.1M"),
		Parameter("color", "3-month NAV total return", ["3-monthnavtotalreturn", "3-monthnav"], tradingViewEtfHeatmap="nav_total_return.3M"),
		Parameter("color", "YTD NAV total return", ["ytdnavtotalreturn", "ytdnav"], tradingViewEtfHeatmap="nav_total_return.YTD"),
		Parameter("color", "1-year NAV total return", ["1-yearnavtotalreturn", "1-yearnav"], tradingViewEtfHeatmap="nav_total_return.1Y"),
		Parameter("color", "3-year NAV total return", ["3-yearnavtotalreturn", "3-yearnav"], tradingViewEtfHeatmap="nav_total_return.3Y"),
		Parameter("color", "5-year NAV total return", ["5-yearnavtotalreturn", "5-yearnav"], tradingViewEtfHeatmap="nav_total_return.5Y"),
		Parameter("color", "weight in top (10)", ["weightintop(10)"], tradingViewEtfHeatmap="weight_top_10"),
		Parameter("color", "weight in top (25)", ["weightintop(25)"], tradingViewEtfHeatmap="weight_top_25"),
		Parameter("color", "beta 1Y", ["beta1Y"], tradingViewEtfHeatmap="beta_1_year"),
		Parameter("color", "beta 3Y", ["beta3Y"], tradingViewEtfHeatmap="beta_3_year"),
		Parameter("color", "beta 5Y", ["beta5Y"], tradingViewEtfHeatmap="beta_5_year"),
	],
	"style": [
		Parameter("dataset", "Nasdaq 100 Index", ["nasdaq100index", "nasdaq", "nasdaq100"], tradingViewStockHeatmap="NASDAQ100"),
		Parameter("dataset", "Nasdaq Composite Index", ["nasdaqcompositeindex", "nasdaqcomposite"], tradingViewStockHeatmap="NASDAQCOMPOSITE"),
		Parameter("dataset", "Dow Jones Composite Average Index", ["dowjonescompositeaverageindex", "dji", "dowjones", "dowjonescompositeaverage", "djca"], tradingViewStockHeatmap="DJCA"),
		Parameter("dataset", "Dow Jones Industrial Average Index", ["dowjonesindustrialaverageindex", "dowjonesindustrialaverage"], tradingViewStockHeatmap="DJDJI"),
		Parameter("dataset", "Dow Jones Transportation Average Index", ["dowjonestransportationaverageindex", "dowjonestransportationaverage"], tradingViewStockHeatmap="DJDJT"),
		Parameter("dataset", "Dow Jones Utility Average Index", ["dowjonesutilityaverageindex", "dowjonesutilityaverage"], tradingViewStockHeatmap="DJDJU"),
		Parameter("dataset", "KBW Nasdaq Bank Index", ["kbwnasdaqbankindex", "kbwnasdaqbank"], tradingViewStockHeatmap="NASDAQBKX"),
		Parameter("dataset", "Mini Russell 2000 Index", ["minirussell2000index", "minirussell2000"], tradingViewStockHeatmap="CBOEFTSEMRUT"),
		Parameter("dataset", "Russell 1000", ["russell1000", "russell1000"], tradingViewStockHeatmap="TVCRUI"),
		Parameter("dataset", "Russell 2000", ["russell2000", "russell2000"], tradingViewStockHeatmap="TVCRUT"),
		Parameter("dataset", "Russell 3000", ["russell3000", "russell3000"], tradingViewStockHeatmap="TVCRUA"),
		Parameter("dataset", "S&P 500 Index", ["s&p500index", "s&p500", "s&p", "sp500", "sap500", "sap", "spx", "spx500"], tradingViewStockHeatmap="SPX500"),
		Parameter("dataset", "all US companies", ["alluscompanies", "us", "usa", "uscompanies", "allusa"], tradingViewStockHeatmap="AllUSA"),
		Parameter("dataset", "MERVAL Index", ["mervalindex", "merval"], tradingViewStockHeatmap="BCBAIMV"),
		Parameter("dataset", "all Argentinean companies", ["allargentineancompanies", "allargentineancompanies"], tradingViewStockHeatmap="AllAR"),
		Parameter("dataset", "S&P/ASX 200 Index", ["s&p/asx200index", "s&p/asx200", "asx200", "asx", "spasx", "sapasx", "sp200", "sap200"], tradingViewStockHeatmap="ASX200"),
		Parameter("dataset", "all Australian companies", ["allaustraliancompanies", "australiancompanies", "au", "allau"], tradingViewStockHeatmap="AllAU"),
		Parameter("dataset", "BEL 20 Index", ["bel20index", "bel20"], tradingViewStockHeatmap="BEL20"),
		Parameter("dataset", "all Belgian companies", ["allbelgiancompanies", "belgiancompanies", "be", "allbe"], tradingViewStockHeatmap="AllBE"),
		Parameter("dataset", "IBovespa Index", ["ibovespaindex", "ibovespa"], tradingViewStockHeatmap="IBOV"),
		Parameter("dataset", "IBRX 50 Index", ["ibrx50index", "ibrx50"], tradingViewStockHeatmap="IBXL"),
		Parameter("dataset", "all Brazilian companies", ["allbraziliancompanies", "allbraziliancompanies"], tradingViewStockHeatmap="AllBR"),
		Parameter("dataset", "S&P/TSX Composite Index", ["s&p/tsxcompositeindex", "s&p/tsxcomposite"], tradingViewStockHeatmap="TSX"),
		Parameter("dataset", "all Canadian companies", ["allcanadiancompanies", "allcanadiancompanies"], tradingViewStockHeatmap="AllCA"),
		Parameter("dataset", "S&P IPSA", ["s&pipsa", "s&pipsa"], tradingViewStockHeatmap="BCSSPIPSA"),
		Parameter("dataset", "all Chilean companies", ["allchileancompanies", "allchileancompanies"], tradingViewStockHeatmap="AllCL"),
		Parameter("dataset", "SZSE Component Index", ["szsecomponentindex", "szsecomponent", "shenzhencomponentindex", "sci", "szse399001", "szse"], tradingViewStockHeatmap="SZSE399001"),
		Parameter("dataset", "all Chinese companies", ["allchinesecompanies", "chinesecompanies", "cn", "allcn"], tradingViewStockHeatmap="AllCN"),
		Parameter("dataset", "INDICE DE CAPITALIZACION BURSATIL", ["indicedecapitalizacionbursatil", "indicedecapitalizacionbursatil"], tradingViewStockHeatmap="BVCICAP"),
		Parameter("dataset", "all Colombian companies", ["allcolombiancompanies", "allcolombiancompanies"], tradingViewStockHeatmap="AllCO"),
		Parameter("dataset", "Alternative Market Index CSE", ["alternativemarketindexcse", "alternativemarketindexcse"], tradingViewStockHeatmap="CSECYALTE"),
		Parameter("dataset", "Main Market Index CSE", ["mainmarketindexcse", "mainmarketindexcse"], tradingViewStockHeatmap="CSECYMAIN"),
		Parameter("dataset", "General Index CSE", ["generalindexcse", "generalindexcse"], tradingViewStockHeatmap="CSECYGEN"),
		Parameter("dataset", "Investment Market Index CSE", ["investmentmarketindexcse", "investmentmarketindexcse"], tradingViewStockHeatmap="CSECYINVE"),
		Parameter("dataset", "Hotel Index CSE", ["hotelindexcse", "hotelindexcse"], tradingViewStockHeatmap="CSECYHOTEL"),
		Parameter("dataset", "FTSE/CYSE 20", ["ftse/cyse20", "ftse/cyse20"], tradingViewStockHeatmap="CSECYFTSE20"),
		Parameter("dataset", "all Cyprus companies", ["allcypruscompanies", "allcypruscompanies"], tradingViewStockHeatmap="AllCY"),
		Parameter("dataset", "OMX Copenhagen 25 Index", ["omxcopenhagen25index", "omxcopenhagen25"], tradingViewStockHeatmap="OMXCOPOMXC25"),
		Parameter("dataset", "all Danish companies", ["alldanishcompanies", "alldanishcompanies"], tradingViewStockHeatmap="AllDK"),
		Parameter("dataset", "EGX 30 Price Return Index", ["egx30pricereturnindex", "egx30pricereturn"], tradingViewStockHeatmap="EGXEGX30"),
		Parameter("dataset", "all Egyptian companies", ["allegyptiancompanies", "allegyptiancompanies"], tradingViewStockHeatmap="AllEG"),
		Parameter("dataset", "OMX Tallinn GI", ["omxtallinngi", "omxtallinngi"], tradingViewStockHeatmap="OMXTSEOMXTGI"),
		Parameter("dataset", "all Estonian companies", ["allestoniancompanies", "allestoniancompanies"], tradingViewStockHeatmap="AllEE"),
		Parameter("dataset", "Euro Stoxx 50 Index", ["eurostoxx50index", "eurostoxx50", "stoxx50", "sx5e"], tradingViewStockHeatmap="SX5E"),
		Parameter("dataset", "STOXX 600", ["stoxx600", "sxxp"], tradingViewStockHeatmap="SXXP"),
		Parameter("dataset", "all European Union companies", ["alleuropeanunioncompanies", "europeanunioncompanies", "eu", "alleu"], tradingViewStockHeatmap="AllEUN"),
		Parameter("dataset", "all European companies", ["alleuropeancompanies", "europeancompanies"], tradingViewStockHeatmap="AllEU"),
		Parameter("dataset", "OMX Helsinki 25 Index", ["omxhelsinki25index", "omxhelsinki25", "omx", "helsinki", "helsinki25"], tradingViewStockHeatmap="HELSINKI25"),
		Parameter("dataset", "all Finnish companies", ["allfinnishcompanies", "fi", "allfi", "finnishcompanies"], tradingViewStockHeatmap="AllFI"),
		Parameter("dataset", "CAC 40 Index", ["cac40index", "cac40", "cac"], tradingViewStockHeatmap="CAC40"),
		Parameter("dataset", "all French companies", ["allfrenchcompanies", "fr", "allfr", "frenchcompanies"], tradingViewStockHeatmap="AllFR"),
		Parameter("dataset", "DAX Index", ["daxindex", "dax"], tradingViewStockHeatmap="DAX"),
		Parameter("dataset", "MDAX Performance", ["mdax", "mdaxperformance"], tradingViewStockHeatmap="MDAX"),
		Parameter("dataset", "SDAX Performance", ["sdax", "sdaxperformance"], tradingViewStockHeatmap="SDAX"),
		Parameter("dataset", "TECDAX TR", ["tecdax", "tecdaxtr"], tradingViewStockHeatmap="TECDAX"),
		Parameter("dataset", "all German companies", ["allgermancompanies", "de", "allde", "germancompanies"], tradingViewStockHeatmap="AllDE"),
		Parameter("dataset", "Composite Index", ["compositeindex", "composite"], tradingViewStockHeatmap="ATHEXGD"),
		Parameter("dataset", "FTSE/ATHEX Market Index", ["ftse/athexmarketindex", "ftse/athexmarket"], tradingViewStockHeatmap="ATHEXFTSEA"),
		Parameter("dataset", "FTSE/ATHEX Mid Cap Index", ["ftse/athexmidcapindex", "ftse/athexmidcap"], tradingViewStockHeatmap="ATHEXFTSEM"),
		Parameter("dataset", "FTSE/ATHEX Large Cap Index", ["ftse/athexlargecapindex", "ftse/athexlargecap"], tradingViewStockHeatmap="ATHEXFTSE"),
		Parameter("dataset", "FTSE/ATHEX Mid & Small Cap Factor-Weighted Index", ["ftse/athexmid&smallcapfactor-weightedindex", "ftse/athexmid&smallcapfactor-weighted"], tradingViewStockHeatmap="ATHEXFTSEMSFW"),
		Parameter("dataset", "FTSE/ATHEX Global Traders Index Plus", ["ftse/athexglobaltradersindexplus", "ftse/athexglobaltradersindexplus"], tradingViewStockHeatmap="ATHEXFTSEGTI"),
		Parameter("dataset", "all Greek companies", ["allgreekcompanies", "allgreekcompanies"], tradingViewStockHeatmap="AllGRC"),
		Parameter("dataset", "Hang Seng Index", ["hangsengindex", "hangseng"], tradingViewStockHeatmap="HSI"),
		Parameter("dataset", "all Hong Kong companies", ["allhongkongcompanies", "allhongkongcompanies"], tradingViewStockHeatmap="AllHK"),
		Parameter("dataset", "Budapest Stock Index", ["budapeststockindex", "budapeststock"], tradingViewStockHeatmap="BETBUX"),
		Parameter("dataset", "all Hungarian companies", ["allhungariancompanies", "allhungariancompanies"], tradingViewStockHeatmap="AllHU"),
		Parameter("dataset", "OMX Iceland 10", ["omxiceland10", "omxiceland10"], tradingViewStockHeatmap="OMXICEOMXI10"),
		Parameter("dataset", "all Icelandic companies", ["allicelandiccompanies", "allicelandiccompanies"], tradingViewStockHeatmap="AllIS"),
		Parameter("dataset", "Nifty 50 Index", ["nifty50index", "nifty50", "nifty"], tradingViewStockHeatmap="NIFTY50"),
		Parameter("dataset", "S&P BSE Sensex Index", ["s&pbsesensexindex", "s&pbsesensex", "sensex"], tradingViewStockHeatmap="SENSEX"),
		Parameter("dataset", "all Indian companies", ["allindiancompanies", "in", "allin", "indiancompanies"], tradingViewStockHeatmap="AllIN"),
		Parameter("dataset", "IDX30 INDEX", ["idx30index", "idx30"], tradingViewStockHeatmap="IDX30"),
		Parameter("dataset", "all Indonesian companies", ["allindonesiancompanies", "allindonesiancompanies"], tradingViewStockHeatmap="AllID"),
		Parameter("dataset", "TA-35 Index", ["ta-35index", "ta-35"], tradingViewStockHeatmap="TA35"),
		Parameter("dataset", "TA-125", ["ta-125", "ta-125"], tradingViewStockHeatmap="TA125"),
		Parameter("dataset", "all Israeli companies", ["allisraelicompanies", "allisraelicompanies"], tradingViewStockHeatmap="AllIL"),
		Parameter("dataset", "FTSE MIB INDEX", ["ftsemib", "ftsemibindex", "ftse"], tradingViewStockHeatmap="FTSEMIB"),
		Parameter("dataset", "all Italian companies", ["allitaliancompanies", "it", "allit", "italiancompanies"], tradingViewStockHeatmap="AllIT"),
		Parameter("dataset", "Nikkei 225 Index", ["nikkei225index", "nikkei225"], tradingViewStockHeatmap="NI225"),
		Parameter("dataset", "all Japanese companies", ["alljapanesecompanies", "alljapanesecompanies"], tradingViewStockHeatmap="AllJP"),
		Parameter("dataset", "All-Share Index (PR)", ["all-shareindex(pr)", "all-shareindex(pr)"], tradingViewStockHeatmap="KSEBKA"),
		Parameter("dataset", "All-Share Index (TR)", ["all-shareindex(tr)", "all-shareindex(tr)"], tradingViewStockHeatmap="KSEBKAT"),
		Parameter("dataset", "Boursa Kuwait Main Market 50 Index", ["boursakuwaitmainmarket50index", "boursakuwaitmainmarket50"], tradingViewStockHeatmap="KSEBKM50"),
		Parameter("dataset", "Main Market Index (PR)", ["mainmarketindex(pr)", "mainmarketindex(pr)"], tradingViewStockHeatmap="KSEBKM"),
		Parameter("dataset", "Main Market Index (TR)", ["mainmarketindex(tr)", "mainmarketindex(tr)"], tradingViewStockHeatmap="KSEBKMT"),
		Parameter("dataset", "Premier Market Index (PR)", ["premiermarketindex(pr)", "premiermarketindex(pr)"], tradingViewStockHeatmap="KSEBKP"),
		Parameter("dataset", "Premier Market Index (TR)", ["premiermarketindex(tr)", "premiermarketindex(tr)"], tradingViewStockHeatmap="KSEBKPT"),
		Parameter("dataset", "all Kuwaiti companies", ["allkuwaiticompanies", "allkuwaiticompanies"], tradingViewStockHeatmap="AllKW"),
		Parameter("dataset", "OMX Riga GI", ["omxrigagi", "omxrigagi"], tradingViewStockHeatmap="OMXRSEOMXRGI"),
		Parameter("dataset", "all Latvian companies", ["alllatviancompanies", "alllatviancompanies"], tradingViewStockHeatmap="AllLV"),
		Parameter("dataset", "OMX Vilnius GI", ["omxvilniusgi", "omxvilniusgi"], tradingViewStockHeatmap="OMXVSEOMXVGI"),
		Parameter("dataset", "all Lithuanian companies", ["alllithuaniancompanies", "alllithuaniancompanies"], tradingViewStockHeatmap="AllLT"),
		Parameter("dataset", "all Malaysian companies", ["allmalaysiancompanies", "my", "allmy", "malaysiancompanies"], tradingViewStockHeatmap="AllMY"),
		Parameter("dataset", "IPC Mexico Index", ["ipcmexicoindex", "ipcmexico"], tradingViewStockHeatmap="BMVME"),
		Parameter("dataset", "all Mexican companies", ["allmexicancompanies", "allmexicancompanies"], tradingViewStockHeatmap="AllMX"),
		Parameter("dataset", "all Moroccan companies", ["allmoroccancompanies", "allmoroccancompanies"], tradingViewStockHeatmap="AllMA"),
		Parameter("dataset", "AEX Index", ["aexindex", "aex"], tradingViewStockHeatmap="AEX"),
		Parameter("dataset", "all Dutch companies", ["alldutchcompanies", "alldutchcompanies"], tradingViewStockHeatmap="AllNL"),
		Parameter("dataset", "S&P / NZX 50 Index Gross", ["s&p/nzx50indexgross", "s&p/nzx50indexgross"], tradingViewStockHeatmap="NZXNZ50G"),
		Parameter("dataset", "all New Zealand companies", ["allnewzealandcompanies", "allnewzealandcompanies"], tradingViewStockHeatmap="AllNZ"),
		Parameter("dataset", "NGX 30 Index", ["ngx30index", "ngx30"], tradingViewStockHeatmap="NSENGNGX30"),
		Parameter("dataset", "all Nigerian companies", ["allnigeriancompanies", "allnigeriancompanies"], tradingViewStockHeatmap="AllNGA"),
		Parameter("dataset", "all Norwegian companies", ["allnorwegiancompanies", "allnorwegiancompanies"], tradingViewStockHeatmap="AllNO"),
		Parameter("dataset", "Banking Tradable Index", ["bankingtradableindex", "bankingtradable"], tradingViewStockHeatmap="PSXBKTI"),
		Parameter("dataset", "JS Momentum Factor Index", ["jsmomentumfactorindex", "jsmomentumfactor"], tradingViewStockHeatmap="PSXJSMFI"),
		Parameter("dataset", "KMI 30 Index", ["kmi30index", "kmi30"], tradingViewStockHeatmap="PSXKMI30"),
		Parameter("dataset", "KMI All Share Index", ["kmiallshareindex", "kmiallshare"], tradingViewStockHeatmap="PSXKMIALLSHR"),
		Parameter("dataset", "KSE 30 Index", ["kse30index", "kse30"], tradingViewStockHeatmap="PSXKSE30"),
		Parameter("dataset", "KSE 100 Index", ["kse100index", "kse100"], tradingViewStockHeatmap="PSXKSE100"),
		Parameter("dataset", "KSE All Share Index", ["kseallshareindex", "kseallshare"], tradingViewStockHeatmap="PSXALLSHR"),
		Parameter("dataset", "Meezan Pakistan Index", ["meezanpakistanindex", "meezanpakistan"], tradingViewStockHeatmap="PSXMZNPI"),
		Parameter("dataset", "NBP Pakistan Growth Index", ["nbppakistangrowthindex", "nbppakistangrowth"], tradingViewStockHeatmap="PSXNBPPGI"),
		Parameter("dataset", "NIT Pakistan Gateway Index", ["nitpakistangatewayindex", "nitpakistangateway"], tradingViewStockHeatmap="PSXNITPGI"),
		Parameter("dataset", "Oil & Gas Tradable Index", ["oil&gastradableindex", "oil&gastradable"], tradingViewStockHeatmap="PSXOGTI"),
		Parameter("dataset", "UBL Pakistan Enterprise Index", ["ublpakistanenterpriseindex", "ublpakistanenterprise"], tradingViewStockHeatmap="PSXUPP9"),
		Parameter("dataset", "all Pakistani companies", ["allpakistanicompanies", "allpakistanicompanies"], tradingViewStockHeatmap="AllPK"),
		Parameter("dataset", "S&P / BVL Peru General Index (PEN)", ["s&p/bvlperugeneralindex(pen)", "s&p/bvlperugeneralindex(pen)"], tradingViewStockHeatmap="BVLSPBLPGPT"),
		Parameter("dataset", "all Peruvian companies", ["allperuviancompanies", "allperuviancompanies"], tradingViewStockHeatmap="AllPE"),
		Parameter("dataset", "all Philippine companies", ["allphilippinecompanies", "allphilippinecompanies"], tradingViewStockHeatmap="AllPH"),
		Parameter("dataset", "WIG20 Index", ["wig20index", "wig20"], tradingViewStockHeatmap="GPWWIG20"),
		Parameter("dataset", "all Polish companies", ["allpolishcompanies", "allpolishcompanies"], tradingViewStockHeatmap="AllPO"),
		Parameter("dataset", "PSI", ["psi", "psi"], tradingViewStockHeatmap="EURONEXTPSI20"),
		Parameter("dataset", "all Portuguese companies", ["allportuguesecompanies", "allportuguesecompanies"], tradingViewStockHeatmap="AllPRT"),
		Parameter("dataset", "QE Index", ["qeindex", "qe"], tradingViewStockHeatmap="QSEGNRI"),
		Parameter("dataset", "all Qatar companies", ["allqatarcompanies", "allqatarcompanies"], tradingViewStockHeatmap="AllQA"),
		Parameter("dataset", "Bucharest Exchange Trading", ["bucharestexchangetrading", "bucharestexchangetrading"], tradingViewStockHeatmap="BVBBET"),
		Parameter("dataset", "all Romanian companies", ["allromaniancompanies", "allromaniancompanies"], tradingViewStockHeatmap="AllRO"),
		Parameter("dataset", "MOEX Russia Index", ["moexrussiaindex", "moex", "moexrussia"], tradingViewStockHeatmap="MOEXRUSSIA"),
		Parameter("dataset", "MOEX BROAD MARKET (RUB)", ["moexbroadmarket(rub)", "moexrub", "moexbroad"], tradingViewStockHeatmap="MOEXBROAD"),
		Parameter("dataset", "MOEX SMID", ["moexsmid"], tradingViewStockHeatmap="MOEXSMID"),
		Parameter("dataset", "RTS Index", ["rtsindex", "rts"], tradingViewStockHeatmap="RTS"),
		Parameter("dataset", "RTS BROAD MARKET", ["rtsbroadmarket", "rtsbroad"], tradingViewStockHeatmap="RTSBROAD"),
		Parameter("dataset", "all Russian companies", ["allrussiancompanies", "ru", "allru", "russiancompanies"], tradingViewStockHeatmap="AllRU"),
		Parameter("dataset", "Banks Index", ["banksindex", "banks"], tradingViewStockHeatmap="TADAWULTBNI"),
		Parameter("dataset", "Capital Goods Index", ["capitalgoodsindex", "capitalgoods"], tradingViewStockHeatmap="TADAWULTCGI"),
		Parameter("dataset", "Consumer Durables & Apparel Index", ["consumerdurables&apparelindex", "consumerdurables&apparel"], tradingViewStockHeatmap="TADAWULTDAI"),
		Parameter("dataset", "Energy Index", ["energyindex", "energy"], tradingViewStockHeatmap="TADAWULTENI"),
		Parameter("dataset", "Food & Beverages Index", ["food&beveragesindex", "food&beverages"], tradingViewStockHeatmap="TADAWULTFBI"),
		Parameter("dataset", "Health Care Equipment & SVC Index", ["healthcareequipment&svcindex", "healthcareequipment&svc"], tradingViewStockHeatmap="TADAWULTHEI"),
		Parameter("dataset", "Insurance Index", ["insuranceindex", "insurance"], tradingViewStockHeatmap="TADAWULTISI"),
		Parameter("dataset", "Materials Index", ["materialsindex", "materials"], tradingViewStockHeatmap="TADAWULTMTI"),
		Parameter("dataset", "Real Estate MGMT & Dev't Index", ["realestatemgmt&dev'tindex", "realestatemgmt&dev't"], tradingViewStockHeatmap="TADAWULTRMI"),
		Parameter("dataset", "Retailing Index", ["retailingindex", "retailing"], tradingViewStockHeatmap="TADAWULTRLI"),
		Parameter("dataset", "Tadawul All Shares Index", ["tadawulallsharesindex", "tadawulallshares"], tradingViewStockHeatmap="TADAWULTASI"),
		Parameter("dataset", "Telecommunication SVC Index", ["telecommunicationsvcindex", "telecommunicationsvc"], tradingViewStockHeatmap="TADAWULTTSI"),
		Parameter("dataset", "all Saudi Arabian companies", ["allsaudiarabiancompanies", "allsaudiarabiancompanies"], tradingViewStockHeatmap="AllSA"),
		Parameter("dataset", "all Serbian companies", ["allserbiancompanies", "allserbiancompanies"], tradingViewStockHeatmap="AllRS"),
		Parameter("dataset", "Straits Times Index", ["straitstimesindex", "straitstimes"], tradingViewStockHeatmap="TVCSTI"),
		Parameter("dataset", "all Singapore companies", ["allsingaporecompanies", "allsingaporecompanies"], tradingViewStockHeatmap="AllSGP"),
		Parameter("dataset", "South Africa Top 40 Index", ["southafricatop40index", "southafricatop40"], tradingViewStockHeatmap="SA40"),
		Parameter("dataset", "all South African companies", ["allsouthafricancompanies", "allsouthafricancompanies"], tradingViewStockHeatmap="AllZA"),
		Parameter("dataset", "all South Korean companies", ["allsouthkoreancompanies", "allsouthkoreancompanies"], tradingViewStockHeatmap="AllKR"),
		Parameter("dataset", "IBEX 35 Index", ["ibex35index", "ibex35"], tradingViewStockHeatmap="IBEX35"),
		Parameter("dataset", "IBEX Small Cap", ["ibexsmallcap", "ibexsmallcap"], tradingViewStockHeatmap="BMEIS"),
		Parameter("dataset", "IBEX Medium Cap", ["ibexmediumcap", "ibexmediumcap"], tradingViewStockHeatmap="BMEICC"),
		Parameter("dataset", "IBEX Growth Market 15", ["ibexgrowthmarket15", "ibexgrowthmarket15"], tradingViewStockHeatmap="BMEINDGRO15"),
		Parameter("dataset", "IBEX Growth Market All Share", ["ibexgrowthmarketallshare", "ibexgrowthmarketallshare"], tradingViewStockHeatmap="BMEINDGROAS"),
		Parameter("dataset", "all Spanish companies", ["allspanishcompanies", "es", "alles", "spanishcompanies"], tradingViewStockHeatmap="AllES"),
		Parameter("dataset", "OMX Stockholm 30 Index", ["omxstockholm30index", "omxstockholm30"], tradingViewStockHeatmap="OMXS30"),
		Parameter("dataset", "all Swedish companies", ["allswedishcompanies", "allswedishcompanies"], tradingViewStockHeatmap="AllSWE"),
		Parameter("dataset", "Swiss Market Index", ["swissmarketindex", "swissmarket"], tradingViewStockHeatmap="SIXSMI"),
		Parameter("dataset", "all Swiss companies", ["allswisscompanies", "allswisscompanies"], tradingViewStockHeatmap="AllCHE"),
		Parameter("dataset", "GRETAI 50 INDEX", ["gretai50index", "gretai50"], tradingViewStockHeatmap="GTSM50"),
		Parameter("dataset", "TWSE TAIWAN 50 INDEX", ["twsetaiwan50index", "twsetaiwan50"], tradingViewStockHeatmap="TW50"),
		Parameter("dataset", "all Taiwan companies", ["alltaiwancompanies", "alltaiwancompanies"], tradingViewStockHeatmap="AllTW"),
		Parameter("dataset", "SET100 INDEX", ["set100index", "set100"], tradingViewStockHeatmap="SET100"),
		Parameter("dataset", "all Thai companies", ["allthaicompanies", "allthaicompanies"], tradingViewStockHeatmap="AllTH"),
		Parameter("dataset", "BIST 100 Index", ["bist100index", "bist100"], tradingViewStockHeatmap="BIST100"),
		Parameter("dataset", "BIST TUM", ["bisttum", "bisttum"], tradingViewStockHeatmap="BISTTUM"),
		Parameter("dataset", "all Turkish companies", ["allturkishcompanies", "tr", "alltr", "turkishcompanies"], tradingViewStockHeatmap="ALLTR"),
		Parameter("dataset", "FTSE ADX 15 Index", ["ftseadx15index", "ftseadx15"], tradingViewStockHeatmap="ADXFADX15"),
		Parameter("dataset", "DFM Index", ["dfmindex", "dfm"], tradingViewStockHeatmap="DFMDFMGI"),
		Parameter("dataset", "all UAE companies", ["alluaecompanies", "alluaecompanies"], tradingViewStockHeatmap="AllARE"),
		Parameter("dataset", "UK 100 Index", ["uk100index", "uk100"], tradingViewStockHeatmap="UK100"),
		Parameter("dataset", "all UK companies", ["allukcompanies", "uk", "alluk", "ukcompanies"], tradingViewStockHeatmap="AllUK"),
		Parameter("dataset", "all Vietnamese companies", ["allvietnamesecompanies", "allvietnamesecompanies"], tradingViewStockHeatmap="AllVN"),
		Parameter("dataset", "crypto in USD (excluding Bitcoin)", ["cryptoinusd(excludingbitcoin)"], tradingViewCryptoHeatmap="CryptoWithoutBTC"),
		Parameter("dataset", "crypto in BTC", ["cryptoinbtc"], tradingViewCryptoHeatmap="CryptoInBTC"),
		Parameter("dataset", "crypto DeFi", ["cryptodefi"], tradingViewCryptoHeatmap="CryptoDeFi"),
		Parameter("dataset", "crypto in USD", ["full", "all", "every", "everything", "cryptoinusd"], tradingViewCryptoHeatmap="Crypto"),
		Parameter("dataset", "USA ETFs", ["usaetfs"], tradingViewEtfHeatmap="AllUSEtf"),
		Parameter("dataset", "Australia ETFs", ["australiaetfs"], tradingViewEtfHeatmap="AllAUEtf"),
		Parameter("dataset", "Canada ETFs", ["canadaetfs"], tradingViewEtfHeatmap="AllCAEtf"),
		Parameter("dataset", "France ETFs", ["franceetfs"], tradingViewEtfHeatmap="AllFREtf"),
		Parameter("dataset", "Germany ETFs", ["germanyetfs"], tradingViewEtfHeatmap="AllDEEtf"),
		Parameter("dataset", "Hong Kong ETFs", ["hongkongetfs"], tradingViewEtfHeatmap="AllHKEtf"),
		Parameter("dataset", "India ETFs", ["indiaetfs"], tradingViewEtfHeatmap="AllINEtf"),
		Parameter("dataset", "Israel ETFs", ["israeletfs"], tradingViewEtfHeatmap="AllILEtf"),
		Parameter("dataset", "Italy ETFs", ["italyetfs"], tradingViewEtfHeatmap="AllITEtf"),
		Parameter("dataset", "Japan ETFs", ["japanetfs"], tradingViewEtfHeatmap="AllJPEtf"),
		Parameter("dataset", "Luxembourg ETFs", ["luxembourgetfs"], tradingViewEtfHeatmap="AllLUEtf"),
		Parameter("dataset", "Malaysia ETFs", ["malaysiaetfs"], tradingViewEtfHeatmap="AllMYEtf"),
		Parameter("dataset", "Netherlands ETFs", ["netherlandsetfs"], tradingViewEtfHeatmap="AllNLEtf"),
		Parameter("dataset", "New Zealand ETFs", ["New zealandetfs"], tradingViewEtfHeatmap="AllNZEtf"),
		Parameter("dataset", "Romania ETFs", ["romaniaetfs"], tradingViewEtfHeatmap="AllROEtf"),
		Parameter("dataset", "Singapore ETFs", ["singaporeetfs"], tradingViewEtfHeatmap="AllSGPEtf"),
		Parameter("dataset", "Spain ETFs", ["spainetfs"], tradingViewEtfHeatmap="AllESEtf"),
		Parameter("dataset", "Switzerland ETFs", ["switzerlandetfs"], tradingViewEtfHeatmap="AllCHEEtf"),
		Parameter("dataset", "Taiwan ETFs", ["taiwanetfs"], tradingViewEtfHeatmap="AllTWEtf"),
		Parameter("dataset", "Thailand ETFs", ["thailandetfs"], tradingViewEtfHeatmap="AllTHEtf"),
		Parameter("dataset", "Turkey ETFs", ["turkeyetfs"], tradingViewEtfHeatmap="AllTREtf"),
		Parameter("dataset", "UAE ETFs", ["uaeetfs"], tradingViewEtfHeatmap="AllAREEtf"),
		Parameter("dataset", "UK ETFs", ["uketfs"], tradingViewEtfHeatmap="AllUKEtf"),
		Parameter("dataset", "Vietnam ETFs", ["vietnametfs"], tradingViewEtfHeatmap="AllVNEtf"),
		Parameter("theme", "light theme", ["light", "white"], tradingViewStockHeatmap="light", tradingViewEtfHeatmap="light", tradingViewCryptoHeatmap="light"),
		Parameter("theme", "dark theme", ["dark", "black"], tradingViewStockHeatmap="dark", tradingViewEtfHeatmap="dark", tradingViewCryptoHeatmap="dark"),
	],
	"preferences": [
		Parameter("size", "market cap", ["marketcap", "mcap"], tradingViewStockHeatmap="market_cap_basic", tradingViewCryptoHeatmap="market_cap_calc"),
		Parameter("size", "traded volume", ["tradedvolume", "volume"], tradingViewCryptoHeatmap="total_value_traded"),
		Parameter("size", "number of employees", ["numberofemployees", "employees"], tradingViewStockHeatmap="number_of_employees"),
		Parameter("size", "dividend yield", ["dividendyield", "dividendyield"], tradingViewStockHeatmap="dividend_yield_recent"),
		Parameter("size", "price to earnings ratio (TTM)", ["pricetoearningsratio(ttm)", "pricetoearningsratio", "pricetoearnings"], tradingViewStockHeatmap="price_earnings_ttm"),
		Parameter("size", "price to sales (FY)", ["pricetosales(fy)", "pricetosales"], tradingViewStockHeatmap="price_sales_ratio"),
		Parameter("size", "price to book (FY)", ["pricetobook(fy)", "pricetobook"], tradingViewStockHeatmap="price_book_ratio"),
		Parameter("size", "price to book (MRQ)", ["pricetoboo(mrq)", "mrq"], tradingViewStockHeatmap="price_book_fq"),
		Parameter("size", "AUM", ["aum"], tradingViewEtfHeatmap="aum"),
		Parameter("size", "volume 1h", ["volume1h"], tradingViewStockHeatmap="volume|60", tradingViewEtfHeatmap="volume|60"),
		Parameter("size", "volume 4h", ["volume4h"], tradingViewStockHeatmap="volume|240", tradingViewEtfHeatmap="volume|240"),
		Parameter("size", "volume D", ["volumed"], tradingViewStockHeatmap="volume", tradingViewEtfHeatmap="volume"),
		Parameter("size", "volume W", ["volumew"], tradingViewStockHeatmap="volume|1W", tradingViewEtfHeatmap="volume|1W"),
		Parameter("size", "volume M", ["volumem"], tradingViewStockHeatmap="volume|1M", tradingViewEtfHeatmap="volume|1M"),
		Parameter("size", "volume*price 1h", ["volume*price1h"], tradingViewStockHeatmap="Volume.Traded|60", tradingViewEtfHeatmap="Volume.Traded|60"),
		Parameter("size", "volume*price 4h", ["volume*price4h"], tradingViewStockHeatmap="Volume.Traded|240", tradingViewEtfHeatmap="Volume.Traded|240"),
		Parameter("size", "volume*price 1D", ["volume*price1d"], tradingViewStockHeatmap="Volume.Traded", tradingViewEtfHeatmap="Volume.Traded"),
		Parameter("size", "volume*price 1W", ["volume*price1w"], tradingViewStockHeatmap="Volume.Traded|1W", tradingViewEtfHeatmap="Volume.Traded|1W"),
		Parameter("size", "volume*price 1M", ["volume*price1m"], tradingViewStockHeatmap="Volume.Traded|1M", tradingViewEtfHeatmap="Volume.Traded|1M"),
		Parameter("size", "dividend yield FWD %", ["dividendyieldfwd%"], tradingViewEtfHeatmap="dividends_yield"),
		Parameter("group", "no group", ["nogroup"], tradingViewStockHeatmap="no_group", tradingViewEtfHeatmap="no_group", tradingViewCryptoHeatmap="no_group"),
		Parameter("group", "sector", ["sector"], tradingViewStockHeatmap="sector"),
		Parameter("group", "asset class", ["sector"], tradingViewEtfHeatmap="asset_class"),
		Parameter("category", "commercial services", ["commercialservices"], tradingViewStockHeatmap="Commercial Services"),
		Parameter("category", "communications", ["communications"], tradingViewStockHeatmap="Communications"),
		Parameter("category", "consumer durables", ["consumerdurables"], tradingViewStockHeatmap="Consumer Durables"),
		Parameter("category", "consumer non-durables", ["consumernon-durables"], tradingViewStockHeatmap="Consumer Non-Durables"),
		Parameter("category", "consumer services", ["consumerservices"], tradingViewStockHeatmap="Consumer Services"),
		Parameter("category", "distribution services", ["distributionservices"], tradingViewStockHeatmap="Distribution Services"),
		Parameter("category", "electronic technology", ["electronictechnology"], tradingViewStockHeatmap="Electronic Technology"),
		Parameter("category", "energy minerals", ["energyminerals"], tradingViewStockHeatmap="Energy Minerals"),
		Parameter("category", "finance", ["finance", "financialservices"], tradingViewStockHeatmap="Finance"),
		Parameter("category", "health services", ["healthservices"], tradingViewStockHeatmap="Health Services"),
		Parameter("category", "health technology", ["health", "healthtechnology", "healthcare"], tradingViewStockHeatmap="Health Technology"),
		Parameter("category", "industrial services", ["industrialservices"], tradingViewStockHeatmap="Industrial Services"),
		Parameter("category", "miscellaneous", ["miscellaneous"], tradingViewStockHeatmap="Miscellaneous"),
		Parameter("category", "non-energy minerals", ["non-energyminerals"], tradingViewStockHeatmap="Non-Energy Minerals"),
		Parameter("category", "process industries", ["processindustries"], tradingViewStockHeatmap="Process Industries"),
		Parameter("category", "producer manufacturing", ["producermanufacturing"], tradingViewStockHeatmap="Producer Manufacturing"),
		Parameter("category", "retail trade", ["retailtrade"], tradingViewStockHeatmap="Retail Trade"),
		Parameter("category", "technology services", ["technologyservices"], tradingViewStockHeatmap="Technology Services"),
		Parameter("category", "transportation", ["transportation"], tradingViewStockHeatmap="Transportation"),
		Parameter("category", "utilities", ["utilities"], tradingViewStockHeatmap="Utilities"),
		Parameter("category", "equity", ["equity"], tradingViewEtfHeatmap="c05f85d35d1cd0be6ebb2af4be16e06a"),
		Parameter("category", "fixed income", ["fixed income"], tradingViewEtfHeatmap="b6e443a6c4a8a2e7918c5dbf3d45c796"),
		Parameter("category", "currency", ["currency"], tradingViewEtfHeatmap="1af0389838508d7016a9841eb6273962"),
		Parameter("category", "alternatives", ["alternatives"], tradingViewEtfHeatmap="4071518f1736a5a43dae51b47590322f"),
		Parameter("category", "commodities", ["commodities"], tradingViewEtfHeatmap="8fe80395f389e29e3ea42210337f0350"),
		Parameter("category", "asset allocation", ["asset allocation"], tradingViewEtfHeatmap="b090e99b8d95f5837ec178c2d3d3fc50"),
		Parameter("forcePlatform", "stocks heatmap", ["stocks"], tradingViewStockHeatmap=True),
		Parameter("forcePlatform", "crypto heatmap", ["crypto"], tradingViewCryptoHeatmap=True),
		Parameter("forcePlatform", "ETF heatmap", ["etf"], tradingViewEtfHeatmap=True),
	]
}
DEFAULTS = {
	"TradingView Stock Heatmap": {
		"timeframes": [
			AbstractRequest.find_parameter_by_id(1440, PARAMETERS, "TradingView Stock Heatmap", parameterType="timeframes")
		],
		"style": [
			AbstractRequest.find_parameter_by_id("theme", PARAMETERS, "TradingView Stock Heatmap", name="dark theme", parameterType="style"),
			AbstractRequest.find_parameter_by_id("dataset", PARAMETERS, "TradingView Stock Heatmap", name="S&P 500 Index", parameterType="style")
		],
		"preferences": [
			AbstractRequest.find_parameter_by_id("group", PARAMETERS, "TradingView Stock Heatmap", name="sector", parameterType="preferences"),
			AbstractRequest.find_parameter_by_id("size", PARAMETERS, "TradingView Stock Heatmap", name="market cap", parameterType="preferences")
		]
	},
	"TradingView ETF Heatmap": {
		"timeframes": [
			AbstractRequest.find_parameter_by_id(1440, PARAMETERS, "TradingView ETF Heatmap", parameterType="timeframes")
		],
		"style": [
			AbstractRequest.find_parameter_by_id("theme", PARAMETERS, "TradingView ETF Heatmap", name="dark theme", parameterType="style"),
			AbstractRequest.find_parameter_by_id("dataset", PARAMETERS, "TradingView ETF Heatmap", name="USA ETFs", parameterType="style")
		],
		"preferences": [
			AbstractRequest.find_parameter_by_id("group", PARAMETERS, "TradingView ETF Heatmap", name="asset class", parameterType="preferences"),
			AbstractRequest.find_parameter_by_id("size", PARAMETERS, "TradingView ETF Heatmap", name="AUM", parameterType="preferences")
		]
	},
	"TradingView Crypto Heatmap": {
		"timeframes": [
			AbstractRequest.find_parameter_by_id(1440, PARAMETERS, "TradingView Crypto Heatmap", parameterType="timeframes")
		],
		"style": [
			AbstractRequest.find_parameter_by_id("theme", PARAMETERS, "TradingView Crypto Heatmap", name="dark theme", parameterType="style"),
			AbstractRequest.find_parameter_by_id("dataset", PARAMETERS, "TradingView Crypto Heatmap", name="crypto in USD", parameterType="style")
		],
		"preferences": [
			AbstractRequest.find_parameter_by_id("group", PARAMETERS, "TradingView Crypto Heatmap", name="no group", parameterType="preferences"),
			AbstractRequest.find_parameter_by_id("size", PARAMETERS, "TradingView Crypto Heatmap", name="market cap", parameterType="preferences")
		]
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
				pass

			elif platform == "TradingView ETF Heatmap":
				pass

			elif platform == "TradingView Crypto Heatmap":
				pass

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
		elif finalOutput.startswith("`Stocks Heatmap") or finalOutput.startswith("`ETF Heatmap") or finalOutput.startswith("`Crypto Heatmap"):
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