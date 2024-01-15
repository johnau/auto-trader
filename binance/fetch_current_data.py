import pandas as pd
from binance.spot import Spot
from datetime import datetime
from properties import *

def parse_kline_data(kline_data):
    parsed_data_list = []
    for data in kline_data:
        open_time, open_price, high_price, low_price, close_price, volume, close_time, qav, nts, tbbav, tbqav, _ = data
        parsed_data_list.append({
            kline_opentime: open_time,
            kline_openprice: open_price,
            kline_highprice: high_price,
            kline_lowprice: low_price,
            kline_closeprice: close_price,
            kline_vol: volume,
            kline_closetime: close_time
        })
    return parsed_data_list

def earliest_candle(kline_data_list):
    return min(kline_data_list, key=lambda kline_data: kline_data['open_time'])

def latest_candle(kline_data_list):
    return max(kline_data_list, key=lambda kline_data: kline_data['open_time'])

def print_range(kline_data_list):
    sml = earliest_candle(kline_data_list)
    lrg = latest_candle(kline_data_list)
    if not sml or not lrg:
        print("Error printing range")
        return
    sml_hr = datetime.utcfromtimestamp(sml['open_time'] / 1000).strftime('%d %B %Y %H:%M:%S')
    lrg_hr = datetime.utcfromtimestamp(lrg['open_time'] / 1000).strftime('%d %B %Y %H:%M:%S')
    print(f"The earliest timestamp is {sml['open_time']} (Unix timestamp), which is {sml_hr}.")
    print(f"The latest timestamp is {lrg['open_time']} (Unix timestamp), which is {lrg_hr}.")

def get_utc_start_of_current_month():
    now = datetime.utcnow()
    start_of_month = datetime(now.year, now.month, 1, 0, 0, 0, 0)
    utc_start_of_month = int(start_of_month.timestamp()) * 1000  # Convert to milliseconds
    return utc_start_of_month

def get_utc_start_of_now():
    now = datetime.utcnow()
    utc_now = int(now.timestamp()) * 1000  # Convert to milliseconds
    return utc_now


class CurrentDataFetcher:
    def __init__(self, pair: str, interval: str, starting_timestamp: int = -1):
        self._client = Spot()
        self.pair = pair
        self.interval = interval
        self.starting_timestamp = starting_timestamp
        self._data = []
    
    @property
    def data(self):
        return self._data

    def run(self):
        st = get_utc_start_of_current_month()
        if not self.starting_timestamp < 0:
            st = self.starting_timestamp

        # formatted_date = datetime.utcfromtimestamp(st/1000).strftime("%d %b %Y %H:%M:%S")
        # print(f"Starting with timestamp: {st} ({formatted_date})")

        nt = get_utc_start_of_now() + (1000*60*60*12) # added 12 hours to ensure get everything
        limit = 1000 # max binance
        kline_data_list = []
        while True:
            print(f"? Querying for {self.pair} {self.interval}, currently have {len(kline_data_list)} candles...")
            try:
                response = self._client.klines(self.pair, self.interval, startTime=st, limit=limit)
            except:
                print(f"Error thrown by binance api for {self.pair}_{self.interval}")
                break

            if response:
                partial_kline_data_list = parse_kline_data(response)
                kline_data_list.extend(partial_kline_data_list)
                # print_range(kline_data_list)
                
                if len(partial_kline_data_list) < limit:
                    # Break the loop if the fetched data is less than the limit
                    break
                st = int(partial_kline_data_list[-1]['close_time']) # Set the start time for the next request
            else:
                print(f"No response: {response}")
                break
                        
        if kline_data_list: 
            print(f":: {len(kline_data_list)} new for {self.pair} {self.interval}")
            # print_range(kline_data_list)
            self._data = kline_data_list
        else:
            print(f"No kline data for {self.pair} {self.interval}")
            self._data = []

# Example usage:
# cdf = CurrentDataFetcher("BTCUSDT", "1h")
# cdf.run()