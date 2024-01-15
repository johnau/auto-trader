data_folder = "./binance/data"

# All current binance symbols (from binance website 30 December 2023)
symbols = [
    "ZRXUSDT", "1INCHUSDT", "AAVEUSDT", "ADXUSDT", "ACHUSDT",
    "ALGOUSDT", "TLMUSDT", "ALPINEUSDT", "FORTHUSDT", "ANKRUSDT",
    "APEUSDT", "API3USDT", "APTUSDT", "ANTUSDT", "ARBUSDT", "ASTRUSDT",
    "AUDIOUSDT", "AVAXUSDT", "AXLUSDT", "AXSUSDT", "BALUSDT", "BNTUSDT",
    "BANDUSDT", "BONUSDT", "BATUSDT", "BICOUSDT", "BTCUSDT", "BCHUSDT",
    "BLURUSDT", "BNBUSDT", "BOSONUSDT", "BTRSTUSDT", "ADAUSDT", "CTSIUSDT",
    "CELRUSDT", "CELOUSDT", "LINKUSDT", "CHZUSDT", "CLVUSDT", "COMPUSDT",
    "ATOMUSDT", "COTIUSDT", "CUDOSUSDT", "CRVUSDT", "DAIUSDT", "DASHUSDT",
    "MANAUSDT", "DIAUSDT", "DGBUSDT", "DOGEUSDT", "XECUSDT", "EGLDUSDT",
    "ENJUSDT", "EOSUSDT", "ETHUSDT", "ETCUSDT", "ENSUSDT", "FTMUSDT",
    "PORTOUSDT", "FETUSDT", "FILUSDT", "FLOKIUSDT", "FLOWUSDT", "FLUXUSDT",
    "FORTUSDT", "GALAUSDT", "GALUSDT", "JAMUSDT", "GTCUSDT", "GLMUSDT",
    "ONEUSDT", "HBARUSDT", "ZENUSDT", "ICXUSDT", "RLCUSDT", "ILVUSDT",
    "IMXUSDT", "ICPUSDT", "IOSTUSDT", "MIOTAUSDT", "KDAUSDT", "KAVAUSDT",
    "KSMUSDT", "KNCUSDT", "LAZIOUSDT", "LOKAUSDT", "LDOUSDT", "LSKUSDT",
    "LTCUSDT", "LPTUSDT", "LOOMUSDT", "LRCUSDT", "LTOUSDT", "MKRUSDT",
    "PONDUSDT", "MASKUSDT", "DARUSDT", "MXCUSDT", "ALICEUSDT", "XNOUSDT",
    "NEARUSDT", "NEOUSDT", "NMRUSDT", "ROSEUSDT", "OCEANUSDT", "ONGUSDT",
    "ONTUSDT", "OPUSDT", "ORBSUSDT", "OXTUSDT", "OGNUSDT", "TRACUSDT",
    "PAXGUSDT", "DOTUSDT", "MATICUSDT", "POLYXUSDT", "PROMUSDT", "QTUMUSDT",
    "QNTUSDT", "RADUSDT", "RVNUSDT", "REEFUSDT", "RENUSDT", "RNDRUSDT",
    "REQUSDT", "SANTOSUSDT", "SHIBUSDT", "SKLUSDT", "SLPUSDT", "SOLUSDT",
    "STGUSDT", "XLMUSDT", "STMXUSDT", "STORJUSDT", "SUIUSDT", "RAREUSDT",
    "SUSHIUSDT", "SNXUSDT", "SYSUSDT", "USDTUSDT", "XRPUSDT", "XTZUSDT",
    "GRTUSDT", "SANDUSDT", "TFUELUSDT", "THETAUSDT", "TUSDT", "TUSDUSDT",
    "UNIUSDT", "USDCUSDT", "VETUSDT", "VTHOUSDT", "VITEUSDT", "VOXELUSDT",
    "WAVESUSDT", "WAXPUSDT", "WBTCBTC", "YFIUSDT", "ZECUSDT", "ZILUSDT"
]

intervals = [
    # "1m", "3m", "5m", "15m", "30m", "1h", "2h", "4h", "6h", "8h", "12h", "1d", "3d", "1w", "1mo" # Full set of available intervals
    "1m", "5m", "15m", "30m", "1h", "4h", "1d", "1w" # This subset should be more than sufficient
]

kline_opentime = "open_time"
kline_openprice = "open_price"
kline_highprice=  "high_price"
kline_lowprice=  "low_price"
kline_closeprice= "close_price"
kline_vol = "volume"
kline_closetime = "close_time"