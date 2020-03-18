import pandas as pd 
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
import time
import alpaca_trade_api as tradeapi

api_key = 'J9YASUS5QZIWIKH7'

tickers = ['MSFT','AAPL','TSLA','AMZN','FB']
close_dic = {}
averages_dic = {}

api = tradeapi.REST('PKG4KMFK0CCDVQB2OSUM',
					'C7eWpJewmvVF8a8RVWxwnrLEKRheoaEUR/ReJyI0',
					'https://paper-api.alpaca.markets')

# get current holding
def get_holdings():
	protfolio = api.get_portfolio_history(date_start=None, date_end=None, period=None, timeframe=None, extended_hours=None)
	print(protfolio)

# get current capital
def get_buying_power():
	buying_power = api.get_account().buying_power
	return buying_power

# submit buy order
def buy(sym,amt):
	api.submit_order(
    			symbol=sym,
			    side='buy',
			    type='market',
			    qty=amt,
			    time_in_force='day'
			    )

#submit sell order
def sell(sym, amt):
	api.submit_order(
    			symbol=sym,
			    side='sell',
			    type='market',
			    qty=amt,
			    time_in_force='day'
			    )

# get most recent close price using alpaca api
def get_last_price():

	for symbol in tickers:
		close_price = api.get_barset(symbol,'1Min',limit=1)
		close_dic[symbol] = close_price[symbol][0].c
		print(symbol + ': ' + str(close_price))

		return close_dic

# get 50 day simple moving averages	using alpha vantage
def get_sma():
	period = 50

	# Get sma and associate with ticker in a dictionary
	for symbol in tickers:
		ti = TechIndicators(key=api_key, output_format='pandas') 
		data_ti, meta_data_ti = ti.get_sma(symbol=symbol, interval='1min', time_period=period, series_type='close')
		#Get only most recent price
		sma = data_ti['SMA'].iloc[-1]
		averages_dic[symbol] = sma 

	return averages_dic

average_dic = get_sma()

def main():
	close_dic = get_last_price()

	for key in close_dic:

		# sell if close price is 5% higher than 50 day sma
		if(close_dic[key] < averages_dic[key]*0.95):
			print('Buying at ' + str(close_dic[key]) + 'SMA50 is: ' + str(averages_dic[key]))
			buy(key, 1)
		elif (close_dic[key] > averages_dic[key]*1.05):
			print('Selling at ' + str(close_dic[key]) + 'SMA50 is: ' + str(averages_dic[key]))
			sell(key, 1)
	time.sleep(65)

while True:
	main()