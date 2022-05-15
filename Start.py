from Found import System_Control,sendingvwap;from Indicators import VWAP,BTCvwap48;from Approval import LT_BUY,LT_SELL;from FillterTicker import fillter;from Format import formatSide;import multiprocessing as mp

indicator = mp.Process(target=VWAP)
LT_buy = mp.Process(target=LT_BUY)
filltering = mp.Process(target=fillter)
format = mp.Process(target=formatSide)
control = mp.Process(target=System_Control)
Btc48 = mp.Process(target=BTCvwap48)
sendin = mp.Process(target=sendingvwap)
#LT_sell = mp.Process(target=LT_SELL)

if __name__ == "__main__" :
	filltering.start()
	indicator.start()
	format.start()
	control.start()
	LT_buy.start()
	Btc48.start()
	sendin.start()
	#LT_sell.start()
	
