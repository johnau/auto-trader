import pandas as pd
import plotly.graph_objects as go
from bokeh.plotting import figure, show, output_file
from bokeh.models import ColumnDataSource, DatetimeTickFormatter, Span, FixedTicker, SingleIntervalTicker, AdaptiveTicker
from properties import *
import math

class CandlestickChart:
    def __init__(self, pair: str, interval: str, data: []):
        self.pair = pair
        self.interval = interval
        self.data = pd.DataFrame(data)
        pass

    def plot_candlestick(self):
        # Convert data to a DataFrame
        df = self.data
        output_file(f"{data_folder}/charts/{self.pair}_{self.interval}.html")
        # Convert timestamps to datetime
        df['open_time'] = pd.to_datetime(df['open_time'], unit='ms')
        df['close_time'] = pd.to_datetime(df['close_time'], unit='ms')
        df['color'] = ['#00ffcc' if close > open else 'black' for open, close in zip(df['open_price'], df['close_price'])]

        # Create a ColumnDataSource
        source = ColumnDataSource(df)

        p = figure(title=f'{self.pair} - {self.interval} Candlestick Chart',
                   x_axis_label='Time', y_axis_label='Price',
                   x_axis_type='datetime', width_policy='max', height=400, sizing_mode='stretch_both')

        # Body lines
        p.segment(x0='open_time', y0='open_price', x1='open_time', y1='close_price',
                  source=source, line_color='color', line_width=4)

        # Wick lines
        p.segment(x0='open_time', y0='high_price', x1='open_time', y1='low_price',
                  source=source, line_color='color', line_width=1)

        p.xaxis.formatter = DatetimeTickFormatter(days="%d %b %Y", hours="%d %b %Y %H:%M:%S", months="%d %b %Y", years="%d %b %Y")

        last_close_price = df['close_price'].iloc[-1]
        last_price_color = '#00ffcc' if df['close_price'].iloc[-1] > df['open_price'].iloc[-1] else 'black'
        
        # p.yaxis.ticker = AdaptiveTicker(base=0.5 * 10 ** math.ceil(math.log10(last_close_price))) # make this adjust based on current price
        p.yaxis.ticker = AdaptiveTicker(base=2)
        p.xaxis.ticker = AdaptiveTicker(base=2)
        # p.yaxis.ticks += last_close_price
        # p.yaxis.ticker = FixedTicker(ticks=[last_close_price])
        current_price_line = Span(location=last_close_price, dimension='width', line_color=last_price_color, line_width=2)
        p.add_layout(current_price_line)

        show(p)


# from random import randint
# from bokeh.plotting import figure, curdoc
# from bokeh.models import ColumnDataSource
# from bokeh.driving import count

# # Create a figure
# p = figure(plot_height=350, plot_width=800, title="Live Updating Plot")
# source = ColumnDataSource(data=dict(x=[], y=[]))
# p.circle(x='x', y='y', source=source)

# # Create a callback that updates the plot every second
# @count()
# def update(n):
#     new_data = dict(x=[n], y=[randint(0, 10)])
#     source.stream(new_data, rollover=20)  # Keep only the last 20 points

# # Add the callback to the document
# curdoc().add_periodic_callback(update, 1000)

# # Display the plot
# curdoc().title = "Live Updating Plot"
# curdoc().add_root(p)