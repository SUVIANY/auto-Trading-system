from time import sleep;from Config import tickers,panel;from tradingview_ta import TA_Handler,Interval,Exchange;from colorama import Fore;import pandas as pd;from Regester import Regester;from Config import client

intrval = "1m"
depth = "40 hours ago UTC"

def VWAP() :
    print("@ALSUFIANY System running UP")
    while True :
        try :
            if panel.find_one({"_id":"controlpanel"})["system"] == "ON" :

                for place in ["safe","discounts"] :
                    if place == "discounts" :
                        break

                    for ticker in tickers.find_one({"_id":place})["tickers"] :
                        df = pd.DataFrame(client.get_historical_klines(ticker,client.KLINE_INTERVAL_1WEEK,'14 days ago UTC'))
                        if not df.empty :
                            df.columns=['date','open','high','low','close','volume','IGNORE','Quote_volume','Trades_Count','BUY_VOL','BUY_VOL_VAL','x']
                            df["open"]=pd.to_numeric(df["open"]);df["high"]=pd.to_numeric(df["high"]);df["low"]=pd.to_numeric(df["low"]);df["close"]=pd.to_numeric(df["close"]);df["volume"]=round(pd.to_numeric(df["volume"]));df['isGreen']=df['close']>df['open']
                            del df['Quote_volume'];del df['IGNORE'];del df['BUY_VOL'];del df['BUY_VOL_VAL'];del df['x'];del df['Trades_Count'];pricenow = float(df.close.tail(1))
                            if list(df.high)[1] > list(df.high)[0] :
                                tp = list(df.high)[1]
                            else :
                                tp = list(df.high)[0]
                            
                            #checkAlarm indicator :
                            if tp >= (pricenow*1.20) or tp >= (pricenow*1.10) and tp < (pricenow*1.2)  or tp >= (pricenow*1.05) and tp < (pricenow*1.10) and place == "safe":
                                df = pd.DataFrame(client.get_historical_klines(ticker,intrval,depth))
                                if not df.empty :
                                    df.columns = ['Date','Open','High','Low','Close','Volume','IGNORE','Quote_Volume','Trades_Count','BUY_VOL','BUY_VOL_VAL','x'] 
                                    df["Close"] = pd.to_numeric(df["Close"]);df["Volume"] = pd.to_numeric(df["Volume"])
                                    mark = [];pos = 0;period = 200
                                    df[f'vwap{period}']=round(((df.Volume*df.Close).rolling(window=period).sum()) / (df['Volume'].rolling(window=period).sum()),10)
                                    df[f'vwapd{period}'] = ((df['Close']-df[f'vwap{period}'])/df[f'vwap{period}'])*100
                                    mean = df[f"vwapd{period}"].rolling(window=period).mean()
                                    std = df[f"vwapd{period}"].rolling(window=period).std()
                                    df[f"vwapzscore{period}"]= (df[f"vwapd{period}"]-mean)/std
                                    vwap = df["vwapzscore200"]

                                    #checking alarms indicator :
                                    for i in range(len(df)) :
                                        if vwap[i] <= -2.5 and pos == 0 :
                                            mark.append(i)
                                            pos = 1      
                                        if vwap[i] > -2.5 and pos == 1 :
                                            pos = 0

                                    #accepted alarms from indicator :
                                    for i in mark :
                                        minute = list(df.Date.tail(3))
                                        if df.Date[i] > minute[2] or df.Date[i] > minute[1] or df.Date[i] > minute[0] :
                                            price = float(df.Close[i])
                                            tppsg = float(((tp/price)-1)*100)
                                            indicator = "vwapzscore"
                                            Regester(ticker,indicator,tppsg,price,place)
                
        except Exception as e :
            print(f"{Fore.RED}VWAP\n{ticker} {e}{Fore.WHITE}")

def BTCvwap48() :
	while True :
		try :
			df = pd.DataFrame(client.get_historical_klines("BTCUSDT","1d","200 days ago UTC"))
			if not df.empty :
				df.columns= ['Date','Open','High','Low','Close','Volume','IGNORE','Quote_Volume','Trades_Count','BUY_VOL','BUY_VOL_VAL','x'] 
				df["Close"]= pd.to_numeric(df["Close"]);df["Volume"]= pd.to_numeric(df["Volume"]);df['vc']= df.Volume*df.Close;df[f'vwap48']=round((df['vc'].rolling(window=48).sum())/(df['Volume'].rolling(window=48).sum()),10).fillna(method='bfill')
				psg = float(round(((float(df.Close.tail(1))/float(df.vwap48.tail(1)))-1)*100,2))
				panel.update_one({"_id":"BTCPSG"},{"$set":{"psg":psg}})
				sleep(10)
		except Exception as e :
			print(f"BTCvwap48\n{e}")

def TV(tickers) :
    for ticker in tickers :
            main = TA_Handler(
            symbol=ticker,
            screener="crypto",
            exchange="binance",
            interval=Interval.INTERVAL_1_HOUR)
            summer = int(main.get_analysis().summary["SELL"])
            osc = int(main.get_analysis().oscillators["SELL"])

            if summer == 17 :
                pass
                #Regester(ticker,"summery def")
            if osc == 14 :
                pass 
                #Regester(ticker,"summery osc")


            print(ticker,"Osc :",osc,"Summery :",summer)

