from sys import maxsize as MAXSIZE
from time import time
from re import search
from asyncio import wait
from traceback import format_exc

from matching.instruments import match_ticker
from .parameter import ChartParameter as Parameter
from .abstract import AbstractRequestHandler, AbstractRequest


PARAMETERS = {
	"timeframes": [
		Parameter(1/60, "1-second", ["1s", "1sec", "1secs", "1second", "1-second", "1seconds"], premium="1S", relay="1S"),
		Parameter(5/60, "5-second", ["5s", "5sec", "5secs", "5second", "5-second", "5seconds"], premium="5S", relay="5S"),
		Parameter(10/60, "10-second", ["10s", "10sec", "10secs", "10second", "10-second", "10seconds"], premium="10S", relay="10S"),
		Parameter(15/60, "15-second", ["15s", "15sec", "15secs", "15second", "15-second", "15seconds"], premium="15S", relay="15S"),
		Parameter(30/60, "30-second", ["30s", "30sec", "30secs", "30second", "30-second", "30seconds"], premium="30S", relay="30S"),
		Parameter(1, "1-minute", ["1", "1m", "1min", "1mins", "1minute", "1-minute", "1minutes", "min", "m"], tradinglite="1", tradingview="1", premium="1", relay="1"),
		Parameter(2, "2-minute", ["2", "2m", "2min", "2mins", "2minute", "2-minute", "2minutes"], premium="2", relay="2"),
		Parameter(3, "3-minute", ["3", "3m", "3min", "3mins", "3minute", "3-minute", "3minutes"], tradinglite="3", tradingview="3", premium="3", relay="3"),
		Parameter(4, "4-minute", ["4", "4m", "4min", "4mins", "4minute", "4-minute", "4minutes"], premium="4", relay="4"),
		Parameter(5, "5-minute", ["5", "5m", "5min", "5mins", "5minute", "5-minute", "5minutes"], tradinglite="5", tradingview="5", premium="5", relay="5"),
		Parameter(6, "6-minute", ["6", "6m", "6min", "6mins", "6minute", "6-minute", "6minutes"], premium="6", relay="6"),
		Parameter(10, "10-minute", ["10", "10m", "10min", "10mins", "10minute", "10-minute", "10minutes"], premium="10", relay="10"),
		Parameter(15, "15-minute", ["15", "15m", "15min", "15mins", "15minute", "15-minute", "15minutes"], tradinglite="15", tradingview="15", premium="15", relay="15"),
		Parameter(20, "20-minute", ["20", "20m", "20min", "20mins", "20minute", "20-minute", "20minutes"], premium="20", relay="20"),
		Parameter(30, "30-minute", ["30", "30m", "30min", "30mins", "30minute", "30-minute", "30minutes"], tradinglite="30", tradingview="30", premium="30", relay="30"),
		Parameter(45, "45-minute", ["45", "45m", "45min", "45mins", "45minute", "45-minute", "45minutes"], tradingview="45", premium="45", relay="45"),
		Parameter(60, "1-hour", ["60", "60m", "60min", "60mins", "60minute", "60-minute", "60minutes", "1", "1h", "1hr", "1hour", "1-hour", "1hours", "hourly", "hour", "hr", "h"], tradinglite="60", tradingview="60", premium="1H", relay="60"),
		Parameter(120, "2-hour", ["120", "120m", "120min", "120mins", "120minute", "120-minute", "120minutes", "2", "2h", "2hr", "2hrs", "2hour", "2-hour", "2hours"], tradinglite="120", tradingview="120", premium="2H", relay="120"),
		Parameter(180, "3-hour", ["180", "180m", "180min", "180mins", "180minute", "180-minute", "180minutes", "3", "3h", "3hr", "3hrs", "3hour", "3-hour", "3hours"], tradingview="180", premium="3H", relay="180"),
		Parameter(240, "4-hour", ["240", "240m", "240min", "240mins", "240minute", "240-minute", "240minutes", "4", "4h", "4hr", "4hrs", "4hour", "4-hour", "4hours"], tradinglite="240", tradingview="240", premium="4H", relay="240"),
		Parameter(360, "6-hour", ["360", "360m", "360min", "360mins", "360minute", "360-minute", "360minutes", "6", "6h", "6hr", "6hrs", "6hour", "6-hour", "6hours"], tradinglite="360", premium="6H", relay="360"),
		Parameter(480, "8-hour", ["480", "480m", "480min", "480mins", "480minute", "480-minute", "480minutes", "8", "8h", "8hr", "8hrs", "8hour", "8-hour", "8hours"], tradinglite="480", premium="8H", relay="480"),
		Parameter(720, "12-hour", ["720", "720m", "720min", "720mins", "720minute", "720-minute", "720minutes", "12", "12h", "12hr", "12hrs", "12hour", "12-hour", "12hours"], tradinglite="720", premium="12H", relay="720"),
		Parameter(1440, "1-day", ["24", "24h", "24hr", "24hrs", "24hour", "24-hour", "24hours", "d", "day", "1", "1d", "1day", "1-day", "daily", "1440", "1440m", "1440min", "1440mins", "1440minute", "1440-minute", "1440minutes"], tradinglite="1440", tradingview="D", premium="1D", relay="D", alternativeme="1D", cnnbusiness="1D"),
		Parameter(2880, "2-day", ["48", "48h", "48hr", "48hrs", "48hour", "48-hour", "48hours", "2", "2d", "2day", "2-day", "2880", "2880m", "2880min", "2880mins", "2880minute", "2880-minute", "2880minutes"], premium="2D", relay="2D", alternativeme="2D", cnnbusiness="2D"),
		Parameter(3420, "3-day", ["72", "72h", "72hr", "72hrs", "72hour", "72-hour", "72hours", "3", "3d", "3day", "3-day", "3420", "3420m", "3420min", "3420mins", "3420minute", "3420-minute", "3420minutes"], premium="3D", relay="3D", alternativeme="3D", cnnbusiness="3D"),
		Parameter(5760, "4-day", ["96", "96h", "96hr", "96hrs", "96hour", "96-hour", "96hours", "4", "4d", "4day", "4-day", "5760", "5760m", "5760min", "5760mins", "5760minute", "5760-minute", "5760minutes"], premium="4D", relay="4D", alternativeme="4D", cnnbusiness="4D"),
		Parameter(7200, "5-day", ["120", "120h", "120hr", "120hrs", "120hour", "120-hour", "120hours", "5", "5d", "5day", "5-day", "7200", "7200m", "7200min", "7200mins", "7200minute", "7200-minute", "7200minutes"], premium="5D", relay="5D", alternativeme="5D", cnnbusiness="5D"),
		Parameter(8640, "6-day", ["144", "144h", "144hr", "144hrs", "144hour", "144-hour", "144hours", "6", "6d", "6day", "6-day", "8640", "8640m", "8640min", "8640mins", "8640minute", "8640-minute", "8640minutes"], premium="6D", relay="6D", alternativeme="6D", cnnbusiness="6D"),
		Parameter(10080, "1-week", ["7", "7d", "7day", "7-day", "7days", "w", "week", "1w", "1-week", "1week", "weekly"], tradingview="W", premium="1W", relay="W", alternativeme="1W", cnnbusiness="1W"),
		Parameter(20160, "2-week", ["14", "14d", "14day", "14-day", "14days", "2w", "2-week", "2week"], premium="2W", relay="2W", alternativeme="2W", cnnbusiness="2W"),
		Parameter(30240, "3-week", ["21", "21d", "21day", "21-day", "21days", "3w", "3-week", "3week"], premium="3W", relay="3W", alternativeme="3W", cnnbusiness="3W"),
		Parameter(43829, "1-month", ["30d", "30day", "30-day", "30days", "1", "1m", "m", "mo", "month", "1mo", "1month", "1-month", "monthly"], tradingview="M", premium="1M", relay="M", alternativeme="1M", cnnbusiness="1M"),
		Parameter(87658, "2-month", ["2", "2m", "2m", "2mo", "2month", "2-month", "2months"], premium="2M", relay="2M"),
		Parameter(131487, "3-month", ["3", "3m", "3m", "3mo", "3month", "3-month", "3months"], premium="3M", relay="3M"),
		Parameter(175316, "4-month", ["4", "4m", "4m", "4mo", "4month", "4-month", "4months"], premium="4M", relay="4M"),
		Parameter(262974, "6-month", ["6", "6m", "6mo", "6month", "6-month", "6months"], premium="6M", relay="6M"),
		Parameter(525949, "1-year", ["12", "12m", "12mo", "12month", "12months", "year", "yearly", "1year", "1-year", "1y", "y", "annual", "annually"], premium="12M", relay="12M"),
	],
	"indicators": [
		Parameter("none", "no indicators", ["none", "noindicators"], tradingview="", premium=""), # Here due to default indicators
		Parameter("accd", "Accumulation/Distribution", ["accd", "ad", "acc", "accumulationdistribution", "accumulation/distribution"], tradingview="STD;Accumulation_Distribution", premium="Accumulation/Distribution"),
		Parameter("accumulationswingindex", "Accumulation Swing Index", ["accumulationswingindex", "accsi", "asi"], premium="Accumulative+Swing+Index"),
		Parameter("adl", "Advance/Decline Line", ["adl", "advance/declineline"], tradingview="STD;Advance%1Decline%1Line"),
		Parameter("adr", "Advance/Decline Ratio", ["adr", "advance/declineratio"], tradingview="STD;Advance%1Decline%1Ratio", premium="Advance/Decline"),
		Parameter("adb", "Advance/Decline Ratio (Bars)", ["adb", "advance/declinebars", "advance/declineratio(bars)"], tradingview="STD;Advance_Decline_Ratio_Bars"),
		Parameter("arnaudlegouxmovingaverage", "Arnaud Legoux Moving Average", ["alma", "arnaudlegouxmovingaverage"], tradingview="STD;Arnaud%1Legoux%1Moving%1Average", premium="Arnaud+Legoux+Moving+Average"),
		Parameter("aroon", "Aroon", ["aroon"], tradingview="STD;Aroon", premium="Aroon"),
		Parameter("admi", "Average Directional Movement Index", ["admi", "adx", "averagedirectionalmovementindex", "averagedirectionalindex"], tradingview="STD;Average%1Directional%1Index", premium="Average+Directional+Index"),
		Parameter("adr", "Average Day Range", ["adr", "averagedayrange"], tradingview="STD;Average%Day%Range"),
		Parameter("atr", "Average True Range", ["atr", "averagetruerange"], tradingview="STD;Average_True_Range", premium="Average+True+Range"),
		Parameter("average", "Average Price", ["averageprice", "ap", "average"], tradingview="STD;Time%1Weighted%1Average%1Price", premium="Average+Price"),
		Parameter("awesome", "Awesome Oscillator", ["awesome", "ao", "awesomeoscillator"], tradingview="STD;Awesome_Oscillator", premium="Awesome+Oscillator"),
		Parameter("balanceofpower", "Balance of Power", ["balanceofpower", "bop"], tradingview="STD;Balance%1of%1Power", premium="Balance+of+Power"),
		Parameter("bollinger", "Bollinger Bands", ["bollinger", "bbands", "bb", "bollingerbands"], tradingview="STD;Bollinger_Bands", premium="Bollinger+Bands"),
		Parameter("bbb", "Bollinger Bands %B", ["%b", "bollingerbandsb", "bollingerbands%b", "bbb"], tradingview="STD;Bollinger_Bands_B", premium="Bollinger+Bands+%B"),
		Parameter("width", "Bollinger Bands Width", ["width", "bbw", "bollingerbandswidth"], tradingview="STD;Bollinger_Bands_Width", premium="Bollinger+Bands+Width"),
		Parameter("bbp", "Bull Bear Power", ["bbp", "bullbearpower"], tradingview="STD;Bull%Bear%Power"),
		Parameter("cmf", "Chaikin Money Flow Index", ["cmf", "chaikinmoneyflow", "chaikinmoneyflowindex"], tradingview="STD;Chaikin_Money_Flow", premium="Chaikin+Money+Flow"),
		Parameter("chaikin", "Chaikin Oscillator", ["chaikin", "co", "chaikinoscillator"], tradingview="STD;Chaikin_Oscillator", premium="Chaikin+Oscillator"),
		Parameter("chandekrollstop", "Chande Kroll Stop", ["chandekrollstop"], premium="STD;Chande%1Kroll%1Stop"),
		Parameter("chande", "Chande Momentum Oscillator", ["chande", "cmo", "chandemomentumoscillator"], tradingview="STD;Chande_Momentum_Oscillator", premium="Chande+Momentum+Oscillator"),
		Parameter("chopzone", "Chop Zone", ["chopzone"], tradingview="STD;Chop%1Zone", premium="Chop+Zone"),
		Parameter("choppiness", "Choppiness Index", ["choppiness", "ci", "choppinessindex"], tradingview="STD;Choppiness_Index", premium="Choppiness+Index"),
		Parameter("cci", "Commodity Channel Index", ["cci"], tradingview="STD;CCI", premium="Commodity+Channel+Index"),
		Parameter("crsi", "Connors RSI", ["crsi"], tradingview="STD;Connors_RSI", premium="Connors+RSI"),
		Parameter("coppockcurve", "Coppock Curve", ["coppockcurve"], tradingview="STD;Coppock%1Curve", premium="Coppock+Curve"),
		Parameter("correlation", "Correlation Coefficient", ["correlation", "cc", "correlationcoefficient"], tradingview="STD;Correlation_Coeff", premium="Correlation+Coefficient"),
		Parameter("correlationlog", "Correlation - Log", ["correlationlog", "correlation-log", "correlationcoefficientlog", "cclog"], premium="Correlation+-+Log"),
		Parameter("cvi", "Cumulative Volume Index", ["cvi", "cumulativevolumeindex"], tradingview="STD;Cumulative%1Volume%1Index"),
		Parameter("detrended", "Detrended Price Oscillator", ["detrended", "dpo", "detrendedpriceoscillator"], tradingview="STD;DPO", premium="Detrended+Price+Oscillator"),
		Parameter("dm", "Directional Movement", ["dm", "directionalmovement"], tradingview="STD;DMI", premium="Directional+Movement"),
		Parameter("donch", "DONCH", ["donch", "donchainchannel"], tradingview="STD;Donchian_Channels", premium="Donchian+Channels"),
		Parameter("dema", "Double EMA", ["dema", "doubleema"], tradingview="STD;DEMA", premium="Double+EMA"),
		Parameter("eom", "Ease of Movement", ["eom", "easeofmovement"], tradingview="STD;EOM", premium="Ease+of+Movement"),
		Parameter("efi", "Elder's Force Index", ["efi"], tradingview="STD;EFI", premium="Elder's Force Index"),
		Parameter("ema", "EMA", ["ema"], tradingview="STD;EMA", premium="Moving+Average+Exponential", dynamic=[("length:f:", 9)]),
		Parameter("env", "Envelope", ["env"], tradingview="STD;ENV", premium="Envelopes"),
		Parameter("fisher", "Fisher Transform", ["fisher", "ft", "fishertransform"], tradingview="STD;Fisher_Transform", premium="Fisher+Transform"),
		Parameter("gaps", "Gaps", ["gaps"], tradingview="STD;Gaps"),
		Parameter("guppy", "Guppy Moving Average", ["guppy", "gma", "rainbow", "rma", "guppymovingaverage"], premium="Guppy+Multiple+Moving+Average"),
		Parameter("hv", "Historical Volatility", ["historicalvolatility", "hv"], tradingview="STD;Historical_Volatility", premium="Historical+Volatility"),
		Parameter("hull", "Hull MA", ["hull", "hma", "hullma"], tradingview="STD;Hull%1MA", premium="Hull+Moving+Average"),
		Parameter("ichimoku", "Ichimoku Cloud", ["ichimoku", "cloud", "ichi", "ic", "ichimokucloud"], tradingview="STD;Ichimoku%1Cloud", premium="Ichimoku+Cloud"),
		Parameter("keltner", "Keltner Channels", ["keltner", "kltnr", "keltnerchannel"], tradingview="STD;Keltner_Channels", premium="Keltner+Channels"),
		Parameter("klinger", "Klinger Oscillator", ["ko", "klinger", "klingeroscillator"], tradingview="STD;Klinger%1Oscillator", premium="Klinger+Oscillator"),
		Parameter("kst", "Know Sure Thing", ["knowsurething", "kst"], tradingview="STD;Know_Sure_Thing", premium="Know+Sure+Thing"),
		Parameter("leastsquaresmovingaverage", "Least Squares Moving Average", ["leastsquaresmovingaverage"], tradingview="STD;Least%1Squares%1Moving%1Average", premium="Least+Squares+Moving+Average"),
		Parameter("regression", "Linear Regression Channel", ["regression", "regressionchannel", "lr", "lrc", "linreg", "linearregression", "linearregressionchannel"], tradingview="STD;Linear_Regression"),
		Parameter("regressionslope", "Linear Regression Slope", ["regressionslope", "lrs", "linregs", "linearregressionslope"], premium="Linear+Regression+Slope"),
		Parameter("regressioncurve", "Linear Regression Curve", ["regressioncurve", "lrc", "linregc", "linearregressioncurve"], premium="Linear+Regression+Curve"),
		Parameter("macd", "MACD", ["macd"], tradingview="STD;MACD", premium="MACD"),
		Parameter("mawithemacross", "MA with EMA Cross", ["mawithemacross"], premium="MA+with+EMA+Cross"),
		Parameter("massindex", "Mass Index", ["massindex", "mi"], tradingview="STD;Mass%1Index", premium="Mass+Index"),
		Parameter("mcginleydynamic", "McGinley Dynamic", ["mcginleydynamic"], tradingview="STD;McGinley%1Dynamic", premium="McGinley+Dynamic"),
		Parameter("medianprice", "Median Price", ["medianprice"], tradingview="STD;Median", premium="Median+Price"),
		Parameter("majorityrule", "Majority Rule", ["majorityrule"], premium="Majority+Rule"),
		Parameter("mom", "Momentum", ["mom", "momentum"], tradingview="STD;Momentum", premium="Momentum"),
		Parameter("mf", "Money Flow Index", ["mf", "mfi", "moneyflow"], tradingview="STD;Money_Flow", premium="Money+Flow+Index"),
		Parameter("moon", "Moon Phases", ["moon", "moonphases"], tradingview="STD;Moon%1Phases"),
		Parameter("ma", "Moving Average", ["ma", "movingaverage"], tradingview="STD;SMA", premium="Moving+Average", dynamic=[("length:f:", 9)]),
		Parameter("macross", "MA Cross", ["macross"], tradingview="STD;MA%1Cross", premium="MA+Cross"),
		Parameter("maribbon", "MA Ribbon", ["maribbon"], tradingview="STD;MA%Ribbon"),
		Parameter("emacross", "EMA Cross", ["emacross"], premium="EMA+Cross"),
		Parameter("movingaveragechannel", "Moving Average Channel", ["movingaveragechannel"], premium="Moving+Average+Channel"),
		Parameter("movingaveragedouble", "Moving Average Double", ["movingaveragedouble"], premium="Moving+Average+Double"),
		Parameter("movingaverageadaptive", "Moving Average Adaptive", ["movingaverageadaptive"], premium="Moving+Average+Adaptive"),
		Parameter("movingaveragehamming", "Moving Average Hamming", ["movingaveragehamming"], premium="Moving+Average+Hamming"),
		Parameter("movingaveragemultiple", "Moving Average Multiple", ["movingaveragemultiple"], premium="Moving+Average+Multiple"),
		Parameter("obv", "On Balance Volume", ["obv", "onbalancevolume"], tradingview="STD;On_Balance_Volume", premium="On+Balance+Volume"),
		Parameter("oi", "Open Interest", ["oi", "openinterest"], tradingview="STD;Open%Interest"),
		Parameter("parabolic", "Parabolic SAR", ["parabolic", "sar", "psar", "parabolicsar"], tradingview="STD;PSAR", premium="Parabolic+SAR"),
		Parameter("pphl", "Pivot Points High Low", ["pphl", "pivotpointshighlow"], tradingview="STD;Pivot%1Points%1High%1Low"),
		Parameter("pps", "Pivot Points Standard", ["pps", "pivot", "pivotpointsstandard"], tradingview="STD;Pivot%1Points%1Standard", premium="Pivot+Points+Standard"),
		Parameter("po", "Price Oscillator", ["po", "priceoscillator"], tradingview="STD;Price_Oscillator", premium="Price+Oscillator"),
		Parameter("pricechannel", "Price Channel", ["pricechannel"], premium="Price+Channel"),
		Parameter("pvt", "Price Volume Trend", ["pvt", "pricevolumetrend"], tradingview="STD;Price_Volume_Trend", premium="Price+Volume+Trend"),
		Parameter("ratio", "Ratio", ["ratio"], premium="Ratio"),
		Parameter("roc", "Price ROC", ["roc", "priceroc", "proc"], tradingview="STD;ROC", premium="Rate+Of+Change"),
		Parameter("rbzgp", "Rob Booker - Ziv Ghost Pivots", ["rbzgp", "robbooker-zivghostpivots", "robbookerzivghostpivots", "robbooker", "zivghostpivots"], tradingview="STD;Rob%1Booker%1Ghost%1Pivots%1v2"),
		Parameter("rvi", "Relative Volatility", ["rvi", "relativevolatility"], premium="Relative+Volatility+Index"),
		Parameter("rsi", "RSI", ["rsi", "relativestrength", "relativestrengthindex", "relativestrengthidx"], tradingview="STD;RSI", premium="Relative+Strength+Index"),
		Parameter("rsidiv", "RSI Divergence Indicator", ["rsidiv", "rsidivergenceindicator", "rsidivergence"], tradingview="STD;Divergence%1Indicator"),
		Parameter("rvigor", "Relative Vigor Index", ["vigor", "vigorindex"], tradingview="STD;Relative_Vigor_Index", premium="Relative+Vigor+Index"),
		Parameter("rvat", "Relative Volume at Time", ["rvat", "relativevolumeattime"], tradingview="STD;Relative%1Volume%1at%1Time"),
		Parameter("sma", "Smoothed Moving Average", ["sma", "smoothedmovingaverage"], tradingview="STD;Smoothed%1Moving%1Average", premium="Smoothed+Moving+Average", dynamic=[("length:f:", 9)]),
		Parameter("smi", "Stochastic Momentum Index", ["smi", "stochmi", "stochasticmi", "stochasticmomentumindex"], tradingview="STD;SMI"),
		Parameter("smiei", "SMI Ergodic Indicator", ["smiei", "smiergodicindicator"], tradingview="STD;SMI_Ergodic_Indicator_Oscillator", premium="SMI+Ergodic+Indicator/Oscillator"),
		Parameter("smieo", "SMI Ergodic Oscillator", ["smieo", "smiergodicoscillator"], tradingview="STD;SMI_Ergodic_Oscillator", premium="SMI+Ergodic+Indicator/Oscillator"),
		Parameter("spread", "Spread", ["spread"], premium="Spread"),
		Parameter("srsi", "Stochastic RSI", ["srsi", "stochrsi", "stochasticrsi"], tradingview="STD;Stochastic_RSI", premium="Stochastic+RSI"),
		Parameter("stochastic", "Stochastic", ["stochastic", "stoch"], tradingview="STD;Stochastic", premium="Stochastic"),
		Parameter("standarderror", "Standard Error", ["standarderror"], premium="Standard+Error"),
		Parameter("stdev", "Standard Deviation", ["stdev", "stddev", "standarddeviation"], premium="Standard+Deviation"),
		Parameter("supertrend", "Supertrend", ["supertrend"], tradingview="STD;Supertrend", premium="SuperTrend"),
		Parameter("standardrrrorbands", "Standard Error Bands", ["standardrrrorbands"], premium="Standard+Error+Bands"),
		Parameter("tema", "Triple EMA", ["tema", "tripleema"], tradingview="STD;TEMA", premium="Triple+EMA"),
		Parameter("technicalratings", "Technical Ratings", ["tr", "technicalratings"], tradingview="STD;Technical%1Ratings"),
		Parameter("tma", "Triple MA", ["tma", "triplema"], premium="Moving+Average+Triple"),
		Parameter("trix", "Triple Exponential Average", ["trix", "txa", "texa", "tripleexponentialaverage"], tradingview="STD;TRIX", premium="TRIX"),
		Parameter("typicalprice", "Typical Price", ["typicalprice", "tp"], premium="Typical+Price"),
		Parameter("truestrengthindicator", "True Strength Index", ["tsi", "truestrengthindex", "truestrengthindicator"], tradingview="STD;True%1Strength%1Indicator", premium="True+Strength+Indicator"),
		Parameter("trendstrengthindex", "Trend Strength Index", ["trendstrengthindex"], premium="Trend+Strength+Index"),
		Parameter("ultimate", "Ultimate Oscillator", ["ultimate", "uo", "ultimateoscillator"], tradingview="STD;Ultimate_Oscillator", premium="Ultimate+Oscillator"),
		Parameter("updownvolume", "Up/Down Volume", ["up/downvolume", "updown", "udv", "updownvolume"], tradingview="STD;UP_DOWN_Volume"),
		Parameter("vap", "Visible Average Price", ["vap", "visibleaverageprice"], tradingview="STD;Visible%1Average%1Price"),
		Parameter("volatility", "Volatility Index", ["volatility", "vi", "volatilityindex"], tradingview="STD;Relative_Volatility_Index", premium="Volatility+Index"),
		Parameter("volatilityclose-to-close", "Volatility Close-to-Close", ["volatilityclose-to-close"], premium="Volatility+Close-to-Close"),
		Parameter("volatilityzerotrendclose-to-close", "Volatility Zero Trend Close-to-Close", ["volatilityzerotrendclose-to-close"], premium="Volatility+Zero+Trend+Close-to-Close"),
		Parameter("volatilityo-h-l-c", "Volatility O-H-L-C", ["volatilityo-h-l-c"], premium="Volatility+O-H-L-C"),
		Parameter("volatilitystop", "Volatility Stop", ["vstop", "volatilitystop"], tradingview="STD;Volatility_Stop"),
		Parameter("volumeoscillator", "Volume Oscillator", ["volosc", "volumeoscillator"], tradingview="STD;Volume%1Oscillator", premium="Volume+Oscillator"),
		Parameter("volumeprofile", "Volume Profile", ["volumeprofile", "vpvr", "tpo", "marketprofile"], premium="Volume+Profile+Visible+Range@row+size:f:100"),
		Parameter("vortex", "Vortex", ["vortex"], tradingview="STD;Vortex%1Indicator", premium="Vortex+Indicator"),
		Parameter("vwap", "VWAP", ["vwap"], tradingview="STD;VWAP", premium="VWAP"),
		Parameter("vwma", "VWMA", ["mavw", "vw", "vwma"], tradingview="STD;VWMA", premium="VWMA"),
		Parameter("williamsa", "Williams Alligator", ["williamsa", "williamsalligator", "wa"], tradingview="STD;Williams_Alligator", premium="Williams+Alligator"),
		Parameter("williamsf", "Williams Fractal", ["williamsf", "williamsfractal", "wf"], tradingview="STD;Whilliams_Fractals", premium="Williams+Fractal"),
		Parameter("williamsr", "Williams %R", ["williamsr", "wr", "williams%r"], tradingview="STD;Willams_R", premium="Williams+%R"),
		Parameter("wma", "Weighted Moving Average", ["wma", "weightedmovingaverage"], tradingview="STD;WMA", premium="Moving+Average+Weighted"),
		Parameter("wcci", "Woodies CCI", ["wcci", "woodiescci"], tradingview="STD;Woodies%1CCI"),
		Parameter("zz", "Zig Zag", ["zz", "zigzag"], tradingview="STD;Zig_Zag", premium="ZigZag")
	],
	"style": [
		Parameter("hidevolume", "no volume", ["hv", "nv", "novol", "hidevolume"], tradingview="1", premium="1"),
		Parameter("theme", "light theme", ["light", "white"], tradingview="light", premium="light", relay="light", alternativeme="light", cnnbusiness="light", tradinglite="light"),
		Parameter("theme", "dark theme", ["dark", "black"], tradingview="dark", premium="dark", relay="dark", alternativeme="dark", cnnbusiness="dark", tradinglite="dark"),
		Parameter("chartType", "bars", ["bars", "bar"], tradingview="0"),
		Parameter("chartType", "candles", ["candles", "candle", "candlestick"], tradingview="1", premium="1"),
		Parameter("chartType", "line", ["line"], tradingview="2", premium="2"),
		Parameter("chartType", "area", ["area"], tradingview="3", premium="3"),
		Parameter("chartType", "renko", ["renko"], tradingview="4"),
		Parameter("chartType", "kagi", ["kagi"], tradingview="5"),
		Parameter("chartType", "point & figure", ["point", "figure", "pf", "paf", "point&figure"], tradingview="6"),
		Parameter("chartType", "line break", ["break", "linebreak", "lb"], tradingview="7"),
		Parameter("chartType", "heikin ashi", ["heikin", "heiken", "heikinashi", "heikenashi", "ashi", "ha"], tradingview="8", premium="8"),
		Parameter("chartType", "hollow candles", ["hollow"], tradingview="9", premium="9"),
		Parameter("chartType", "baseline", ["baseline"], premium="10"),
		Parameter("chartType", "hiLo", ["hilo"], premium="12"),
		Parameter("log", "log chart", ["log", "logarithmic"], tradingview=True, premium=True, alternativeme=True, cnnbusiness=True),
		Parameter("extended", "extended hours", ["extended", "post", "pre", "extendedhours"], premium=True),
		Parameter("wide", "wide chart", ["wide"], tradinglite=True, tradingview=True, premium=True, alternativeme=True, cnnbusiness=True),
	],
	"preferences": [
		Parameter("heatmapIntensity", "whales heatmap intensity", ["whale", "whales"], tradinglite=(50,100)),
		Parameter("heatmapIntensity", "low heatmap intensity", ["low"], tradinglite=(10,100)),
		Parameter("heatmapIntensity", "normal heatmap intensity", ["normal"], tradinglite=(0,85)),
		Parameter("heatmapIntensity", "medium heatmap intensity", ["medium", "med"], tradinglite=(0,62)),
		Parameter("heatmapIntensity", "high heatmap intensity", ["high"], tradinglite=(0,39)),
		Parameter("heatmapIntensity", "crazy heatmap intensity", ["crazy"], tradinglite=(0,16)),
		Parameter("forcePlatform", "request chart on TradingLite", ["tl", "tradinglite"], tradinglite=True),
		Parameter("forcePlatform", "request chart on TradingView", ["tv", "tradingview"], tradingview=True),
		Parameter("forcePlatform", "request chart on TradingView Premium", ["tv", "tradingview", "prem", "premium", "tvp", "tradingviewpremium"], premium=True),
		Parameter("forcePlatform", "request chart on Alternative.me", ["am", "alternativeme", "crypto"], alternativeme=True),
		Parameter("forcePlatform", "request chart on CNN Business", ["cnn", "cnnbusiness", "stocks"], cnnbusiness=True),
	]
}
DEFAULTS = {
	"Alternative.me": {
		"timeframes": [
			AbstractRequest.find_parameter_by_id(1440, PARAMETERS, "Alternative.me", parameterType="timeframes")
		],
		"indicators": [],
		"style": [],
		"preferences": []
	},
	"CNN Business": {
		"timeframes": [
			AbstractRequest.find_parameter_by_id(1440, PARAMETERS, "CNN Business", parameterType="timeframes")
		],
		"indicators": [],
		"style": [],
		"preferences": []
	},
	"TradingLite": {
		"timeframes": [
			AbstractRequest.find_parameter_by_id(60, PARAMETERS, "TradingLite", parameterType="timeframes")
		],
		"indicators": [],
		"style": [
			AbstractRequest.find_parameter_by_id("theme", PARAMETERS, "TradingLite", name="dark theme", parameterType="style")
		],
		"preferences": [
			AbstractRequest.find_parameter_by_id("heatmapIntensity", PARAMETERS, "TradingLite", name="normal heatmap intensity", parameterType="preferences")
		]
	},
	"TradingView Premium": {
		"timeframes": [
			AbstractRequest.find_parameter_by_id(60, PARAMETERS, "TradingView Premium", parameterType="timeframes")
		],
		"indicators": [],
		"style": [
			AbstractRequest.find_parameter_by_id("theme", PARAMETERS, "TradingView Premium", name="dark theme", parameterType="style"),
			AbstractRequest.find_parameter_by_id("chartType", PARAMETERS, "TradingView Premium", name="candles", parameterType="style")
		],
		"preferences": []
	},
	"TradingView Relay": {
		"timeframes": [
			AbstractRequest.find_parameter_by_id(60, PARAMETERS, "TradingView Relay", parameterType="timeframes")
		],
		"indicators": [],
		"style": [
			AbstractRequest.find_parameter_by_id("theme", PARAMETERS, "TradingView Relay", name="dark theme", parameterType="style")
		],
		"preferences": []
	},
	"TradingView": {
		"timeframes": [
			AbstractRequest.find_parameter_by_id(60, PARAMETERS, "TradingView", parameterType="timeframes")
		],
		"indicators": [],
		"style": [
			AbstractRequest.find_parameter_by_id("theme", PARAMETERS, "TradingView", name="dark theme", parameterType="style"),
			AbstractRequest.find_parameter_by_id("chartType", PARAMETERS, "TradingView", name="candles", parameterType="style")
		],
		"preferences": []
	}
}


class ChartRequestHandler(AbstractRequestHandler):
	def __init__(self, tickerId, platforms, assetClass=None, defaults={}):
		super().__init__(platforms, assetClass)
		for platform in platforms:
			self.requests[platform] = ChartRequest(tickerId, platform, defaults)

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

			if platform == "Alternative.me":
				if request.ticker.get("id") not in ["FGI"]: request.set_error(None, isFatal=True)

			elif platform == "CNN Business":
				if request.ticker.get("id") not in ["FGI"]: request.set_error(None, isFatal=True)

			elif platform == "TradingLite":
				if not bool(request.exchange):
					request.set_error("TradingLite currently only supports cryptocurrency markets on supported exchanges.", isFatal=True)
				elif request.ticker.get("symbol") is None:
					request.set_error(f"Requested chart for `{request.ticker.get('id')}` is not available.", isFatal=True)
				elif request.exchange.get("id") in ["binanceusdm", "binancecoinm", "okex5", "kucoin"]:
					request.set_error(f"{request.exchange.get('name')} exchange is not available. ||Yet? Let TradingLite know you want it!||", isFatal=True)

			elif platform == "TradingView Premium":
				if styles["chartType"] == "6" and styles.get("log", False):
					request.set_error("Point & Figure chart can't be viewed in log scale.", isFatal=True)

				indicators = request.indicators
				parameters = request.numericalParameters
				lengths = {i: [] for i in range(len(indicators))}
				cursor = len(parameters) - 1
				for i in reversed(range(len(indicators))):
					while parameters[cursor] != -1:
						lengths[i].insert(0, parameters[cursor])
						cursor -= 1
					cursor -= 1

					if indicators[i].dynamic is not None and len(lengths[i]) > len(indicators[i].dynamic):
						request.set_error(f"{indicators[i].name} indicator takes in `{len(indicators[i].dynamic)}` {'parameters' if len(indicators[i].dynamic) > 1 else 'parameter'}, but `{len(lengths[i])}` were given.", isFatal=True)
						break

				if len(indicators) == 0 and len(parameters) != 0:
					request.set_error(f"`{str(parameters[0])[:229]}` is not a valid argument.", isFatal=True)

			elif platform == "TradingView Relay":
				pass

			elif platform == "TradingView":
				if styles["chartType"] == "6" and styles.get("log", False):
					request.set_error("Point & Figure chart can't be viewed in log scale.", isFatal=True)


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
		d["requestCount"] = len(d["timeframes"].get(d.get("currentPlatform"), []))

		return d


class ChartRequest(AbstractRequest):
	def __init__(self, tickerId, platform, defaults):
		super().__init__(platform)
		self.tickerId = tickerId
		self.ticker = {}
		self.exchange = {}

		self.timeframes = []
		self.indicators = []
		self.styles = []
		self.preferences = []
		self.numericalParameters = []

		self.currentTimeframe = None
		self.hasExchange = False

		self.defaults = {
			"timeframes": [
				AbstractRequest.find_parameter_by_trigger(defaults.get("timeframe"), PARAMETERS, self.platform, parameterType="timeframes")
			],
			"indicators": [
				AbstractRequest.find_parameter_by_trigger(e, PARAMETERS, self.platform, parameterType="indicators")
				for e in defaults.get("indicators", [])
			],
			"style": [
				AbstractRequest.find_parameter_by_trigger(e, PARAMETERS, self.platform, parameterType="style")
				for e in [defaults.get("theme"), defaults.get("chartType")]
			],
			"preferences": []
		}

	async def process_argument(self, argument):
		# None None - No successeful parse
		# None True - Successful parse and add
		# "" False - Successful parse and error
		# None False - Successful parse and breaking error

		finalOutput = None

		responseMessage, success = await self.add_timeframe(argument)
		if responseMessage is not None: finalOutput = responseMessage
		elif success: return

		responseMessage, success = await self.add_indicator(argument)
		if responseMessage is not None: finalOutput = responseMessage
		elif success: return

		responseMessage, success = await self.add_style(argument)
		if responseMessage is not None: finalOutput = responseMessage
		elif success: return

		responseMessage, success = await self.add_preferences(argument)
		if responseMessage is not None: finalOutput = responseMessage
		elif success: return

		responseMessage, success = await self.add_exchange(argument)
		if responseMessage is not None: finalOutput = responseMessage
		elif success: return

		responseMessage, success = await self.add_numerical_parameters(argument)
		if responseMessage is not None: finalOutput = responseMessage
		elif success: return

		if finalOutput is None:
			self.set_error(f"`{argument[:229]}` is not a valid argument.", isFatal=True)
		elif finalOutput.startswith("`Request Chart"):
			self.set_error(None, isFatal=True)
		else:
			self.set_error(finalOutput)

	async def process_ticker(self, assetClass):
		updatedTicker, error = None, None
		try:
			updatedTicker, error = await match_ticker(self.tickerId, self.exchange.get("id"), self.platform, assetClass)
		except:
			print(format_exc())
			error = "Something went wrong while processing the requested ticker."

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
					requiresPro = "Advanced Charting"
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
				if self.platform != "TradingView Premium":
					responseMessage = "Indicator parameters can only be changed on TradingView Premium."
					return responseMessage, False
				else:
					self.numericalParameters.append(int(length.group()))
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
			if self.platform != "TradingView Premium":
				responseMessage = "Indicator parameters can only be changed on TradingView Premium."
				return responseMessage, False
			self.numericalParameters.append(numericalParameter)
			return None, True
		except: return None, None

	def set_default_for(self, t):
		if t == "timeframes" and len(self.timeframes) == 0:
			userDefaults = [e for e in self.defaults.get("timeframes") if e is not None]
			if len(userDefaults) > 0:
				for parameter in userDefaults:
					if not self.has_parameter(parameter.id, self.timeframes):
						self.timeframes.append(parameter)
			else:
				for parameter in DEFAULTS.get(self.platform, {}).get(t, []):
					if not self.has_parameter(parameter.id, self.timeframes):
						self.timeframes.append(parameter)
		elif t == "indicators" and len(self.indicators) == 0:
			userDefaults = [e for e in self.defaults.get("indicators") if e is not None]
			if len(userDefaults) > 0:
				for parameter in userDefaults:
					self.indicators.append(parameter)
					self.numericalParameters.append(-1)
			else:
				for parameter in DEFAULTS.get(self.platform, {}).get(t, []):
					if not self.has_parameter(parameter.id, self.indicators):
						self.indicators.append(parameter)
						self.numericalParameters.append(-1)
		elif t == "style":
			userDefaults = [e for e in self.defaults.get("style") if e is not None]
			if len(userDefaults) > 0:
				for parameter in userDefaults:
					if not self.has_parameter(parameter.id, self.styles):
						self.styles.append(parameter)
			else:
				for parameter in DEFAULTS.get(self.platform, {}).get(t, []):
					if not self.has_parameter(parameter.id, self.styles):
						self.styles.append(parameter)
		elif t == "preferences":
			userDefaults = [e for e in self.defaults.get("preferences") if e is not None]
			if len(userDefaults) > 0:
				for parameter in userDefaults:
					if not self.has_parameter(parameter.id, self.preferences):
						self.preferences.append(parameter)
			else:
				for parameter in DEFAULTS.get(self.platform, {}).get(t, []):
					if not self.has_parameter(parameter.id, self.preferences):
						self.preferences.append(parameter)

	def prepare_indicators(self):
		parsed = [e.parsed[self.platform] for e in self.indicators]
		if "" in parsed or len(self.indicators) == 0:
			return ""

		indicators = ""

		if self.platform in "TradingView":
			indicators = "\u001f".join(parsed)

		elif self.platform == "TradingView Premium":
			lengths = {i: [] for i in range(len(self.indicators))}
			cursor = len(self.numericalParameters) - 1

			_indicators = []
			for i in reversed(range(len(self.indicators))):
				while self.numericalParameters[cursor] != -1:
					lengths[i].insert(0, ["", self.numericalParameters[cursor]])
					cursor -= 1
				cursor -= 1

				if self.indicators[i].dynamic is not None and lengths[i] != 0:
					for j in range(0, len(lengths[i])):
						lengths[i][j][0] = self.indicators[i].dynamic[j][0]
					for j in range(len(lengths[i]), len(self.indicators[i].dynamic)):
						lengths[i].append(list(self.indicators[i].dynamic[j]))

				_indicators.insert(0, f"{parsed[i]}@{';'.join([f'{n}{l}' for n, l in lengths[i]])}")

			indicators = "&studies=" + ",".join(_indicators)

		return indicators


	def to_dict(self):
		d = {
			"ticker": self.ticker,
			"exchange": self.exchange,
			"timeframes": [e.parsed[self.platform] for e in self.timeframes],
			"indicators": self.prepare_indicators(),
			"styles": self.prepare_styles(),
			"preferences": self.prepare_preferences(),
			"numericalParameters": self.numericalParameters,
			"currentTimeframe": self.currentTimeframe
		}
		return d