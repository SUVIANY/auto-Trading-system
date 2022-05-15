from Config import data,panel,client,notifyMe,order ; import pandas as pd;from time import sleep

def System_Control() :
	while True :
		try :
			
			psg = panel.find_one({"_id":"BTCPSG"})["psg"]
			system = panel.find_one({"_id":"controlpanel"})["system"]

			if psg <= -5 and system == "ON" : #system_shutdown & cancel_buyorder & delete_profile 🛑 if vwap84 < -5% 
				panel.update_one({"_id":"controlpanel"},{"$set":{"system":"OFF" }})
				local = order.find_one({"_id":"buylimit"})["coins"]
				data.delete_many({})
				if local != [] :
					for i in range(len(local)) :
						profil = local[i]
						client.cancel_order(symbol=profil["coinName"],orderId=int(profil["orderId"]))
						order.update_one({"_id":"buylimit"},{"$pull":{"coins":profil}})
						sleep(1)
				notifyMe("System shutdown 🛑")

			if psg >= 0 and system == "OFF" : #system_turnON ✅ 
				panel.update_one({"_id":"controlpanel"},{"$set":{"system":"ON"}})
				notifyMe("System runing ✅")

			sleep(10)
		except Exception as e :
			print(f"System_Control\n{e}")

def sendingvwap():
	while True :
		try :
			psg = panel.find_one({"_id":"BTCPSG"})["psg"]
			if psg > 0 and psg < 20 :
				place = "safe✳️"
			elif psg < 2 and psg > -5 :
				place = "medium⚠️"
			elif psg < -5 :
				place = "risk📛"
			elif psg > 20 :
				place = "correction mode"
			pricenow = float(client.get_avg_price(symbol="BTCUSDT")["price"])
			notifyMe(f"𝙱𝚃𝙲𝚄𝚂𝙳𝚃 𝚙𝚛𝚒𝚌𝚎: {int(pricenow)}\n𝚟𝚠𝚊𝚙 𝙳𝚒𝚜𝚝𝚊𝚗𝚌𝚎: {psg}\n𝚖𝚊𝚛𝚔𝚎𝚝 𝚂𝚝𝚊𝚝𝚞𝚜: {place} \nThis message will be sent every 1h")
			sleep(3600)
		except Exception as e :
			print(f"sendingvwap\n{e}")



