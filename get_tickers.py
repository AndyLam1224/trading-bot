import bs4 as bs
import pandas as pd
import requests
from arctic import Arctic
from datetime import datetime
from alpha_vantage.timeseries import TimeSeries

api_key = 'J9YASUS5QZIWIKH7'

# Get tickers for SP100
def get_tickers():
	# Use table in wikipedia
	resp = requests.get('https://en.wikipedia.org/wiki/S%26P_100')
	soup = bs.BeautifulSoup(resp.text, features = "html.parser")
	table= soup.find('table',{'class':'wikitable sortable'})
	tickers = []
	for row in table.findAll('tr')[1:]:
		ticker = row.findAll('td')[0].text
		tickers.append(ticker.replace('\n',''))
	return tickers

# Connect to Local MongoDB
store = Arctic('localhost')

# Create the library - defaults to VersionStore
store.initialize_library('HISTORICAL_DATA')

#Access the library
library = store['HISTORICAL_DATA']

# set symbols into SP100 tickers
symbols = get_tickers()

# initialize timeseries
ts = TimeSeries(key=api_key, output_format='pandas') 

# Gets the date of the last day of the most recent tick data in the database
def get_lastdate(symbol):
	item = library.read(symbol).data
	date = str(item.index[0])[0:10]
	return date

# Write to DB daily historical data for SP 100
def update_tickers:
	for symbol in symbols:
		# If the current ticker does not exist, create new table and gather data
		if library.has_symbol(symbol) == False:
			print("Currently gathering data for: " + symbol) 
			data_ts, meta_data_ts = ts.get_daily(symbol=symbol,outputsize='full')
			df1 = data_ts
			library.write(symbol, df1, metadata ={'source': 'AlphaVantage'})
			time.sleep(15)
			print(symbol + ": Complete")

		# If ticker exists, check to see if its up to date, if not append newest data
		elif(get_lastdate(symbol) != datetime.date(datetime.now())):
			start = get_lastdate()
			data_ts, meta_data_ts = ts.get_daily(symbol='symbol',outputsize='full')
			new_data = data_ts[:start]
			library.append(symbol, new_data, upsert=False)
			print(symbol + ": Added new data")



