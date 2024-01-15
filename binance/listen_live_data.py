import time
import json

def parse_agg_trade_response(response):
    if isinstance(response, str):
        response = json.loads(response)

    parsed_response = {
        "Event Type": response.get("e"),
        "Event Time": response.get("E"),
        "Symbol": response.get("s"),
        "Aggregate Trade ID": response.get("a"),
        "Price": response.get("p"),
        "Quantity": response.get("q"),
        "First Trade ID": response.get("f"),
        "Last Trade ID": response.get("l"),
        "Trade Time": response.get("T"),
        "Is Buyer Market Maker": response.get("m"),
        # Ignoring the "M" field as per your request
    }

    formatted_output = json.dumps(parsed_response, indent=2)
    print(formatted_output)


# from binance.websocket.spot.websocket_api import SpotWebsocketAPIClient

# def message_handler(_, message):
#     print(message)

# my_client = SpotWebsocketAPIClient(on_message=message_handler)

# my_client.ticker(symbol="BTCUSDT", type="FULL")


# time.sleep(100)
# print("closing ws connection")
# my_client.stop()

from binance.websocket.spot.websocket_stream import SpotWebsocketStreamClient

def message_handler(_, message):
    print(parse_agg_trade_response(message))

my_client = SpotWebsocketStreamClient(on_message=message_handler)

# Subscribe to a single symbol stream
my_client.ticker(symbol="btcusdt")
time.sleep(60)
my_client.stop()






