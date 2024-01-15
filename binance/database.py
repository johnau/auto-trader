import sqlite3
from properties import *

replace_numeric_with_word = lambda s: s.replace(s[0], {'1': 'ONE', '2': 'TWO', '3': 'THREE', '4': 'FOUR', '5': 'FIVE', '6': 'SIX', '7': 'SEVEN', '8': 'EIGHT', '9': 'NINE', '0': 'ZERO'}.get(s[0], s), 1) if s and s[0].isdigit() else s


class DatabaseManager:
    def __init__(self, db_path=data_folder+'/kline_data.db'):
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()

    def create_table(self, pair: str, interval: str):
        table_name = self._table_name(pair, interval)
        create_table_query = f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            open_time INTEGER PRIMARY KEY DESC,
            open_price REAL,
            high_price REAL,
            low_price REAL,
            close_price REAL,
            volume REAL,
            close_time INTEGER
        )
        '''
        self.cursor.execute(create_table_query)

    def _table_name(self, pair: str, interval: str):
        return replace_numeric_with_word(f"{pair.upper()}_{interval.upper()}")

    def submit(self, pair: str, interval: str, kline_data_list):
        '''
            Candles with duplicate timestamp will be ignored.  
            Updated values will overwrite.
        '''
        if not kline_data_list:
            return

        table_name = self._table_name(pair, interval)
        # self.create_table(table_name)

        insert_query = f'''
        INSERT OR IGNORE INTO {table_name} (
            open_time, open_price, high_price, low_price, close_price, volume, close_time
        ) VALUES (
            ?, ?, ?, ?, ?, ?, ?
        )
        ON CONFLICT(open_time) DO UPDATE SET
            high_price = excluded.high_price,
            low_price = excluded.low_price,
            close_price = excluded.close_price,
            volume = excluded.volume,
            close_time = excluded.close_time
        '''

        insert_data = [
            (
                kline_data[kline_opentime],
                kline_data[kline_openprice],
                kline_data[kline_highprice],
                kline_data[kline_lowprice],
                kline_data[kline_closeprice],
                kline_data[kline_vol],
                kline_data[kline_closetime]
            ) for kline_data in kline_data_list
        ]

        self.cursor.executemany(insert_query, insert_data)
        self.connection.commit()

    def fetch_candle_data(self, pair: str, interval: str):
        table_name = self._table_name(pair, interval)
        fetch_query = f'''
        SELECT * FROM {table_name}
        '''
        self.cursor.execute(fetch_query)
        candle_data_tuples = self.cursor.fetchall()

        column_names = ["open_time", "open_price", "high_price", "low_price", "close_price", "volume", "close_time"]
        mapped_data = [dict(zip(column_names, row)) for row in candle_data_tuples]

        return mapped_data

    def get_highest_opentime(self, pair, interval) -> int:
        table_name = self._table_name(pair,interval)
        query = f'''
        SELECT MAX(open_time) FROM {table_name}
        '''
        self.cursor.execute(query)
        highest_timestamp = self.cursor.fetchone()[0]
        if highest_timestamp:
            return int(highest_timestamp)
        else:
            return None

    def get_second_highest_opentime(self, pair, interval) -> int:
        table_name = self._table_name(pair, interval)
        query = f'''
        SELECT open_time FROM {table_name}
        ORDER BY open_time DESC
        LIMIT 1 OFFSET 1
        '''
        self.cursor.execute(query)
        second_highest_timestamp = self.cursor.fetchone()
        if second_highest_timestamp:
            return int(second_highest_timestamp[0])
        else:
            return None

    def list_tables(self):
        query = "SELECT name FROM sqlite_master WHERE type='table';"
        self.cursor.execute(query)
        tables = self.cursor.fetchall()
        return [table[0] for table in tables]
        
    def close_connection(self):
        self.connection.close()