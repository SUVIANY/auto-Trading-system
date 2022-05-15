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

def TOPGANERS():
    allticker = ["SOLUSDT","BTCUSDT"]

    x = pd.DataFrame()
    for ticker in allticker :
        raw = pd.DataFrame(client.get_historical_klines(ticker,"1h","40 hours ago UTC"))
        if not raw.empty:
                raw[0] =  pd.to_datetime(raw[0],unit='ms')
                raw.columns = ['timestamp','open','high','low','close','volume','IGNORE','quoteVolume','SELLVolume','BUY_VOL','BUY_VOL_VAL','x']
                # convert to numbers 
                del raw['IGNORE'];del raw['BUY_VOL'];del raw['BUY_VOL_VAL'];del raw['x'];del raw['SELLVolume']
                raw ["open"] = pd.to_numeric(raw["open"]);raw ["high"] = pd.to_numeric(raw["high"]);raw ["low"] = pd.to_numeric(raw["low"]);raw ["close"] = pd.to_numeric(raw["close"]);raw ["volume"] = round(pd.to_numeric(raw["volume"]));raw ["quoteVolume"] = round(pd.to_numeric(raw["quoteVolume"]));raw.loc[raw.quoteVolume < 100, 'quoteVolume'] =100

                raw['pchange1h'] = raw.close.diff(1).fillna(0) # diff can has if for different timeperiods
                raw['pchange1hpct'] = round((raw['pchange1h']/raw ["close"])*100,2)
                raw['pchange24h'] = raw.close.diff(23).fillna(0) # diff can has if for different timeperiods 
                raw['pchange24hpct'] = round((raw['pchange24h']/raw ["close"])*100,2)

                raw['v1h'] = raw.quoteVolume.rolling(window = 1).sum().fillna(0)#.shift()
                raw['vchange1h'] = raw.v1h.diff(1).fillna(0) # diff can has if for different timeperiods 
                raw['vchange1hpct'] = round((raw['vchange1h']/raw ["quoteVolume"])*100,2)

                raw['v4h'] = raw.quoteVolume.rolling(window = 4).sum().fillna(0)#.shift()
                raw['vchange4h'] = raw.v4h.diff(4).fillna(0) # diff can has if for different timeperiods 
                raw['vchange4hpct'] = round((raw['vchange4h']/raw ["quoteVolume"])*100,2)
                
                raw['v24'] = raw.quoteVolume.rolling(window = 23).sum().fillna(0)#.shift()
                raw['vchange24h'] = raw.v24.diff(23).fillna(0) # diff can has if for different timeperiods 
                raw['vchange24hpct'] = round((raw['vchange24h']/raw ["quoteVolume"])*100,2)
                
                #PRICE %
                lastprice = (list(raw.close.tail(1)))[0] #lastprice
                pchange1hpct = (list(raw.pchange1hpct.tail(1)))[0] #Pchange1H_pct
                pchange24hpct = (list(raw.pchange24hpct.tail(1)))[0] #Pchange24H_pct
                #VOLUME %
                vchange1h = (list(raw.vchange1h.tail(1)))[0] #Vchange1H
                vchange1hpct = (list(raw.vchange1hpct.tail(1)))[0] #vchange1hpct
                vchange4h = (list(raw.vchange4h.tail(1)))[0] #Vchange4H
                v4 = (list(raw.v4h.tail(1)))[0] 
                vchange4hpct = (list(raw.vchange4hpct.tail(1)))[0] #Vchange4H
                vchange24h = (list(raw.vchange24h.tail(1)))[0] #vchange24h
                vchange24hpct = (list(raw.vchange24hpct.tail(1)))[0] #Vchange24H_pct

                volume24h = round((list(raw.v24.tail(1)))[0]) #vchange24h

                x = x.append(pd.DataFrame({'symbol':ticker,'lastPrice':lastprice,'volume24h':v4},index = [0]))

    sort = x.sort_values(by=["volume24h"],axis=0,ascending=False).tail(30) # (TOP 30) u change the value
    
    print(sort.tail(30))


