from sys import maxsize as MAXSIZE
from time import time
from re import search
from traceback import format_exc

from matching.instruments import match_ticker
from .parameter import ChartParameter as Parameter
from .abstract import AbstractRequestHandler, AbstractRequest


PARAMETERS = {
	"timeframes": [
		Parameter(1, "1-minute", ["1", "1m", "1min", "1mins", "1minute", "1-minute", "1minutes", "min", "m"], tradinglite="1", tradingview="1", premium="1", gocharting="1m"),
		Parameter(2, "2-minute", ["2", "2m", "2min", "2mins", "2minute", "2-minute", "2minutes"], premium="2"),
		Parameter(3, "3-minute", ["3", "3m", "3min", "3mins", "3minute", "3-minute", "3minutes"], tradinglite="3", tradingview="3", premium="3", gocharting="3m"),
		Parameter(4, "4-minute", ["4", "4m", "4min", "4mins", "4minute", "4-minute", "4minutes"], premium="4"),
		Parameter(5, "5-minute", ["5", "5m", "5min", "5mins", "5minute", "5-minute", "5minutes"], tradinglite="5", tradingview="5", premium="5", gocharting="5m"),
		Parameter(6, "6-minute", ["6", "6m", "6min", "6mins", "6minute", "6-minute", "6minutes"], premium="6"),
		Parameter(10, "10-minute", ["10", "10m", "10min", "10mins", "10minute", "10-minute", "10minutes"], bookmap="10m", premium="10"),
		Parameter(15, "15-minute", ["15", "15m", "15min", "15mins", "15minute", "15-minute", "15minutes"], tradinglite="15", tradingview="15", premium="15", gocharting="15m"),
		Parameter(20, "20-minute", ["20", "20m", "20min", "20mins", "20minute", "20-minute", "20minutes"], premium="20"),
		Parameter(30, "30-minute", ["30", "30m", "30min", "30mins", "30minute", "30-minute", "30minutes"], tradinglite="30", tradingview="30", premium="30", gocharting="30m"),
		Parameter(45, "45-minute", ["45", "45m", "45min", "45mins", "45minute", "45-minute", "45minutes"], tradingview="45", premium="45"),
		Parameter(60, "1-hour", ["60", "60m", "60min", "60mins", "60minute", "60-minute", "60minutes", "1", "1h", "1hr", "1hour", "1-hour", "1hours", "hourly", "hour", "hr", "h"], tradinglite="60", tradingview="60", premium="1H", bookmap="1h", gocharting="1h"),
		Parameter(120, "2-hour", ["120", "120m", "120min", "120mins", "120minute", "120-minute", "120minutes", "2", "2h", "2hr", "2hrs", "2hour", "2-hour", "2hours"], tradinglite="120", tradingview="120", premium="2H", gocharting="2h"),
		Parameter(180, "3-hour", ["180", "180m", "180min", "180mins", "180minute", "180-minute", "180minutes", "3", "3h", "3hr", "3hrs", "3hour", "3-hour", "3hours"], tradingview="180", premium="3H"),
		Parameter(240, "4-hour", ["240", "240m", "240min", "240mins", "240minute", "240-minute", "240minutes", "4", "4h", "4hr", "4hrs", "4hour", "4-hour", "4hours"], tradinglite="240", tradingview="240", premium="4H", gocharting="4h"),
		Parameter(360, "6-hour", ["360", "360m", "360min", "360mins", "360minute", "360-minute", "360minutes", "6", "6h", "6hr", "6hrs", "6hour", "6-hour", "6hours"], tradinglite="360", premium="6H"),
		Parameter(480, "8-hour", ["480", "480m", "480min", "480mins", "480minute", "480-minute", "480minutes", "8", "8h", "8hr", "8hrs", "8hour", "8-hour", "8hours"], tradinglite="480", premium="8H"),
		Parameter(720, "12-hour", ["720", "720m", "720min", "720mins", "720minute", "720-minute", "720minutes", "12", "12h", "12hr", "12hrs", "12hour", "12-hour", "12hours"], tradinglite="720", premium="12H", gocharting="12h"),
		Parameter(1440, "1-day", ["24", "24h", "24hr", "24hrs", "24hour", "24-hour", "24hours", "d", "day", "1", "1d", "1day", "1-day", "daily", "1440", "1440m", "1440min", "1440mins", "1440minute", "1440-minute", "1440minutes"], tradinglite="1440", tradingview="D", premium="1D", bookmap="1d", gocharting="1D", finviz="d", alternativeme="1D", cnnbusiness="1D"),
		Parameter(2880, "2-day", ["48", "48h", "48hr", "48hrs", "48hour", "48-hour", "48hours", "2", "2d", "2day", "2-day", "2880", "2880m", "2880min", "2880mins", "2880minute", "2880-minute", "2880minutes"], premium="2D", alternativeme="2D", cnnbusiness="2D"),
		Parameter(3420, "3-day", ["72", "72h", "72hr", "72hrs", "72hour", "72-hour", "72hours", "3", "3d", "3day", "3-day", "3420", "3420m", "3420min", "3420mins", "3420minute", "3420-minute", "3420minutes"], premium="3D", alternativeme="3D", cnnbusiness="3D"),
		Parameter(5760, "4-day", ["96", "96h", "96hr", "96hrs", "96hour", "96-hour", "96hours", "4", "4d", "4day", "4-day", "5760", "5760m", "5760min", "5760mins", "5760minute", "5760-minute", "5760minutes"], premium="4D", alternativeme="4D", cnnbusiness="4D"),
		Parameter(7200, "5-day", ["120", "120h", "120hr", "120hrs", "120hour", "120-hour", "120hours", "5", "5d", "5day", "5-day", "7200", "7200m", "7200min", "7200mins", "7200minute", "7200-minute", "7200minutes"], premium="5D", alternativeme="5D", cnnbusiness="5D"),
		Parameter(8640, "6-day", ["144", "144h", "144hr", "144hrs", "144hour", "144-hour", "144hours", "6", "6d", "6day", "6-day", "8640", "8640m", "8640min", "8640mins", "8640minute", "8640-minute", "8640minutes"], premium="6D", alternativeme="6D", cnnbusiness="6D"),
		Parameter(10080, "1-week", ["7", "7d", "7day", "7-day", "7days", "w", "week", "1w", "1-week", "1week", "weekly"], tradingview="W", premium="1W", bookmap="7d", gocharting="1W", finviz="w", alternativeme="1W", cnnbusiness="1W"),
		Parameter(20160, "2-week", ["14", "14d", "14day", "14-day", "14days", "2w", "2-week", "2week"], premium="2W", alternativeme="2W", cnnbusiness="2W"),
		Parameter(30240, "3-week", ["21", "21d", "21day", "21-day", "21days", "3w", "3-week", "3week"], premium="3W", alternativeme="3W", cnnbusiness="3W"),
		Parameter(43829, "1-month", ["30d", "30day", "30-day", "30days", "1", "1m", "m", "mo", "month", "1mo", "1month", "1-month", "monthly"], tradingview="M", premium="1M", bookmap="32d", gocharting="1M", finviz="m", alternativeme="1M", cnnbusiness="1M"),
		Parameter(87658, "2-month", ["2", "2m", "2m", "2mo", "2month", "2-month", "2months"], premium="2M"),
		Parameter(131487, "3-month", ["3", "3m", "3m", "3mo", "3month", "3-month", "3months"], premium="3M"),
		Parameter(175316, "4-month", ["4", "4m", "4m", "4mo", "4month", "4-month", "4months"], premium="4M"),
		Parameter(262974, "6-month", ["6", "6m", "5m", "6mo", "6month", "6-month", "6months"], premium="6M"),
		Parameter(525949, "1-year", ["12", "12m", "12mo", "12month", "12months", "year", "yearly", "1year", "1-year", "1y", "y", "annual", "annually"], premium="12M"),
	],
	"indicators": [
		Parameter("ab", "Abandoned Baby", ["ab", "abandonedbaby"], gocharting="ABANDONEDBABY"),
		Parameter("accd", "Accumulation/Distribution", ["accd", "ad", "acc", "accumulationdistribution", "accumulation/distribution"], tradingview="ACCD@tv-basicstudies", premium="Accumulation/Distribution", gocharting="ACC", dynamic={"GoCharting": [20]}),
		Parameter("accumulationswingindex", "Accumulation Swing Index", ["accumulationswingindex", "accsi", "asi"], premium="Accumulative+Swing+Index", gocharting="ACCSWINGINDEX"),
		Parameter("admi", "Average Directional Movement Index", ["admi", "adx", "averagedirectionalmovementindex", "averagedirectionalindex"], premium="Average+Directional+Index", gocharting="ADX", dynamic={"GoCharting": [20]}),
		Parameter("adr", "Advance/Decline Ratio", ["adr", "advance/declineratio"], tradingview="studyADR@tv-basicstudies", premium="Advance/Decline"),
		Parameter("alligator", "Alligator", ["alligator"], gocharting="ALLIGATOR"),
		Parameter("arnaudlegouxmovingaverage", "Arnaud Legoux Moving Average", ["alma", "arnaudlegouxmovingaverage"], premium="Arnaud+Legoux+Moving+Average"),
		Parameter("aroon", "Aroon", ["aroon"], tradingview="AROON@tv-basicstudies", premium="Aroon", gocharting="AROON", dynamic={"GoCharting": [20]}),
		Parameter("aroonoscillator", "Aroon Oscillator", ["aroonoscillator"], gocharting="AROONOSCILLATOR", dynamic={"GoCharting": [20]}),
		Parameter("atr", "ATR", ["atr"], tradingview="ATR@tv-basicstudies", premium="Average+True+Range", gocharting="ATR", dynamic={"GoCharting": [20]}),
		Parameter("atrb", "ATR Bands", ["atrb", "atrbands"], gocharting="ATRBAND", dynamic={"GoCharting": [14, 2]}),
		Parameter("atrts", "ATR Trailing Stop", ["trailingstop", "atrts", "atrstop", "atrs", "atrtrailingstop"], gocharting="ATRTRAILINGSTOP", dynamic={"GoCharting": [14, 2]}),
		Parameter("average", "Average Price", ["averageprice", "ap", "average"], premium="Average+Price"),
		Parameter("awesome", "Awesome Oscillator", ["awesome", "ao", "awesomeoscillator"], tradingview="AwesomeOscillator@tv-basicstudies", premium="Awesome+Oscillator", gocharting="AWESOMEOSCILLATOR", dynamic={"GoCharting": [20]}),
		Parameter("balanceofpower", "Balance of Power", ["balanceofpower", "bop"], premium="Balance+of+Power", gocharting="BOP", dynamic={"GoCharting": [20]}),
		Parameter("bearish", "All Bearish Candlestick Patterns", ["bear", "bearish", "bearishpatterns", "allbearishcandlestickpatterns"], gocharting="BEARISH"),
		Parameter("bearishengulfing", "Bearish Engulfing Pattern", ["bearishengulfing", "bearishengulfingpattern"], gocharting="BEARISHENGULFINGPATTERN"),
		Parameter("bearishhammer", "Bearish Hammer Pattern", ["bearishhammer", "bearishhammerpattern"], gocharting="BEARISHHAMMER"),
		Parameter("bearishharami", "Bearish Harami Pattern", ["bearishharami", "bearishharamipattern"], gocharting="BEARISHHARAMI"),
		Parameter("bearishharamicross", "Bearish Harami Cross Pattern", ["bearishharamicross", "bearishharamicrosspattern"], gocharting="BEARISHHARAMICROSS"),
		Parameter("bearishinvertedhammer", "Bearish Inverted Hammer Pattern", ["bearishinvertedhammer", "bearishinvertedhammerpattern"], gocharting="BEARISHINVERTEDHAMMER"),
		Parameter("bearishmarubozu", "Bearish Marubozu Pattern", ["bearishmarubozu", "bearishmarubozupattern"], gocharting="BEARISHMARUBOZU"),
		Parameter("bearishspinningtop", "Bearish Spinning Top Pattern", ["bearishspinningtop", "bearishspinningtoppattern"], gocharting="BEARISHSPINNINGTOP"),
		Parameter("bullish", "All Bullish Candlestick Patterns", ["bull", "bullish", "bullishpatterns", "allbullishcandlestickpatterns"], gocharting="BULLISH"),
		Parameter("bullishengulfing", "Bullish Engulfing Pattern", ["bullishengulfing", "bullishengulfingpattern"], gocharting="BULLISHENGULFINGPATTERN"),
		Parameter("bullishhammer", "Bullish Hammer Pattern", ["bullishhammer", "bullishhammerpattern"], gocharting="BULLISHHAMMER"),
		Parameter("bullishharami", "Bullish Harami Pattern", ["bullishharami", "bullishharamipattern"], gocharting="BULLISHHARAMI"),
		Parameter("bullishharamicross", "Bullish Harami Cross Pattern", ["bullishharamicross", "bullishharamicrosspattern"], gocharting="BULLISHHARAMICROSS"),
		Parameter("bullishinvertedhammer", "Bullish Inverted Hammer Pattern", ["bullishinvertedhammer", "bullishinvertedhammerpattern"], gocharting="BULLISHINVERTEDHAMMER"),
		Parameter("bullishmarubozu", "Bullish Marubozu Pattern", ["bullishmarubozu", "bullishmarubozupattern"], gocharting="BULLISHMARUBOZU"),
		Parameter("bullishspinningtop", "Bullish Spinning Top Pattern", ["bullishspinningtop", "bullishspinningtoppattern"], gocharting="BULLISHSPINNINGTOP"),
		Parameter("bollinger", "Bollinger Bands", ["bollinger", "bbands", "bb", "bollingerbands"], tradingview="BB@tv-basicstudies", premium="Bollinger+Bands", gocharting="BOLLINGERBAND", dynamic={"GoCharting": [14, 2]}),
		Parameter("bbb", "Bollinger Bands %B", ["%b", "bollingerbandsb", "bollingerbands%b", "bbb"], tradingview="BollingerBandsR@tv-basicstudies", premium="Bollinger+Bands+%B"),
		Parameter("width", "Bollinger Bands Width", ["width", "bbw", "bollingerbandswidth"], tradingview="BollingerBandsWidth@tv-basicstudies", premium="Bollinger+Bands+Width"),
		Parameter("cmf", "Chaikin Money Flow Index", ["cmf", "chaikinmoneyflow", "chaikinmoneyflowindex"], tradingview="CMF@tv-basicstudies", premium="Chaikin+Money+Flow", gocharting="CHAIKINMFI", dynamic={"GoCharting": [20]}),
		Parameter("chaikin", "Chaikin Oscillator", ["chaikin", "co", "chaikinoscillator"], tradingview="ChaikinOscillator@tv-basicstudies", premium="Chaikin+Oscillator"),
		Parameter("cv", "Chaikin Volatility", ["cv", "chaikinvolatility"], tradingview="Chaikin Volatility", gocharting="CHAIKINVOLATILITY"),
		Parameter("cf", "Chande Forecast", ["cf", "chandeforecast"], gocharting="CHANDEFORECAST", dynamic={"GoCharting": [20]}),
		Parameter("chande", "Chande Momentum Oscillator", ["chande", "cmo", "chandemomentumoscillator"], tradingview="chandeMO@tv-basicstudies", premium="Chande+Momentum+Oscillator", gocharting="CMO", dynamic={"GoCharting": [20]}),
		Parameter("choppiness", "Choppiness Index", ["choppiness", "ci", "choppinessindex"], tradingview="ChoppinessIndex@tv-basicstudies", premium="Choppiness+Index", gocharting="CHOPPINESS"),
		Parameter("chandekrollstop", "Chande Kroll Stop", ["chandekrollstop"], premium="Chande+Kroll+Stop"),
		Parameter("chopzone", "Chop Zone", ["chopzone"], premium="Chop+Zone"),
		Parameter("coppockcurve", "Coppock Curve", ["coppockcurve"], premium="Coppock+Curve"),
		Parameter("cci", "Commodity Channel Index", ["cci"], tradingview="CCI@tv-basicstudies", premium="Commodity+Channel+Index", gocharting="CCI", dynamic={"GoCharting": [14, 20, 80]}),
		Parameter("crsi", "Connors RSI", ["crsi"], tradingview="CRSI@tv-basicstudies", premium="Connors+RSI"),
		Parameter("cog", "Center of Gravity", ["cog", "centerofgravity"], gocharting="COG", dynamic={"GoCharting": [20]}),
		Parameter("coppock", "Coppock", ["coppock"], gocharting="COPPOCK"),
		Parameter("cumtick", "Cumulative Tick", ["cumtick", "cumulativetick"], gocharting="CUMTICK", dynamic={"GoCharting": [20]}),
		Parameter("correlation", "Correlation Coefficient", ["correlation", "cc", "correlationcoefficient"], tradingview="CorrelationCoefficient@tv-basicstudies", premium="Correlation+Coefficient"),
		Parameter("correlationlog", "Correlation - Log", ["correlationlog", "correlation-log", "correlationcoefficientlog", "cclog"], premium="Correlation+-+Log"),
		Parameter("darkcloudcoverpattern", "Dark Cloud Cover Pattern", ["darkcloudcover", "dccp", "darkcloudcoverpattern"], gocharting="DARKCLOUDCOVER"),
		Parameter("detrended", "Detrended Price Oscillator", ["detrended", "dpo", "detrendedpriceoscillator"], tradingview="DetrendedPriceOscillator@tv-basicstudies", premium="Detrended+Price+Oscillator", gocharting="DPO", dynamic={"GoCharting": [20]}),
		Parameter("disparityoscillator", "Disparity Oscillator", ["disparityoscillator"], gocharting="DISPARITY", dynamic={"GoCharting": [20]}),
		Parameter("donchainwidth", "Donchain Width", ["donchainwidth"], gocharting="DONCHIANWIDTH", dynamic={"GoCharting": [20]}),
		Parameter("dm", "Directional Movement", ["dm", "directionalmovement"], tradingview="DM@tv-basicstudies", premium="Directional+Movement"),
		Parameter("dojipattern", "Doji Pattern", ["doji", "dojipattern"], gocharting="DOJI"),
		Parameter("donch", "DONCH", ["donch", "donchainchannel"], tradingview="DONCH@tv-basicstudies", premium="Donchian+Channels", gocharting="DONCHIANCHANNEL", dynamic={"GoCharting": [14, 2]}),
		Parameter("downsidetasukigappattern", "Downside Tasuki Gap Pattern", ["downsidetasukigap", "dtgp", "downsidetasukigappattern"], gocharting="DOWNSIDETASUKIGAP"),
		Parameter("dema", "Double EMA", ["dema", "doubleema"], tradingview="DoubleEMA@tv-basicstudies", premium="Double+EMA", gocharting="DEMA", dynamic={"GoCharting": [20]}),
		Parameter("dragonflydojipattern", "Dragonfly Doji Pattern", ["dragonflydoji", "ddp", "dragonflydojipattern"], gocharting="DRAGONFLYDOJI"),
		Parameter("efi", "Elder's Force Index", ["efi"], tradingview="EFI@tv-basicstudies", premium="Elder's Force Index"),
		Parameter("ema", "EMA", ["ema"], tradingview="MAExp@tv-basicstudies", premium="Moving+Average+Exponential", gocharting="EMA", dynamic={"GoCharting": [20]}),
		Parameter("elderray", "Elder Ray", ["elderray"], gocharting="ELDERRAY"),
		Parameter("elliott", "Elliott Wave", ["elliott", "ew", "elliottwave"], tradingview="ElliottWave@tv-basicstudies"),
		Parameter("env", "Envelopes", ["env"], tradingview="ENV@tv-basicstudies", premium="Envelopes"),
		Parameter("eom", "Ease of Movement", ["eom", "easeofmovement"], tradingview="EaseOfMovement@tv-basicstudies", premium="Ease+of+Movement", gocharting="EOM", dynamic={"GoCharting": [20]}),
		Parameter("eveningdojistarpattern", "Evening Doji Star Pattern", ["eveningdojistar", "edsp", "eveningdojistarpattern"], gocharting="EVENINGDOJISTAR"),
		Parameter("eveningstarpattern", "Evening Star Pattern", ["eveningstar", "esp", "eveningstarpattern"], gocharting="EVENINGSTAR"),
		Parameter("fisher", "Fisher Transform", ["fisher", "ft", "fishertransform"], tradingview="FisherTransform@tv-basicstudies", premium="Fisher+Transform", gocharting="EHLERFISHERTRANSFORM", dynamic={"GoCharting": [20]}),
		Parameter("forceindex", "Force Index", ["forceindex"], gocharting="FORCEINDEX"),
		Parameter("fullstochasticoscillator", "Full Stochastic Oscillator", ["fso", "fullstochasticoscillator"], gocharting="FULLSTOCHASTICOSCILLATOR"),
		Parameter("gravestonedojipattern", "Gravestone Doji Pattern", ["gravestonedoji", "gd", "gravestonedojipattern"], gocharting="GRAVESTONEDOJI"),
		Parameter("gatoroscillator", "Gator Oscillator", ["gatoroscillator", "gatoro"], gocharting="GATOROSCILLATOR"),
		Parameter("gopalakrishnanrangeindex", "Gopalakrishnan Range Index", ["gopalakrishnanrangeindex", "gri", "gapo"], gocharting="GAPO", dynamic={"GoCharting": [20]}),
		Parameter("guppy", "Guppy Moving Average", ["guppy", "gma", "rainbow", "rma", "guppymovingaverage"], premium="Guppy+Multiple+Moving+Average", gocharting="GUPPY", dynamic={"GoCharting": [20]}),
		Parameter("guppyoscillator", "Guppy Oscillator", ["guppyoscillator", "guppyo", "rainbowoscillator", "rainbowo"], gocharting="GUPPYOSCILLATOR"),
		Parameter("hangmanpattern", "Hangman Pattern", ["hangman", "hangingman", "hangmanpattern"], gocharting="HANGINGMAN"),
		Parameter("hhv", "Highest High Volume", ["highesthighvolume", "hhv"], gocharting="HHV", dynamic={"GoCharting": [20]}),
		Parameter("hml", "High Minus Low", ["highminuslow", "hml"], gocharting="HIGHMINUSLOW"),
		Parameter("hv", "Historical Volatility", ["historicalvolatility", "hv"], tradingview="HV@tv-basicstudies", premium="Historical+Volatility", gocharting="HISTVOLATILITY"),
		Parameter("hull", "Hull MA", ["hull", "hma", "hullma"], tradingview="hullMA@tv-basicstudies", premium="Hull+Moving+Average", gocharting="HULL"),
		Parameter("ichimoku", "Ichimoku Cloud", ["ichimoku", "cloud", "ichi", "ic", "ichimokucloud"], tradingview="IchimokuCloud@tv-basicstudies", premium="Ichimoku+Cloud", gocharting="ICHIMOKU"),
		Parameter("imi", "Intraday Momentum Index", ["intradaymomentumindex", "imi", "intradaymi"], gocharting="INTRADAYMI", dynamic={"GoCharting": [20]}),
		Parameter("keltner", "Keltner Channel", ["keltner", "kltnr", "keltnerchannel"], tradingview="KLTNR@tv-basicstudies", premium="Keltner+Channels", gocharting="KELTNERCHANNEL", dynamic={"GoCharting": [14, 2]}),
		Parameter("klinger", "Klinger", ["klinger"], premium="Klinger+Oscillator", gocharting="KLINGER"),
		Parameter("kst", "Know Sure Thing", ["knowsurething", "kst"], tradingview="KST@tv-basicstudies", premium="Know+Sure+Thing", gocharting="KST"),
		Parameter("llv", "Lowest Low Volume", ["llv", "lowestlowvolume"], gocharting="LLV", dynamic={"GoCharting": [20]}),
		Parameter("leastsquaresmovingaverage", "Least Squares Moving Average", ["leastsquaresmovingaverage"], premium="Least+Squares+Moving+Average"),
		Parameter("regression", "Linear Regression Channel", ["regression", "regressionchannel", "lr", "lrc", "linreg", "linearregression", "linearregressionchannel"], tradingview="LinearRegression@tv-basicstudies"),
		Parameter("regressionslope", "Linear Regression Slope", ["regressionslope", "lrs", "linregs", "linearregressionslope"], premium="Linear+Regression+Slope"),
		Parameter("regressioncurve", "Linear Regression Curve", ["regressioncurve", "lrc", "linregc", "linearregressioncurve"], premium="Linear+Regression+Curve"),
		Parameter("mawithemacross", "MA with EMA Cross", ["mawithemacross"], premium="MA+with+EMA+Cross"),
		Parameter("mcginleydynamic", "McGinley Dynamic", ["mcginleydynamic"], premium="McGinley+Dynamic"),
		Parameter("majorityrule", "Majority Rule", ["majorityrule"], premium="Majority+Rule"),
		Parameter("macd", "MACD", ["macd"], tradingview="MACD@tv-basicstudies", premium="MACD", gocharting="MACD"),
		Parameter("massindex", "Mass Index", ["massindex", "mi"], premium="Mass+Index", gocharting="MASSINDEX"),
		Parameter("medianprice", "Median Price", ["medianprice", "mp"], gocharting="MP", dynamic={"GoCharting": [20]}),
		Parameter("mom", "Momentum", ["mom", "momentum"], tradingview="MOM@tv-basicstudies", premium="Momentum", gocharting="MOMENTUMINDICATOR", dynamic={"GoCharting": [20]}),
		Parameter("morningdojistarpattern", "Morning Doji Star Pattern", ["morningdojistar", "mds", "morningdojistarpattern"], gocharting="MORNINGDOJISTAR"),
		Parameter("morningstarpattern", "Morning Star Pattern", ["morningstar", "ms", "morningstarpattern"], gocharting="MORNINGSTAR"),
		Parameter("mf", "Money Flow Index", ["mf", "mfi", "moneyflow"], tradingview="MF@tv-basicstudies", premium="Money+Flow+Index", gocharting="MONEYFLOWINDEX", dynamic={"GoCharting": [14, 20, 80]}),
		Parameter("moon", "Moon Phases", ["moon", "moonphases"], tradingview="MoonPhases@tv-basicstudies", gocharting="MOONPHASE"),
		Parameter("ma", "Moving Average", ["ma", "movingaverage"], tradingview="MASimple@tv-basicstudies", premium="Moving+Average", gocharting="SMA", dynamic={"GoCharting": [20]}),
		Parameter("macross", "MA Cross", ["macross"], premium="MA+Cross"),
		Parameter("emacross", "EMA Cross", ["emacross"], premium="EMA+Cross"),
		Parameter("medianprice", "Median Price", ["medianprice"], premium="Median+Price"),
		Parameter("movingaveragechannel", "Moving Average Channel", ["movingaveragechannel"], premium="Moving+Average+Channel"),
		Parameter("movingaveragedouble", "Moving Average Double", ["movingaveragedouble"], premium="Moving+Average+Double"),
		Parameter("movingaverageadaptive", "Moving Average Adaptive", ["movingaverageadaptive"], premium="Moving+Average+Adaptive"),
		Parameter("movingaveragehamming", "Moving Average Hamming", ["movingaveragehamming"], premium="Moving+Average+Hamming"),
		Parameter("movingaveragemultiple", "Moving Average Multiple", ["movingaveragemultiple"], premium="Moving+Average+Multiple"),
		Parameter("sma", "Smoothed Moving Average", ["sma", "smoothedmovingaverage"], premium="Smoothed+Moving+Average"),
		Parameter("maenvelope", "Moving Average Envelope", ["maenvelope", "mae", "movingaverageenvelope"], gocharting="MAENVELOPE", dynamic={"GoCharting": [14, 2]}),
		Parameter("nvi", "Negative Volume Index", ["nvi", "negvolindex", "negativevolumeindex"], gocharting="NEGVOLINDEX"),
		Parameter("obv", "On Balance Volume", ["obv", "onbalancevolume"], tradingview="OBV@tv-basicstudies", premium="On+Balance+Volume", gocharting="ONBALANCEVOLUME", dynamic={"GoCharting": [20]}),
		Parameter("parabolic", "Parabolic SAR", ["parabolic", "sar", "psar", "parabolicsar"], tradingview="PSAR@tv-basicstudies", premium="Parabolic+SAR", gocharting="SAR"),
		Parameter("performanceindex", "Performance Index", ["performanceindex", "pi"], gocharting="PERFORMANCEINDEX"),
		Parameter("pgo", "Pretty Good Oscillator", ["prettygoodoscillator", "pgo"], gocharting="PRETTYGOODOSCILLATOR", dynamic={"GoCharting": [20]}),
		Parameter("piercinglinepattern", "Piercing Line Pattern", ["piercingline", "pl", "piercinglinepattern"], gocharting="PIERCINGLINE"),
		Parameter("pmo", "Price Momentum Oscillator", ["pmo", "pricemomentum", "pricemomentumoscillator"], gocharting="PMO"),
		Parameter("po", "Price Oscillator", ["po", "priceoscillator"], tradingview="PriceOsc@tv-basicstudies", premium="Price+Oscillator", gocharting="PRICEOSCILLATOR"),
		Parameter("pphl", "Pivot Points High Low", ["pphl", "pivotpointshighlow"], tradingview="PivotPointsHighLow@tv-basicstudies"),
		Parameter("pps", "Pivot Points Standard", ["pps", "pivot", "pivotpointsstandard"], tradingview="PivotPointsStandard@tv-basicstudies", premium="Pivot+Points+Standard", gocharting="PIVOTPOINTS"),
		Parameter("pricechannel", "Price Channel", ["pricechannel"], premium="Price+Channel"),
		Parameter("primenumberbands", "Prime Number Bands", ["primenumberbands", "pnb"], gocharting="PRIMENUMBERBANDS", dynamic={"GoCharting": [14, 2]}),
		Parameter("primenumberoscillator", "Prime Number Oscillator", ["primenumberoscillator", "pno"], gocharting="PRIMENUMBEROSCILLATOR"),
		Parameter("psychologicalline", "Psychological Line", ["psychologicalline", "psy", "psychological"], gocharting="PSY", dynamic={"GoCharting": [20]}),
		Parameter("pvi", "Positive Volume Index", ["pvi", "positivevolumeindex", "posvolindex"], gocharting="POSVOLINDEX"),
		Parameter("pvt", "Price Volume Trend", ["pvt", "pricevolumetrend"], tradingview="PriceVolumeTrend@tv-basicstudies", premium="Price+Volume+Trend"),
		Parameter("qstickindicator", "Qstick Indicator", ["qstickindicator", "qi", "qsticks"], gocharting="QSTICKS", dynamic={"GoCharting": [20]}),
		Parameter("randomwalk", "Random Walk", ["randomwalk", "ra"], gocharting="RANDOMWALK", dynamic={"GoCharting": [20]}),
		Parameter("ratio", "Ratio", ["ratio"], premium="Ratio"),
		Parameter("ravi", "Ravi Oscillator", ["ravi", "ravioscillator"], gocharting="RAVI"),
		Parameter("rvi", "Relative Volatility", ["rvi", "relativevolatility"], premium="Relative+Volatility+Index", gocharting="RELATIVEVOLATILITY"),
		Parameter("roc", "Price ROC", ["roc", "priceroc", "proc"], tradingview="ROC@tv-basicstudies", premium="Rate+Of+Change", gocharting="PRICEROC", dynamic={"GoCharting": [20]}),
		Parameter("rsi", "RSI", ["rsi", "relativestrength", "relativestrengthindex", "relativestrengthidx"], tradingview="RSI@tv-basicstudies", premium="Relative+Strength+Index", gocharting="RSI", dynamic={"GoCharting": [14, 20, 80]}),
		Parameter("schaff", "Schaff", ["schaff"], gocharting="SCHAFF"),
		Parameter("shinohara", "Shinohara", ["shinohara", "shin"], gocharting="SHINOHARA", dynamic={"GoCharting": [20]}),
		Parameter("shootingstarpattern", "Shooting Star Pattern", ["shootingstar", "ss", "shootingstarpattern"], gocharting="SHOOTINGSTAR"),
		Parameter("smiei", "SMI Ergodic Indicator", ["smiei", "smiergodicindicator"], tradingview="SMIErgodicIndicator@tv-basicstudies", premium="SMI+Ergodic+Indicator/Oscillator"),
		Parameter("smieo", "SMI Ergodic Oscillator", ["smieo", "smiergodicoscillator"], tradingview="SMIErgodicOscillator@tv-basicstudies", premium="SMI+Ergodic+Indicator/Oscillator"),
		Parameter("spread", "Spread", ["spread"], premium="Spread"),
		Parameter("srsi", "Stochastic RSI", ["srsi", "stochrsi", "stochasticrsi"], tradingview="StochasticRSI@tv-basicstudies", premium="Stochastic+RSI"),
		Parameter("standarderror", "Standard Error", ["standarderror"], premium="Standard+Error"),
		Parameter("stdev", "Standard Deviation", ["stdev", "stddev", "standarddeviation"], premium="Standard+Deviation", gocharting="SD"),
		Parameter("stochastic", "Stochastic", ["stochastic", "stoch"], tradingview="Stochastic@tv-basicstudies", premium="Stochastic"),
		Parameter("stolleraveragerangechannelbands", "Stoller Average Range Channel Bands", ["stolleraveragerange", "sarc", "sarcb", "stolleraveragerangechannelbands"], gocharting="STARCBAND", dynamic={"GoCharting": [14, 2]}),
		Parameter("supertrend", "Supertrend", ["supertrend"], premium="SuperTrend", gocharting="SUPERTREND", dynamic={"GoCharting": [14, 2]}),
		Parameter("swing", "Swing Index", ["swing", "swingindex", "si"], gocharting="SWINGINDEX"),
		Parameter("standardrrrorbands", "Standard Error Bands", ["standardrrrorbands"], premium="Standard+Error+Bands"),
		Parameter("tma", "Triple MA", ["tma", "triplema"], premium="Moving+Average+Triple"),
		Parameter("tema", "Triple EMA", ["tema", "tripleema"], tradingview="TripleEMA@tv-basicstudies", premium="Triple+EMA", gocharting="TEMA", dynamic={"GoCharting": [20]}),
		Parameter("tpo", "Market Profile", ["tpo", "marketprofile"], premium="Volume+Profile+Visible+Range@row+size:i:100", gocharting="MARKETPROFILE"),
		Parameter("trix", "Triple Exponential Average", ["trix", "txa", "texa", "tripleexponentialaverage"], tradingview="Trix@tv-basicstudies", premium="TRIX", gocharting="TRIX", dynamic={"GoCharting": [20]}),
		Parameter("ts", "Time Series Moving Average", ["timeseriesmovingaverage", "ts"], gocharting="TS", dynamic={"GoCharting": [20]}),
		Parameter("threeblackcrowspattern", "Three Black Crows Pattern", ["threeblackcrows", "tbc", "threeblackcrowspattern"], gocharting="THREEBLACKCROWS"),
		Parameter("threewhitesoldierspattern", "Three White Soldiers Pattern", ["threewhitesoldiers", "tws", "threewhitesoldierspattern"], gocharting="THREEWHITESOLDIERS"),
		Parameter("tradevolumeindex", "Trade Volume Index", ["tradevolumeindex", "tvi"], gocharting="TRADEVOLUMEINDEX", dynamic={"GoCharting": [20]}),
		Parameter("trendintensity", "Trend Intensity", ["trendintensity", "ti"], gocharting="TRENDINTENSITY"),
		Parameter("triangularmovingaverage", "Triangular Moving Average", ["triangularmovingaverage", "trma"], gocharting="TRIANGULAR", dynamic={"GoCharting": [20]}),
		Parameter("tweezerbottompattern", "Tweezer Bottom Pattern", ["tweezerbottom", "tbp", "tweezerbottompattern"], gocharting="TWEEZERBOTTOM"),
		Parameter("tweezertoppattern", "Tweezer Top Pattern", ["tweezertop", "ttp", "tweezertoppattern"], gocharting="TWEEZERTOP"),
		Parameter("tmfi", "Twiggs Money Flow Index", ["tmfi", "twiggsmfi", "twiggsmoneyflowindex"], gocharting="TWIGGSMONEYFLOWINDEX", dynamic={"GoCharting": [20]}),
		Parameter("typicalprice", "Typical Price", ["typicalprice", "tp"], premium="Typical+Price", gocharting="TP", dynamic={"GoCharting": [20]}),
		Parameter("truestrengthindicator", "True Strength Indicator", ["truestrengthindicator"], premium="True+Strength+Indicator"),
		Parameter("trendstrengthindex", "Trend Strength Index", ["trendstrengthindex"], premium="Trend+Strength+Index"),
		Parameter("ulcer", "Ulcer Index", ["ulcer", "ulcerindex", "ui"], gocharting="ULCERINDEX", dynamic={"GoCharting": [14, 2]}),
		Parameter("ultimate", "Ultimate Oscillator", ["ultimate", "uo", "ultimateoscillator"], tradingview="UltimateOsc@tv-basicstudies", premium="Ultimate+Oscillator"),
		Parameter("vidya", "VIDYA Moving Average", ["vidya", "vidyamovingaverage"], gocharting="VIDYA", dynamic={"GoCharting": [20]}),
		Parameter("vigor", "Vigor Index", ["vigor", "vigorindex"], tradingview="VigorIndex@tv-basicstudies", premium="Relative+Vigor+Index"),
		Parameter("vma", "Variable Moving Average", ["vma", "variablema", "varma", "variablemovingaverage"], gocharting="VMA", dynamic={"GoCharting": [20]}),
		Parameter("volatility", "Volatility Index", ["volatility", "vi", "volatilityindex"], tradingview="VolatilityIndex@tv-basicstudies", premium="Volatility+Index"),
		Parameter("volatilityclose-to-close", "Volatility Close-to-Close", ["volatilityclose-to-close"], premium="Volatility+Close-to-Close"),
		Parameter("volatilityzerotrendclose-to-close", "Volatility Zero Trend Close-to-Close", ["volatilityzerotrendclose-to-close"], premium="Volatility+Zero+Trend+Close-to-Close"),
		Parameter("volatilityo-h-l-c", "Volatility O-H-L-C", ["volatilityo-h-l-c"], premium="Volatility+O-H-L-C"),
		Parameter("volumeoscillator", "Volume Oscillator", ["volosc", "volumeoscillator"], premium="Volume+Oscillator", gocharting="VOLUMEOSCILLATOR"),
		Parameter("volumeprofile", "Volume Profile", ["volumeprofile", "vpvr"], premium="Volume+Profile+Visible+Range@row+size:i:100", gocharting="VOLUMEPROFILE"),
		Parameter("volumeroc", "Volume ROC", ["vroc", "volumeroc"], gocharting="VOLUMEROC", dynamic={"GoCharting": [20]}),
		Parameter("volumeunderlay", "Volume Underlay", ["volund", "volumeunderlay"], gocharting="VOLUMEUNDERLAY", dynamic={"GoCharting": [20]}),
		Parameter("vortex", "Vortex", ["vortex"], premium="Vortex+Indicator", gocharting="VORTEX", dynamic={"GoCharting": [20]}),
		Parameter("vstop", "VSTOP", ["vstop"], tradingview="VSTOP@tv-basicstudies"),
		Parameter("vwap", "VWAP", ["vwap"], tradingview="VWAP@tv-basicstudies", premium="VWAP", gocharting="VWAP", dynamic={"GoCharting": [20]}),
		Parameter("vwma", "VWMA", ["mavw", "vw", "vwma"], tradingview="MAVolumeWeighted@tv-basicstudies", premium="VWMA"),
		Parameter("weightedclose", "Weighted Close", ["weightedclose"], gocharting="WC", dynamic={"GoCharting": [20]}),
		Parameter("williamsr", "Williams %R", ["williamsr", "wr", "williams%r"], tradingview="WilliamR@tv-basicstudies", premium="Williams+%R", gocharting="WILLIAMSR", dynamic={"GoCharting": [14, 20, 80]}),
		Parameter("williamsa", "Williams Alligator", ["williamsa", "williamsalligator", "wa"], tradingview="WilliamsAlligator@tv-basicstudies", premium="Williams+Alligator"),
		Parameter("williamsf", "Williams Fractal", ["williamsf", "williamsfractal", "wf"], tradingview="WilliamsFractal@tv-basicstudies", premium="Williams+Fractal"),
		Parameter("wma", "Weighted Moving Average", ["wma", "weightedmovingaverage"], tradingview="MAWeighted@tv-basicstudies", premium="Moving+Average+Weighted", gocharting="WMA"),
		Parameter("zz", "Zig Zag", ["zz", "zigzag"], tradingview="ZigZag@tv-basicstudies", premium="ZigZag", gocharting="ZIGZAG")
	],
	"types": [
		Parameter("ta", "Advanced TA", ["ta", "advanced"], finviz="&ta=1"),
		Parameter("nv", "No volume", ["hv", "nv", "novol"], tradingview="&hidevolume=1", premium="&hidevolume=1"),
		Parameter("np", "No price", ["hp", "np", "nopri"], gocharting="&showmainchart=false"),
		Parameter("theme", "Light theme", ["light", "white"], tradingview="&theme=light", premium="&theme=Light", gocharting="&theme=light", alternativeme="&theme=light", cnnbusiness="&theme=light"),
		Parameter("theme", "Dark theme", ["dark", "black"], tradingview="&theme=dark", premium="&theme=Dark", gocharting="&theme=dark", alternativeme="&theme=dark", cnnbusiness="&theme=dark"),
		Parameter("candleStyle", "Bars", ["bars", "bar"], tradingview="&style=0", premium="&chartType=0"),
		Parameter("candleStyle", "Candles", ["candles", "candle"], tradingview="&style=1", premium="&chartType=1", gocharting="&charttype=CANDLESTICK", finviz="&ty=c"),
		Parameter("candleStyle", "Line", ["line"], tradingview="&style=2", premium="&chartType=2", gocharting="&charttype=LINE", finviz="&ty=l"),
		Parameter("candleStyle", "Area", ["area"], tradingview="&style=3", premium="&chartType=3", gocharting="&charttype=AREA"),
		Parameter("candleStyle", "Renko", ["renko"], tradingview="&style=4", gocharting="&charttype=RENKO"),
		Parameter("candleStyle", "Kagi", ["kagi"], tradingview="&style=5", gocharting="&charttype=KAGI"),
		Parameter("candleStyle", "Point&Figure", ["point", "figure", "pf", "paf", "point&figure"], tradingview="&style=6", gocharting="&charttype=POINT_FIGURE"),
		Parameter("candleStyle", "Line break", ["break", "linebreak", "lb"], tradingview="&style=7", gocharting="&charttype=LINEBREAK"),
		Parameter("candleStyle", "Heikin ashi", ["heikin", "heiken", "heikinashi", "heikenashi", "ashi", "ha"], tradingview="&style=8", premium="&chartType=8", gocharting="&charttype=HEIKIN_ASHI"),
		Parameter("candleStyle", "Hollow candles", ["hollow"], tradingview="&style=9", premium="&chartType=9", gocharting="&charttype=HOLLOW_CANDLESTICK"),
		Parameter("candleStyle", "Baseline", ["baseline"], premium="&chartType=10"),
		Parameter("candleStyle", "HiLo", ["hilo"], premium="&chartType=12"),
		Parameter("candleStyle", "Column", ["column"], premium="&chartType=13"),
	],
	"style": [
		Parameter("theme", "Light theme", ["light", "white"], tradinglite="light", finviz="light"),
		Parameter("theme", "Dark theme", ["dark", "black"], tradinglite="dark", finviz="dark"),
		Parameter("log", "Log chart", ["log", "logarithmic"], tradingview="log", premium="log", alternativeme="log", cnnbusiness="log"),
		Parameter("extended", "Extended hours", ["extended", "post", "pre", "extendedhours"], premium="extended"),
		Parameter("wide", "Wide chart", ["wide"], tradinglite="wide", tradingview="wide", premium="wide", bookmap="wide", gocharting="wide", alternativeme="wide", cnnbusiness="wide"),
	],
	"preferences": [
		Parameter("heatmapIntensity", "Whales heatmap intensity", ["whale", "whales"], tradinglite=(50,100)),
		Parameter("heatmapIntensity", "Low heatmap intensity", ["low"], tradinglite=(10,100)),
		Parameter("heatmapIntensity", "Normal heatmap intensity", ["normal"], tradinglite=(0,85)),
		Parameter("heatmapIntensity", "Medium heatmap intensity", ["medium", "med"], tradinglite=(0,62)),
		Parameter("heatmapIntensity", "High heatmap intensity", ["high"], tradinglite=(0,39)),
		Parameter("heatmapIntensity", "Crazy heatmap intensity", ["crazy"], tradinglite=(0,16)),
		Parameter("forcePlatform", "request chart on TradingLite", ["tl", "tradinglite"], tradinglite=True),
		Parameter("forcePlatform", "request chart on TradingView", ["tv", "tradingview"], tradingview=True),
		Parameter("forcePlatform", "request chart on TradingView Premium", ["tv", "tradingview", "prem", "premium", "tvp", "tradingviewpremium"], premium=True),
		Parameter("forcePlatform", "request chart on Bookmap", ["bm", "bookmap"], bookmap=True),
		Parameter("forcePlatform", "request chart on GoCharting", ["gc", "gocharting"], gocharting=True),
		Parameter("forcePlatform", "request chart on Finviz", ["fv", "finviz"], finviz=True),
		Parameter("forcePlatform", "request chart on Alternative.me", ["am", "alternativeme"], alternativeme=True),
		Parameter("forcePlatform", "request chart on CNN Business", ["cnn", "cnnbusiness"], cnnbusiness=True),
	]
}
DEFAULTS = {
	"Alternative.me": {
		"timeframes": [AbstractRequest.find_parameter_with_id(1440, type="timeframes", params=PARAMETERS)],
		"indicators": [],
		"types": [],
		"style": [],
		"preferences": []
	},
	"CNN Business": {
		"timeframes": [AbstractRequest.find_parameter_with_id(1440, type="timeframes", params=PARAMETERS)],
		"indicators": [],
		"types": [],
		"style": [],
		"preferences": []
	},
	"TradingLite": {
		"timeframes": [AbstractRequest.find_parameter_with_id(60, type="timeframes", params=PARAMETERS)],
		"indicators": [],
		"types": [],
		"style": [AbstractRequest.find_parameter_with_id("theme", name="Dark theme", type="style", params=PARAMETERS)],
		"preferences": [AbstractRequest.find_parameter_with_id("heatmapIntensity", name="Normal heatmap intensity", type="preferences", params=PARAMETERS)]
	},
	"TradingView Premium": {
		"timeframes": [AbstractRequest.find_parameter_with_id(60, type="timeframes", params=PARAMETERS)],
		"indicators": [],
		"types": [AbstractRequest.find_parameter_with_id("theme", name="Dark theme", type="types", params=PARAMETERS), AbstractRequest.find_parameter_with_id("candleStyle", name="Candles", type="types", params=PARAMETERS)],
		"style": [],
		"preferences": []
	},
	"TradingView": {
		"timeframes": [AbstractRequest.find_parameter_with_id(60, type="timeframes", params=PARAMETERS)],
		"indicators": [],
		"types": [AbstractRequest.find_parameter_with_id("theme", name="Dark theme", type="types", params=PARAMETERS), AbstractRequest.find_parameter_with_id("candleStyle", name="Candles", type="types", params=PARAMETERS)],
		"style": [],
		"preferences": []
	},
	"Bookmap": {
		"timeframes": [AbstractRequest.find_parameter_with_id(60, type="timeframes", params=PARAMETERS)],
		"indicators": [],
		"types": [],
		"style": [],
		"preferences": []
	},
	"GoCharting": {
		"timeframes": [AbstractRequest.find_parameter_with_id(60, type="timeframes", params=PARAMETERS)],
		"indicators": [],
		"types": [AbstractRequest.find_parameter_with_id("theme", name="Dark theme", type="types", params=PARAMETERS), AbstractRequest.find_parameter_with_id("candleStyle", name="Candles", type="types", params=PARAMETERS)],
		"style": [],
		"preferences": []
	},
	"Finviz": {
		"timeframes": [AbstractRequest.find_parameter_with_id(1440, type="timeframes", params=PARAMETERS)],
		"indicators": [],
		"types": [AbstractRequest.find_parameter_with_id("candleStyle", name="Candles", type="types", params=PARAMETERS)],
		"style": [AbstractRequest.find_parameter_with_id("theme", name="Light theme", type="style", params=PARAMETERS)],
		"preferences": []
	}
}


class ChartRequestHandler(AbstractRequestHandler):
	def __init__(self, tickerId, platforms, bias="traditional"):
		super().__init__(platforms)
		for platform in platforms:
			self.requests[platform] = ChartRequest(tickerId, platform, bias)

	async def parse_argument(self, argument):
		for platform, request in self.requests.items():
			_argument = argument.lower().replace(" ", "")
			if request.errorIsFatal or argument == "": continue

			# None None - No successeful parse
			# None True - Successful parse and add
			# "" False - Successful parse and error
			# None False - Successful parse and breaking error

			finalOutput = None

			responseMessage, success = await request.add_timeframe(_argument)
			if responseMessage is not None: finalOutput = responseMessage
			elif success: continue

			responseMessage, success = await request.add_indicator(_argument)
			if responseMessage is not None: finalOutput = responseMessage
			elif success: continue

			responseMessage, success = await request.add_type(_argument)
			if responseMessage is not None: finalOutput = responseMessage
			elif success: continue

			responseMessage, success = await request.add_style(_argument)
			if responseMessage is not None: finalOutput = responseMessage
			elif success: continue

			responseMessage, success = await request.add_preferences(_argument)
			if responseMessage is not None: finalOutput = responseMessage
			elif success: continue

			responseMessage, success = await request.add_exchange(_argument)
			if responseMessage is not None: finalOutput = responseMessage
			elif success: continue

			responseMessage, success = await request.add_numerical_parameters(_argument)
			if responseMessage is not None: finalOutput = responseMessage
			elif success: continue

			if finalOutput is None:
				request.set_error(f"`{argument[:229]}` is not a valid argument.", isFatal=True)
			elif finalOutput.startswith("`Request Chart"):
				request.set_error(None, isFatal=True)
			else:
				request.set_error(finalOutput)

	def set_defaults(self):
		for platform, request in self.requests.items():
			if request.errorIsFatal: continue
			for type in PARAMETERS:
				request.set_default_for(type)

	async def find_caveats(self):
		for platform, request in self.requests.items():
			if request.errorIsFatal: continue

			types = "".join([e.parsed[platform] for e in request.types])
			styles = [e.parsed[platform] for e in request.styles]
			preferences = [{"id": e.id, "value": e.parsed[platform]} for e in request.preferences]

			if platform == "Alternative.me":
				if request.ticker.get("id") not in ["FGI"]: request.set_error(None, isFatal=True)
			
			elif platform == "CNN Business":
				if request.ticker.get("id") not in ["FGI"]: request.set_error(None, isFatal=True)
			
			elif platform == "TradingLite":
				if not bool(request.exchange):
					request.set_error("TradingLite currently only supports cryptocurrency markets on supported exchanges.", isFatal=True)
				elif request.ticker.get("symbol") is None:
					request.set_error(f"Requested chart for `{request.ticker.get('id')}` is not available.", isFatal=True)
				elif request.exchange.get("id") in ["binanceusdm", "binancecoinm", "ftx", "okex5"]:
					request.set_error(f"{request.exchange.get('name')} exchange is not available. ||Yet? Let TradingLite know you want it!||", isFatal=True)
			
			elif platform == "TradingView":
				if "&style=6" in types and "log" in styles:
					request.set_error("Point & Figure chart can't be viewed in log scale.", isFatal=True)
			
			elif platform == "Bookmap":
				if not bool(request.exchange):
					request.set_error("Bookmap currently only supports cryptocurrency markets on supported exchanges.", isFatal=True)
			
			elif platform == "GoCharting":
				request.set_error("GoCharting charts are temporarily unavailable.", isFatal=True)

				indicators = request.indicators
				parameters = request.numericalParameters
				lengths = {i: [] for i in range(len(indicators))}
				cursor = len(parameters) - 1
				for i in reversed(range(len(indicators))):
					while parameters[cursor] != -1:
						lengths[i].insert(0, parameters[cursor])
						cursor -= 1
					cursor -= 1

					if indicators[i].dynamic is not None and len(lengths[i]) > len(indicators[i].dynamic[platform]):
						request.set_error(f"{indicators[i].name} indicator takes in `{len(indicators[i].dynamic[platform])}` {'parameters' if len(indicators[i].dynamic[platform]) > 1 else 'parameter'}, but `{len(lengths[i])}` were given.", isFatal=True)
						break

				if len(indicators) == 0 and len(parameters) != 0:
					request.set_error(f"`{str(parameters[0])[:229]}` is not a valid argument.", isFatal=True)
			
			elif platform == "Finviz":
				pass


	def to_dict(self):
		d = {
			"platforms": self.platforms,
			"currentPlatform": self.currentPlatform
		}

		timeframes = []

		for platform in self.platforms:
			request = self.requests[platform].to_dict()
			timeframes.append(request.pop("timeframes"))
			d[platform] = request

		d["timeframes"] = {p: t for p, t in zip(self.platforms, timeframes)}
		d["requestCount"] = len(d["timeframes"][d.get("currentPlatform")])

		return d


class ChartRequest(AbstractRequest):
	def __init__(self, tickerId, platform, bias):
		super().__init__(platform, bias)
		self.tickerId = tickerId
		self.ticker = {}
		self.exchange = {}

		self.timeframes = []
		self.indicators = []
		self.types = []
		self.styles = []
		self.preferences = []
		self.numericalParameters = []

		self.currentTimeframe = None
		self.hasExchange = False

	async def process_ticker(self):
		updatedTicker, error = None, None
		try: updatedTicker, error = await match_ticker(self.tickerId, self.exchange.get("id"), self.platform, self.parserBias)
		except: error = "Something went wrong while processing the requested ticker."

		if error is not None:
			self.set_error(error, isFatal=True)
		elif updatedTicker.get("id") is None:
			self.couldFail = True
		else:
			self.ticker = updatedTicker
			self.tickerId = updatedTicker.get("id")
			self.exchange = updatedTicker.get("exchange")

	def add_parameter(self, argument, type):
		isSupported = None
		parsedParameter = None
		requiresPro = None
		for param in PARAMETERS[type]:
			if argument in param.parsablePhrases:
				parsedParameter = param
				isSupported = param.supports(self.platform)
				if isSupported: break
				if self.platform == "TradingView" and param.supports("TradingView Premium"):
					requiresPro = "Live Charting Data"
		return isSupported, parsedParameter, requiresPro

	# async def add_timeframe(self, argument) -- inherited

	# async def add_exchange(self, argument) -- inherited

	async def add_indicator(self, argument):
		if argument in ["oscillator", "bands", "band", "ta"]: return None, False
		length = search("(\d+)$", argument)
		if length is not None and int(length.group()) > 0: argument = argument[:-len(length.group())]
		indicatorSupported, parsedIndicator, requiresPro = self.add_parameter(argument, "indicators")
		if parsedIndicator is not None and not self.has_parameter(parsedIndicator.id, self.indicators):
			if not indicatorSupported:
				responseMessage = f"{parsedIndicator.name} indicator is " + (f"only available with the {requiresPro} add-on." if requiresPro else f"not supported on {self.platform}.")
				return responseMessage, False
			self.indicators.append(parsedIndicator)
			self.numericalParameters.append(-1)
			if length is not None:
				if self.platform not in ["GoCharting"]:
					responseMessage = "Indicator lengths can only be changed on GoCharting."
					return responseMessage, False
				else:
					self.numericalParameters.append(int(length.group()))
			return None, True
		return None, None

	async def add_type(self, argument):
		typeSupported, parsedType, requiresPro = self.add_parameter(argument, "types")
		if parsedType is not None and not self.has_parameter(parsedType.id, self.types):
			if not typeSupported:
				responseMessage = f"`{parsedType.name.title()}` chart style is " + (f"only available with the {requiresPro} add-on." if requiresPro else f"not supported on {self.platform}.")
				return responseMessage, False
			self.types.append(parsedType)
			return None, True
		return None, None

	# async def add_style(self, argument) -- inherited

	# async def add_preferences(self, argument) -- inherited

	async def add_numerical_parameters(self, argument):
		try:
			numericalParameter = float(argument)
			if numericalParameter <= 0:
				responseMessage = "Only parameters greater than `0` are valid."
				return responseMessage, False
			if self.platform not in ["GoCharting"]:
				responseMessage = "Indicator lengths can only be changed on GoCharting."
				return responseMessage, False
			self.numericalParameters.append(numericalParameter)
			return None, True
		except: return None, None

	def set_default_for(self, t):
		if t == "timeframes" and len(self.timeframes) == 0:
			for parameter in DEFAULTS.get(self.platform, {}).get(t, []):
				if not self.has_parameter(parameter.id, self.timeframes): self.timeframes.append(parameter)
		elif t == "indicators":
			for parameter in DEFAULTS.get(self.platform, {}).get(t, []):
				if not self.has_parameter(parameter.id, self.indicators): self.indicators.append(parameter)
		elif t == "types":
			for parameter in DEFAULTS.get(self.platform, {}).get(t, []):
				if not self.has_parameter(parameter.id, self.types): self.types.append(parameter)
		elif t == "style":
			for parameter in DEFAULTS.get(self.platform, {}).get(t, []):
				if not self.has_parameter(parameter.id, self.styles): self.styles.append(parameter)
		elif t == "preferences":
			for parameter in DEFAULTS.get(self.platform, {}).get(t, []):
				if not self.has_parameter(parameter.id, self.preferences): self.preferences.append(parameter)

	def prepare_indicators(self):
		indicators = []

		if self.platform == "TradingView":
			if len(self.indicators) == 0:
				indicators = ""
			else:
				indicators = "&studies=" + "%1F".join([e.parsed[self.platform] for e in self.indicators])

		elif self.platform == "TradingView Premium":
			if len(self.indicators) == 0:
				indicators = ""
			else:
				indicators = "&studies=" + ",".join([e.parsed[self.platform] for e in self.indicators])

		elif self.platform == "GoCharting":
			if len(self.indicators) == 0:
				indicators = ""
			else:
				lengths = {i: [] for i in range(len(self.indicators))}
				cursor = len(self.numericalParameters) - 1
				for i in reversed(range(len(self.indicators))):
					while self.numericalParameters[cursor] != -1:
						lengths[i].insert(0, self.numericalParameters[cursor])
						cursor -= 1
					cursor -= 1

					if self.indicators[i].dynamic is not None and lengths[i] != 0 and len(lengths[i]) < len(self.indicators[i].dynamic[self.platform]):
						for j in range(len(lengths[i]), len(self.indicators[i].dynamic[self.platform])):
							lengths[i].append(self.indicators[i].dynamic[self.platform][j])

					indicators.insert(0, f"{self.indicators[i].parsed[self.platform]}_{'_'.join([str(l) for l in lengths[i]])}")

				indicators = "&studies=" + "-".join(indicators)

		return indicators


	def to_dict(self):
		d = {
			"ticker": self.ticker,
			"exchange": self.exchange,
			"parserBias": self.parserBias,
			"timeframes": [e.parsed[self.platform] for e in self.timeframes],
			"indicators": self.prepare_indicators(),
			"types": "".join([e.parsed[self.platform] for e in self.types]),
			"styles": [e.parsed[self.platform] for e in self.styles],
			"preferences": [{"id": e.id, "value": e.parsed[self.platform]} for e in self.preferences],
			"numericalParameters": self.numericalParameters,
			"currentTimeframe": self.currentTimeframe
		}
		return d