import os
import requests
from itertools import product
import sys
from itertools import product
from concurrent.futures import ThreadPoolExecutor, as_completed
from properties import data_folder, symbols, intervals

max_threads = 10
base_url = "https://data.binance.vision"

start_year, end_year = 2018, 2023
start_month, end_month = 1, 12

# total_downloads = len(symbols) * len(intervals) * (end_year - start_year) * (end_month - start_month + 1)

def update_console(msg: str):
    sys.stdout.write('\033[F')  # Move the cursor up one line
    sys.stdout.write('\033[K') 
    # p = float(count/total_downloads*100)
    # print(f"{p:.2f}% completed")
    print(f":: {msg}")

    return

def download_file(url, filename):
    msg = ""
    if os.path.exists(filename):
        msg = f"File already exists: {filename}"
    else:
        response = requests.get(url)
        if response.status_code == 200:
            with open(filename, 'wb') as file:
                file.write(response.content)
            msg = filename
        else:
            msg = f"Failed to download {filename}. Status code: {response.status_code}"
    return msg

def run():
    print(f"Downloading Binance Historical Data from {start_month}-{start_year} to {end_month}-{end_year}...")
    print("0% complete")
    print("::")
    
    with ThreadPoolExecutor(max_threads) as executor:
        futures = []
        count = 1
        for symbol, interval, year, month in product(symbols, intervals, range(start_year, end_year + 1), range(start_month, end_month + 1)):
            url = f"{base_url}/data/spot/monthly/klines/{symbol}/{interval}/{symbol}-{interval}-{year}-{month:02d}.zip"
            filename = f"{data_folder}/{symbol}_{interval}_{year}_{month:02d}.zip"

            future = executor.submit(download_file, url, filename)
            future.add_done_callback(lambda f: update_console(f.result()))
            futures.append(future)

        try:
            total = len(futures)
            count = 0
            for future in as_completed(futures):
                count += 1
                future.result()
              
                p = float(count/total*100)
                print(f"{p:.2f}% completed")
        except KeyboardInterrupt:
            print("Download interrupted by user.")


if __name__ == "__main__":
    run()