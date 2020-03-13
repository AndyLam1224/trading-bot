import bs4 as bs
import requests
from arctic import Arctic
import time 
from alpha_vantage.timeseries import TimeSeries

api_key = 'J9YASUS5QZIWIKH7'

# Get tickers for SP100
def get_tickers():
	# Use table in wikipedia
	resp = requests.get('https://en.wikipedia.org/wiki/S%26P_100')
	soup = bs.BeautifulSoup(resp.text)
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

# Write to DB daily historical data for SP 100
for symbol in symbols:
	data_ts, meta_data_ts = ts.get_daily(symbol=symbol,outputsize='full')
	df1 = data_ts
	library.write(symbol, df1, metadata ={'source': 'AlphaVantage'})
	time.sleep(15)
	print(symbol + ": Complete")