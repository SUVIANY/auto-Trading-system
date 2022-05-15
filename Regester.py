from Config import panel,data,client;import pandas as pd;import time;from colorama import Fore

def Regester(coin,ind,tppsg,price,place) :	
	try :
		controlpanel = panel.find_one({"_id":"controlpanel"})
		if controlpanel["system"] == "ON" and data.find_one({"_id":coin}) == None :
			df = pd.DataFrame(client.get_my_trades(symbol=coin,limit=10))
			if not df.empty:
				df.loc[df['isBuyer'] == True, 'type'] = 'Buy'
				df.loc[df['isBuyer'] == False, 'type'] = 'Sell'
				df = (df).tail(1)
				action = list(df["type"])[-1]
			else :
				action = "None"

			if action == "Sell" or action == "None" :
				data.insert_one({"_id":f"{coin}","Login":"Coin Profile","Date":int(time.time()),"TakeProfit":round(tppsg,2),"place":place,"Indicator":ind,"price":price,"Approval":"no"})
				
	except Exception as e:
		print(f"Regester\n{e}")


		'''
			data.update_one({"_id":f"{coin}"},{"$addToSet":{f"Indicator {coin}":ind}})

		#This side for multipale Indicators

		#ScanAlert Side :
		try :
			d = data.distinct(f"Indicator {coin}")
			a = d[0]
			b = d[1]
			c = d[2]
			if c in d :
				#NEED TO CHANGE SOMETHINK HERE ALERTPRICE
				notifyMe({"ScanAlertSide :\nsymbol":coin,"timeStamp":int(time.time()),"alertPrice":round(float(client.get_avg_price(symbol=coin)["price"]),2),"side":"buy","indicatorName":"3rouls","reason":"auto","postionSize":"manual"})
				print(f"{Fore.LIGHTYELLOW_EX}TelgramSend it on {coin}{Fore.WHITE}")
		except :
			try :
				if a in d :
					print(f"{Fore.LIGHTGREEN_EX} NewInsert {coin} {d}{Fore.WHITE}")
			except :
				pass
			'''