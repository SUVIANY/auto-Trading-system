from pymongo import MongoClient;from binance.client import Client;import requests;import pandas as pd
client= Client(api_key="-",api_secret="-")
data  = MongoClient
order = MongoClient
panel = MongoClient
logs  = MongoClient
tickers = MongoClient

def notifyMe(message) :
    try : 
        url = f'https://api.telegram.org/bot2022290712:AAH_zCy9PUtBXRC46rZ6p8EMzqepKxu6xwE/sendMessage?chat_id=@nanoATS&text={message}'
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


#data.delete_many({})
#panel.insert_one({"_id":"controlpanel","system":"OFF"})
#panel.insert_one({"_id":"BTCPSG","psg":0})
#order.insert_one({"_id":"buylimit","coins":[]})
#order.update_one({"_id":"buylimit"},{"$addToSet":{"coins":{"coinName":"SOLUSDT","price":213,"orderId":1537202387} }})
#order.update_one({"_id":"buylimit"},{"$addToSet":{"coins":{"coinName":"SOLUSDT","price":"133","usdt":200,"orderId":1537202387,"tppsg":20,"reach":10,"term":panel.find_one({"_id":"controlpanel"})["term"]}}})
#order.update_one({"_id":"buylimit","coins":{"$elemMatch":{"coinName":"SOLUSDT"}}},{"$set":{"coins.$.reach":0}})
#tickers.delete_many({})
#tickers.insert_one({"_id":"discounts","tickers":[]})
#tickers.insert_one({"_id":"safe","tickers":[]})
#tickers.insert_one({"_id":"risk","tickers":[]})
#tickers.update_one({"_id":"safe"},{"$addToSet":{"tickers":"SOLUSDT"}})
