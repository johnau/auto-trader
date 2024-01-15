from properties import *
from itertools import product
from database import DatabaseManager
from datetime import datetime
from candlestick_chart import CandlestickChart
from load_historical_data import HistoricalDataFetcher


# UNCOMMENT THESE LINES IF RUNNING FOR THE FIRST TIME OR AFTER 1 MONTH OF INACTIVITY - takes 2 hours
# import fetch_historical_data
# fetch_historical_data.run()

# CREATE ALL TABLES IF REQUIRED
db = DatabaseManager()
for s, i in product(symbols, intervals):
    db.create_table(s, i)

# DEBUG, LIST ALL TABLES CREATED IN DB
all_tables = db.list_tables()
print("List of Tables:")
for table_name in all_tables:
    print(table_name)

# GETS THE CURRENT MONTHS DATA FOR ALL ASSETS IF NOT IN DB
    # check the db for the latest timestamp and assume all before it are filled
    # collect data after said timestamp or back to start of month if there are none existing
normal_run = False
if normal_run:
    from fetch_current_data import CurrentDataFetcher
    for s, i in product(symbols, intervals):
        highest_ts = db.get_highest_opentime(s, i) # will update the latest candle
        if highest_ts:
            # print(f"{s} {i} : {datetime.utcfromtimestamp(highest_ts/1000).strftime('%d %b %Y %H:%M:%S')}")
            cdf = CurrentDataFetcher(s, i, int(highest_ts))
        else:
            cdf = CurrentDataFetcher(s, i)
        cdf.run()
        latest_data_list = cdf.data
        # print(f"Adding {len(latest_data_list)} kline entries for {s.upper()}_{i.upper()} to the database")
        
        # STORE IN DB
        db.submit(s, i, latest_data_list)
    
    # When processing looks at data, it will first look to the database for data, and then fetch additional data from the zip files
# for s,i in product(symbols, intervals):
#     data = db.fetch_candle_data(s, i)
#     csc = CandlestickChart(s, i, data)
#     csc.plot_candlestick()

if not normal_run:
    symbol1 = "ICP"
    symbol2 = "USDT"
    timeframe = "1h"
    hd = HistoricalDataFetcher(symbol1, symbol2, timeframe)
    historical_data = hd.get_historical_data()
    recent_data = db.fetch_candle_data(symbol1+symbol2, timeframe)
    print(historical_data[0])
    print(recent_data[0])
    keys_to_keep = list(recent_data[0].keys())
    combined_data = [{**entry, **{key: None for key in keys_to_keep if key not in entry}} for entry in historical_data]
    combined_data.extend(recent_data)
    # combined_data = historical_data.extend(recent_data)

    csc = CandlestickChart(symbol1+symbol2, timeframe, combined_data)
    csc.plot_candlestick()    