from Config import order,data,client;from time import sleep;import time

def formatSide() : 
	while True :
		sleep(60)

	   #FORMAT { PROFILES }
		try :
			find = data.find({"Login":"Coin Profile"})
			for local in find :
				timenow = int(time.time())
				coin = local["_id"]
				calc = int(local["Date"]) + 9000

				if timenow > calc :
					data.delete_one({"_id":coin})
		except Exception as e:
			print(f"FormatProfiles\n{e}")
		

	   #FORMAT { ORDER }
		try :
			local = order.find_one({"_id":"buylimit"})["coins"]
			if local != [] :
				for j in range(len(local)) :
					profil = local[j]
					detail = client.get_order(symbol=profil["coinName"],orderId=int(profil["orderId"]))
					if detail["status"] == "NEW" :
						#if date insert order > 4hours = cancel
						if detail["time"] >= int(detail["time"])+14400000 :
							client.cancel_order(symbol=profil["coinName"],orderId=int(profil["orderId"]))
							order.update_one({"_id":"buylimit"},{"$pull":{"coins":{"coinName":profil["coinName"],"price":profil["price"],"orderId":profil["orderId"]}}})
		except Exception as e :
			print(f"FormatOrder\n{e}")