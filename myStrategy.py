import pandas as pd
import numpy as np



def myStrategy(pastPriceVec, currentPrice, window_size, rolling_window, low_threshold, high_threshold):
	# buy return 1
	# sell return -1
	# hold return 0
    action = 0

    if len(pastPriceVec) + 1 < window_size:
        return action
	
    pastPriceVec = pastPriceVec[-window_size:]
    PriceVec = np.concatenate(pastPriceVec, np.array(currentPrice))
	
    PriceVec = pd.DataFrame(PriceVec)
    delta = PriceVec.diff()
    delta = delta[1:]
	
    pricesUp = delta.copy()
    pricesDown = delta.copy()
	
    pricesUp[pricesUp < 0] = 0
    pricesDown[pricesDown > 0] = 0
	
    rollUp = pricesUp.rolling(rolling_window).mean()
    rollDown = pricesDown.rolling(rolling_window).mean()
	
    rs = rollUp/rollDown
    rsi = 100.0 - (100.0 / (1.0 + rs))

    if rsi > high_threshold:
        action = -1
    elif rsi < low_threshold:
        action = 1

    return action

def rrEstimate(priceVec):
	capital=1000	# Initial available capital
	capitalOrig=capital		# original capital
	dataCount=len(priceVec)				# day size
	suggestedAction=np.zeros((dataCount,1))	# Vec of suggested actions
	stockHolding=np.zeros((dataCount,1))  	# Vec of stock holdings
	total=np.zeros((dataCount,1))	 	# Vec of total asset
	realAction=np.zeros((dataCount,1))	# Real action, which might be different from suggested action. For instance, when the suggested action is 1 (buy) but you don't have any capital, then the real action is 0 (hold, or do nothing). 
	# Run through each day
	for ic in range(dataCount):
		currentPrice=priceVec[ic]	# current price
		suggestedAction[ic]=myStrategy(priceVec[0:ic], currentPrice)		# Obtain the suggested action
		# get real action by suggested action
		if ic>0:
			stockHolding[ic]=stockHolding[ic-1]	# The stock holding from the previous day
		if suggestedAction[ic]==1:	# Suggested action is "buy"
			if stockHolding[ic]==0:		# "buy" only if you don't have stock holding
				stockHolding[ic]=capital/currentPrice # Buy stock using cash
				capital=0	# Cash
				realAction[ic]=1
		elif suggestedAction[ic]==-1:	# Suggested action is "sell"
			if stockHolding[ic]>0:		# "sell" only if you have stock holding
				capital=stockHolding[ic]*currentPrice # Sell stock to have cash
				stockHolding[ic]=0	# Stocking holding
				realAction[ic]=-1
		elif suggestedAction[ic]==0:	# No action
			realAction[ic]=0
		else:
			assert False
		total[ic]=capital+stockHolding[ic]*currentPrice	# Total asset, including stock holding and cash 
	returnRate=(total[-1].item()-capitalOrig)/capitalOrig		# Return rate of this run
	return returnRate