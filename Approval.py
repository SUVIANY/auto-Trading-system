import time;from time import sleep;import pandas as pd;import talib;from Config import notifyMe,panel,client,data,order;from Buy import Buy_limit;from Sell import sell_market;from datetime import datetime

def LT_BUY() :
	while True :
		try :
			psg = panel.find_one({"_id":"BTCPSG"})["psg"]
			#1- dataBase check Regestered coins
			local = data.find({"Login":"Coin Profile"})
			for i in local :
				sleep(2)
				coin = i["_id"]
				tppsg = i["TakeProfit"]
				place = i["place"]
				Approval = i["Approval"]
				price = i["price"]
				ind = i["Indicator"]
				#2- binanceClint
				df = pd.DataFrame(client.get_historical_klines(coin,"15m",'90 minutes ago UTC'))
				if not df.empty:
					df.columns = ['date','open','high','low','close','volume','IGNORE','Quote_volume','Trades_Count','BUY_VOL','BUY_VOL_VAL','x']
					df ["open"] = pd.to_numeric(df["open"])
					df ["high"] = pd.to_numeric(df["high"])
					df ["low"] = pd.to_numeric(df["low"])
					df ["close"] = pd.to_numeric(df["close"])
					df ["volume"] = round(pd.to_numeric(df["Quote_volume"]))
					df ['isGreen'] = df['close'] > df['open']
					del df['Quote_volume']
					del df['IGNORE']    
					del df['BUY_VOL']
					del df['BUY_VOL_VAL']
					del df['x']
					del df['Trades_Count']
					
					#3-  %-1 then approve deal
					if float(df.close.tail(1)) <= (price-(price*0.01)) and data.find_one({"_id":coin})["Approval"] == "no" :
						data.update_one({"_id":coin},{"$set":{"Approval":"yes"}})
						Approval = "yes"
						date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
						notifyMe(f"𝔯𝔢𝔤𝔢𝔰𝔱𝔢𝔯 𝔰𝔦𝔡𝔢 ♛\n\ncoin : @{coin}  \nprice : ${price} \ntarget : % {int(tppsg)}\nplace : {place}\nindicator : {ind}\napproval : accepted \ncomment : start LiveTracking\ntimeStamp :{int(time.time())} \ndate :{date}")


					if Approval == "yes" :
						#4- Eating Candel Track
						df["Gulf"] = talib.CDLENGULFING(df.open,df.high,df.low,df.close)
						df["Gulf"] = pd.to_numeric(df["Gulf"])	
						if df.Gulf[4] == 100 and df.date[4] > i["Date"] :

							if df.close[5] < df.close[4] :
								price = df.close[5]
							else :
								price = df.close[4]
						
							#term and PS Calc
							if place == "discounts" :
								if place == "discounts" and psg > 0 and psg <= 20:
									term = "LONG"
									PSlocal = "@HR"
								elif place == "discounts" and psg < 0 and psg > -5:
									term = "LONG"
									PSlocal = "@MR"
								elif place == "discounts" and psg > 35 :
									term = "LONG"
									PSlocal = "@LR"
								else :
									term = "LONG"
									PSlocal = "@LR"
								#Buy_limit(coin,price,PSlocal,tppsg,term,place)
								print(coin,price,PSlocal,tppsg,term,place)
								data.delete_one({"_id":coin})

							if place == "safe" :
								if place == "safe" and psg > 0 and psg <= 20:
									term = "MEDIUM"
									PSlocal = "@MR"
							
								elif place == "safe" and psg < 0 and psg > -5:
									term = "MEDIUM"
									PSlocal = "@LR"
								
								elif place == "safe" and psg > 35:
									term = "MEDIUM"
									PSlocal = "@LR"
								else :
									term = "MEDIUM"
									PSlocal = "@LR"

								#Buy_limit(coin,price,PSlocal,tppsg,term,place)
								notifyMe(f"{coin} buylimit ♞\n${price} @0")
								data.delete_one({"_id":coin})


		except Exception as e:
			print(f"LT_BUY\n{e}")

def LT_SELL() :
	while True :
			sleep(1)
			#1- dataBase check Bought coins
			local = order.find_one({"_id":"buylimit"})["coins"]
			if local != [] :
				for i in range(len(local)) :
					profil = local[i]
					coinname = profil["coinName"]
					price = profil["price"]
					orderId = profil["orderId"]
					tppsg = profil["tppsg"]
					term = profil["term"]
					reach = profil["reach"]
					date = profil["date"]
					if client.get_order(symbol=coinname,orderId=orderId)["status"] == "FILLED" :
						listTicker = client.get_all_tickers()
						for tickery in listTicker:					
							if tickery["symbol"] == coinname : 
								pricenow = float(tickery["price"])

						if term == "LONG" and tppsg > 20 : #LONG TERM : target+20% 					
							target = float(tppsg/100)

							#profits Live Track
							for i in [9,8,7,6,5,4,3,2] :
								if reach == 0 :
									r = price
								else :
									r = (price+(price*(target/reach)))
									
								if pricenow >= (price+(price*(target/i))) and (price+(price*(target/i))) > r :
									order.update_one({"_id":"buylimit","coins":{"$elemMatch":{"coinName":coinname}}},{"$set":{"coins.$.reach":(target/i)}})
								if pricenow >= (price+(price*(target/i))) :
									order.update_one({"_id":"buylimit","coins":{"$elemMatch":{"coinName":coinname}}},{"$set":{"coins.$.live":(target/i)}})
									order.update_one({"_id":"buylimit","coins":{"$elemMatch":{"coinName":coinname}}},{"$set":{"coins.$.pricenow":pricenow}})
									
							#take profit 
							if pricenow >= target :
								sell_market(coinname,profil,"win")
							#stop lose
							if pricenow <= (price-(price*0.098)) :
								sell_market(coinname,profil,"lose")
							#lvl up SL
							elif pricenow <= (price+(price*0.05)) and pricenow > price and reach >= (target/4)   :
								sell_market(coinname,profil,"win")

						elif term == "MEDIUM" and tppsg > 10 : #MEDIUM TERM : target10%
							target = float(10/100)

							#profits Live Track
							for i in [9,8,7,6,5,4,3,2] :
								if reach == 0 :
									r = price
								else :
									r = (price+(price*(target/reach)))
									
								if pricenow >= (price+(price*(target/i))) and (price+(price*(target/i))) > r :
									order.update_one({"_id":"buylimit","coins":{"$elemMatch":{"coinName":coinname}}},{"$set":{"coins.$.reach":(target/i)}})
								if pricenow >= (price+(price*(target/i))) :
									order.update_one({"_id":"buylimit","coins":{"$elemMatch":{"coinName":coinname}}},{"$set":{"coins.$.live":(target/i)}})
									order.update_one({"_id":"buylimit","coins":{"$elemMatch":{"coinName":coinname}}},{"$set":{"coins.$.pricenow":pricenow}})
				
							#take profit
							if pricenow >= (price+(price*target)) :
								sell_market(coinname,profil,"win")
							#stop lose
							if pricenow <= (price-(price*0.049)) :
								sell_market(coinname,profil,"lose")
							#lvl up SL
							elif pricenow <= (price+(price*0.02)) and pricenow > price and  reach >= (target/4) :
								sell_market(coinname,profil,"win")

						if term == "MEDIUM" and tppsg < 10 and tppsg > 5: #SHORT TERM : target2%
							target = float(tppsg/100)

							#profits Live Track
							for i in [9,8,7,6,5,4,3,2] :
								if reach == 0 :
									r = price
								else :
									r = (price+(price*(target/reach)))
									
								if pricenow >= (price+(price*(target/i))) and (price+(price*(target/i))) > r :
									order.update_one({"_id":"buylimit","coins":{"$elemMatch":{"coinName":coinname}}},{"$set":{"coins.$.reach":(target/i)}})
								if pricenow >= (price+(price*(target/i))) :
									order.update_one({"_id":"buylimit","coins":{"$elemMatch":{"coinName":coinname}}},{"$set":{"coins.$.live":(target/i)}})
									order.update_one({"_id":"buylimit","coins":{"$elemMatch":{"coinName":coinname}}},{"$set":{"coins.$.pricenow":pricenow}})
							
							#take profit
							if pricenow >= (price+(price*target)) :
								sell_market(coinname,profil,"win")
							#stop lose
							if pricenow <= (price-(price*target/2)) :
								sell_market(coinname,profil,"lose")
							
							#lvl up SL
							elif pricenow <= (price+(price*0.012)) and pricenow > price and  reach >= (target/4) :
								sell_market(coinname,profil,"win")

						#quit from deal (3days+5%)(4days+2%) @ need to think up

						if time.time() > (date+259200) and pricenow >= (price+(price*(float(5/100))))   or   time.time() > (date+345600) and pricenow >= (price+(price*(float(1/100)))) :
							sell_market(coinname,profil,"win")


'''
#GULF MADE BY ME :

#3- stoplose calclation
if tp > 10 :
	sl = price-(price*0.10)#01%
elif tp < 10 :
	sl = tp/2
	sl = "" #تحويل الى رقم 0.02
	sl = price-(price*sl)#1%

lc_high = list(df.high)[0] 
lc_low = list(df.low)[0] 
tc_open = list(df.open)[1]
tc_close = list(df.close)[1]
x = pd.DataFrame() ; x = x.append(pd.DataFrame({"coin":coin,"high":lc_high,"low":lc_low,"open":tc_open,"close":tc_close},index=[0]))
if tc_close > lc_high :
	print(tc_open)
'''