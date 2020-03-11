import alpaca_trade_api as tradeapi
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

APCA_API_KEY_ID = 'PKG4KMFK0CCDVQB2OSUM'
APCA_API_SECRET_KEY = 'C7eWpJewmvVF8a8RVWxwnrLEKRheoaEUR/ReJyI0'
APCA_API_BASE_URL = "https://paper-api.alpaca.markets"

storageLocation = 'C:/Users/andyl/Desktop/Projects/Python/Trading Bot'
api = tradeapi.REST(APCA_API_KEY_ID,APCA_API_SECRET_KEY,APCA_API_BASE_URL)
barTimeframe = '1Min'
tickers = ['MSFT','AAPL','TSLA','AMZN','FB']


iteratorPos = 0
assetListLen = len(tickers)


symbol = tickers[0]
	
dataFile = ""
lastDate = "2020-00-00T00:00:00.000Z" 
	
returned_data = api.get_barset(symbol,barTimeframe,limit=1).df

print(returned_data['MSFT'])						
