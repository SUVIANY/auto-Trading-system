import pandas as pd
import matplotlib.pyplot as plt
import time

def Trackasset(asset) :
	with open('TrackAsset.py', 'a', newline='') as e  :

		date = str(round(time.time()))

		e.write("\nx =x.append(pd.DataFrame(")

		e.write("{'asset':")
		e.write(asset)
		e.write("},")

		e.write("{'date':")
		e.write(date)
		e.write("},")

		e.write("index = [0]))")

x = pd.DataFrame() 

