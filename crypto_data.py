import requests
import json

def cg_historical_api(id):
    api = "https://api.coingecko.com/api/v3/coins/"+id+"/market_chart?vs_currency=usd&days=max"
    try:
        data = requests.get(api,timeout=10).json()
        return data
    except requests.exceptions.RequestException:
        return False
    except (ValueError):
        return False
        
def crypto_chart(id):
    data = cg_historical_api(id)
    if data:
        try:
            mc = data['market_caps']
            
            price = json.dumps(data['prices'])
            volume = json.dumps(data['total_volumes'])
            output = price, volume
        except (IndexError, KeyError, TypeError, ValueError):
            output = "No chart data to display."
    else:
        output = "No chart data to display."
    return output

chart = crypto_chart("bitcoin")
file1 = open("btc_data.txt", "w") 
file1.write(chart[0])
file1.write(chart[1])
file1.close() 

