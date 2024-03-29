from pymongo import MongoClient;from binance.client import Client;import requests;import pandas as pd
client= Client(api_key="-",api_secret="-")
data  = MongoClient
order = MongoClient
panel = MongoClient
logs  = MongoClient
tickers = MongoClient

def notifyMe(message) :
    try : 
        url = f'https://api.telegram.org/-:-/sendMessage?chat_id=@-&text={message}'
        requests.post(url)
    except Exception as e :
        print(f"notifyMe\n{e}")

class format() :
    def format_value(valuetoformatx,fractionfactorx):
                Precision = abs(int(f'{fractionfactorx:e}'.split('e')[-1]))
                FormattedValue = float('{:0.0{}f}'.format(valuetoformatx, Precision))
                return FormattedValue
    def pairQtyinfo(ticker):
                try :
                    info = client.get_symbol_info(ticker)
                    minQty = pd.to_numeric(info['filters'][2]['minQty'])
                    return minQty
                except Exception as e :
                    print(f"pairQtyinfo\n{e}")
    def pairPriceinfo(ticker): 
                try :
                    info = client.get_symbol_info(ticker)
                    minPrice = pd.to_numeric(info['filters'][0]['minPrice'])
                    return minPrice
                except Exception as e :
                    print(f"pairPriceinfo\n{e}")


