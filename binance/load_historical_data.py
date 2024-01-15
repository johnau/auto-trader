import os
import zipfile
import csv
from datetime import datetime
from pathlib import Path

class HistoricalDataFetcher:
    def __init__(self, symbol1, symbol2, timeframe):
        self.symbol1 = symbol1
        self.symbol2 = symbol2
        self.timeframe = timeframe
        self.columns = ['open_time', 'open_price', 'high_price', 'low_price', 'close_price', 'volume', 'close_time', 'quote_volume', 'count', 'taker_buy_volume', 'taker_buy_quote_volume', 'ignore']

    def read_csv_from_zip(self, zip_path):
        with zipfile.ZipFile(zip_path, 'r') as zip_file:
            csv_file = [file for file in zip_file.namelist() if file.endswith('.csv')][0]
            with zip_file.open(csv_file, 'r') as csvfile:
                reader = csv.DictReader((line.decode('utf-8') for line in csvfile), fieldnames=self.columns)
                return list(reader)

    def get_historical_data(self):
        folder_path = Path('./binance/data')
        pair = f"{self.symbol1.upper()}{self.symbol2.upper()}"
        search = f"{pair}_{self.timeframe}_*.zip"
        files = sorted(
            [file for file in folder_path.glob(search)],
            key=lambda x: (int(x.stem.split('_')[-1]), int(x.stem.split('_')[-2]))
        )

        all_data = []
        for file in files:
            all_data.extend(self.read_csv_from_zip(file))

        # Convert data types
        for entry in all_data:
            entry['open_time'] = int(entry['open_time'])
            entry['open_price'] = float(entry['open_price'])
            entry['high_price'] = float(entry['high_price'])
            entry['low_price'] = float(entry['low_price'])
            entry['close_price'] = float(entry['close_price'])
            entry['volume'] = float(entry['volume'])
            entry['close_time'] = int(entry['close_time'])

        # Sort by timestamp
        all_data.sort(key=lambda x: int(x['open_time']))

        return all_data

# import os
# import zipfile
# import csv
# from datetime import datetime
# from pathlib import Path

# # columns = ['open_time', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_volume', 'count', 'taker_buy_volume', 'taker_buy_quote_volume', 'ignore']
# columns = ['open_time', 'open_price', 'high_price', 'low_price', 'close_price', 'volume', 'close_time', 'quote_volume', 'count', 'taker_buy_volume', 'taker_buy_quote_volume', 'ignore']

# def read_csv_from_zip(zip_path):

#     with zipfile.ZipFile(zip_path, 'r') as zip_file:
#         csv_file = [file for file in zip_file.namelist() if file.endswith('.csv')][0]
#         with zip_file.open(csv_file, 'r') as csvfile:
#             reader = csv.DictReader((line.decode('utf-8') for line in csvfile), fieldnames=columns)
#             return list(reader)

# def get_historical_data(symbol1, symbol2, timeframe):
#     folder_path = Path('./binance/data')
#     pair = f"{symbol1.upper()}{symbol2.upper()}"
#     search = f"{pair}_{timeframe}_*.zip"
#     files = sorted(
#         [file for file in folder_path.glob(search)],
#         key=lambda x: (int(x.stem.split('_')[-1]), int(x.stem.split('_')[-2]))
#     )

#     all_data = []
#     for file in files:
#         all_data.extend(read_csv_from_zip(file))

#     # Convert data types
#     for entry in all_data:
#         entry['open_time'] = int(entry['open_time'])
#         entry['open_price'] = float(entry['open_price'])
#         entry['high_price'] = float(entry['high_price'])
#         entry['low_price'] = float(entry['low_price'])
#         entry['close_price'] = float(entry['close_price'])
#         entry['volume'] = float(entry['volume'])
#         entry['close_time'] = int(entry['close_time'])

#     # Sort by timestamp
#     all_data.sort(key=lambda x: int(x['open_time']))

#     return all_data
