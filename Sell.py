from datetime import datetime;import pandas as pd;from Config import client,notifyMe,order,format,logs

def sell_oco():
	while True :
		try :
			#1- dataBase
			local = order.find_one({"_id":"buylimit"})["coins"]
			if local != [] :
				for i in range(len(local)) :
					profil = local[i]
					coinname = profil["coinName"]
					price = profil["price"]
					orderId = profil["orderId"]
				#1- binanceClint
				if client.get_order(symbol=coinname,orderId=orderId)["status"] == "FILLED" :
						#Assets Want to Sell
						asset = float(client.get_asset_balance(asset=coinname[:-4])["free"])
						#FormatQty
						minQty = format.pairQtyinfo(coinname)
						asset = format.format_value(asset,minQty)
						#FormatPrice 
						minPrice = format.pairPriceinfo(coinname)
						#TP
						Above = price+(price*0.02)#2%
						Above = format.format_value(Above,minPrice)
						#SL Trigger
						belowTrigger = price-(price*0.01)#1%
						belowTrigger = format.format_value(belowTrigger,minPrice)
						#SL
						belowLimit = belowTrigger-(belowTrigger*0.001)
						belowLimit = format.format_value(belowLimit,minPrice)
						#OCO Sell Comand
						orderoco = client.create_oco_order(symbol=coinname,side ='SELL',quantity=asset,price=Above,stopPrice=belowTrigger,stopLimitPrice=belowLimit,limitIcebergQty=0,stopIcebergQty=0,stopLimitTimeInForce='GTC')
						# DELET Profile
						order.update_one({"_id":"buylimit"},{"$pull":{"coins":profil}})
						notifyMe(f"{coinname} OCO sell order FILLED")

		except Exception as e:
			print(f"{coinname} OCO\n{e}")

def sell_market(ticker,profil,trade):
	try :
		#1- format value
		asset = float(client.get_asset_balance(asset=ticker[:-4])["free"])
		minQty = format.pairQtyinfo(ticker)
		asset = format.format_value(asset,minQty)
		#2- create order
		sellorder = client.order_market_sell(symbol=ticker,quantity=asset)
		#3- logs calc
		if trade == "win" :
			usdt = float(sellorder["origQuoteOrderQty"]) - profil["usdt"]
			psg = float(round(((sellorder["origQuoteOrderQty"]/profil["usdt"])-1)*100,2))
			mark = "✅"
		elif trade == "lose" :
			usdt =  profil["usdt"] - float(sellorder["origQuoteOrderQty"])
			psg = float(round(((sellorder["origQuoteOrderQty"]/profil["usdt"])-1)*100,2))
			mark = "❎"	
		notifyMe(f"{ticker} marketsell {mark} ♞\n${usdt} @{psg}")
		#4- dataBase
		order.update_one({"_id":"buylimit"},{"$pull":{"coins":profil}})
		logs.insert_one({"_id":sellorder["orderId"],"condition":mark,"psg":psg,"usdt":usdt,"date":f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}'})
		
	except Exception as e :
		notifyMe(f"{ticker} marketsell\n{e}")

def TSL_moveing():
	while True :
		try :
			#TimeNow = int(time.time() * 1000) - @@@ 5 min or 2 min or 1 min

			local = order.find_one({"_id":"buylimit"})["coins"]
			if local != [] :
				for i in range(len(local)) :
					profil = local[i]
					coinname = profil["coinName"]
					price = profil["price"]
					orderId = profil["orderId"]
					
					detail = client.get_order(symbol=coinname,orderId=orderId)
					if detail["status"] == "FILLED" :
							df = pd.DataFrame(client.get_historical_klines(coinname,"1m",start_str=detail["updateTime"]))
							if not df.empty:
								df.columns = ['date','open','high','low','close','volume','IGNORE','Quote_volume','Trades_Count','BUY_VOL','BUY_VOL_VAL','x']
								df ["open"] = pd.to_numeric(df["open"])
								df ["high"] = pd.to_numeric(df["high"])
								df ["low"] = pd.to_numeric(df["low"])
								df ["close"] = pd.to_numeric(df["close"])
								df ["volume"] = round(pd.to_numeric(df["volume"]))
								df ["Quote_volume"] = round(pd.to_numeric(df["Quote_volume"]))
								df ["Trades_Count"] = pd.to_numeric(df["Trades_Count"])
								df['isGreen'] = df['close'] > df['open']
								del df['Quote_volume']
								del df['IGNORE']    
								del df['BUY_VOL']
								del df['BUY_VOL_VAL']
								del df['x']
								del df['Trades_Count']

								df["TSL"] = df.close.cummax() * 0.90

								mark = []
								pos = 0
								for i in range(len(df)) :
									if df.close[i] <= df.TSL[i] and pos == 0 :
											mark.append(i)
											pos = 1
									if df.close[i] > df.TSL[i] and pos == 1 :
											pos = 0
								for i in mark :
									
									if df.Date[i] > "@@@TimeNow" :
										try :
											asset = float(client.get_asset_balance(asset=coinname[:-4])["free"])
											minQty = format.pairQtyinfo(coinname)
											asset = format.format_value(asset,minQty)
											client.order_market_sell(symbol=coinname,quantity=asset)
											order.update_one({"_id":"buylimit"},{"$pull":{"coins":profil}})
										except Exception as e :
											notifyMe(f"{coinname} market sell order UNFILLED / {e}")

		except Exception as e :
			print(f"sell : There is isio in sell_market \n\n{e}")

def TSL_hold(coin):
	pull = pd.DataFrame(client.get_my_trades(symbol=coin,limit=500))
	if not pull.empty:
		pull = (pull).tail(1)
		if pull['isBuyer'].any() == True:
			df = pd.DataFrame(client.get_historical_klines(coin,"1m",start_str=int(pull['time'])))
			if not df.empty:
				df.columns = ['date','open','high','low','close','volume','IGNORE','Quote_volume','Trades_Count','BUY_VOL','BUY_VOL_VAL','x']
				df["high"] = pd.to_numeric(df["high"])
				#get now price 
				listTicker = client.get_all_tickers()
				for tickery in listTicker:					
					if tickery["symbol"] == coin:
						PriceNow = float(tickery["price"])
				#pcg
				StopLoss = df.high.max()-(df.high.max()*0.2)
				if PriceNow < StopLoss:
					#Get Asset Balance
					qty = float(client.get_asset_balance(asset=coin[:-4])["free"]) 
					#Format
					minQty = format.pairQtyinfo(coin)
					minPrice = format.pairPriceinfo(coin)
					#rusalt for market sell
					qtyFormatted = format.format_value(qty, minQty)
					#PRINT SIDE :
					AVG_price = format.pairPriceinfo(coin)
					pluspricesell = AVG_price * 0.003
					lastpricesell = AVG_price - pluspricesell
					priceFormatted = format.format_value(lastpricesell, minPrice)
					stoplossvalue = round(((StopLoss - float(pull['price']))/float(pull['price']))*100 , 4)
					try:
						print(f'Success stop loss on : {coin}  price : {PriceNow}  {stoplossvalue}%')
					except Exception as e:
						print("trailing stop loss failed on (%s)",coin, e)
				else :
					print('Price Boght :', float(pull['price']))
					print('Price Now :', PriceNow)
					print('Stop loss :', round(StopLoss,2))


