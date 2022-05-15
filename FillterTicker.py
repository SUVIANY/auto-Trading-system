from Config import tickers,client;import pandas as pd
allticker = ["ICPUSDT","ILVUSDT","REQUSDT","BTCUSDT","ETHUSDT","NEOUSDT","LTCUSDT","QTUMUSDT","ADAUSDT","IOTAUSDT","XLMUSDT","ONTUSDT","ICXUSDT","TFUELUSDT","ONEUSDT","ALGOUSDT","GTOUSDT","DUSKUSDT","COSUSDT","COCOSUSDT","GALAUSDT","MTLUSDT","TOMOUSDT","NKNUSDT","STXUSDT","ARPAUSDT","IOTXUSDT","CTXCUSDT","BCHUSDT","DREPUSDT","LSKUSDT","DENTUSDT","KEYUSDT","DOCKUSDT","WANUSDT","CVCUSDT","BANDUSDT","XTZUSDT","RENUSDT","RVNUSDT","HIVEUSDT","CHRUSDT","ARDRUSDT","MDTUSDT","STMXUSDT","LRCUSDT","PNTUSDT","LRCUSDT","SCUSDT","ZENUSDT","HCUSDT","LTOUSDT","CTSIUSDT","VTHOUSDT","DGBUSDT","DCRUSDT","STORJUSDT","MANAUSDT","BLZUSDT","IRISUSDT","NULSUSDT","LINKUSDT","WAVESUSDT","BTTUSDT","ONGUSDT","HOTUSDT","ZRXUSDT","FETUSDT","BATUSDT","XMRUSDT","KMDUSDT","SANDUSDT","OCEANUSDT","NMRUSDT","DOTUSDT","RSRUSDT","TRBUSDT","KSMUSDT","FIOUSDT","STRATUSDT","AIONUSDT","MBLUSDT","XRPUSDT","EOSUSDT","STPTUSDT","WTCUSDT","DATAUSDT","XZCUSDT","SOLUSDT","OXTUSDT","AVAXUSDT","HNTUSDT","NEARUSDT","FILUSDT","UTKUSDT","ANTUSDT","CTKUSDT","AXSUSDT","DNTUSDT","ZECUSDT","IOSTUSDT","CELRUSDT","DASHUSDT","OMGUSDT","THETAUSDT","ENJUSDT","MITHUSDT","MATICUSDT","STRAXUSDT","AVAUSDT","XEMUSDT","SKLUSDT","MBOXUSDT","CELOUSDT","RIFUSDT","CKBUSDT","FIROUSDT","LITUSDT","SFPUSDT"]

def fillter() :
    while True :
        try :
            for ticker in allticker :
                df = pd.DataFrame(client.get_historical_klines(ticker,"1d","200 days ago UTC"))
                if not df.empty :
                    df.columns = ['Date','Open','High','Low','Close','Volume','IGNORE','Quote_Volume','Trades_Count','BUY_VOL','BUY_VOL_VAL','x'] 
                    df["Close"] = pd.to_numeric(df["Close"]);df["Volume"] = pd.to_numeric(df["Volume"]);df['vc'] = df.Volume * df.Close
                    df[f'vwap48']=round((df['vc'].rolling(window=48).sum())/(df['Volume'].rolling(window=48).sum()),10).fillna(method='bfill')
                    pricenow = float(df.Close.tail(1))
                    vwap48 = df.vwap48.tail(1)
                    psg = float(round(((pricenow/vwap48)-1)*100,2))

                    if psg <= -30 :
                        tickers.update_one({"_id":"discounts"},{"$addToSet":{"tickers":ticker}})
                    if psg >= 20 :
                        tickers.update_one({"_id":"risk"},{"$addToSet":{"tickers":ticker}})
                    if psg <= 10 and psg >= -5 :
                        tickers.update_one({"_id":"safe"},{"$addToSet":{"tickers":ticker}})
                        
                    #ReCheck place
                    if ticker in tickers.find_one({"_id":"safe"})["tickers"] :
                        if psg <= 10 and psg >= -5 :
                            pass
                        else :
                            tickers.update_one({"_id":"safe"},{"$pull":{"tickers":ticker}})

                    if ticker in tickers.find_one({"_id":"discounts"})["tickers"] :
                        if psg <= -30 :
                            pass
                        else :
                            tickers.update_one({"_id":"discounts"},{"$pull":{"tickers":ticker}})

                    if ticker in tickers.find_one({"_id":"risk"})["tickers"] :
                        if psg >= 20 :
                            pass
                        else :
                            tickers.update_one({"_id":"risk"},{"$pull":{"tickers":ticker}})

        except Exception as e :
            print(f"{ticker} fillter\n{e}")




