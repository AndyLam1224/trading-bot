import pandas as pd 
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
import time
import alpaca_trade_api as tradeapi
from get_tickers import *

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

# get most recent close price using alpaca api and adds it to a dictionary
def get_last_price(tickers):

	for symbol in tickers:
		close_price = api.get_barset(symbol,'1Min',limit=1)
		close_dic[symbol] = close_price[symbol][0].c
		return close_dic

# get 50 day simple moving averages	using alpha vantage
def get_sma(tickers):
	period = 50

	# Get sma and associate with ticker in a dictionary
	for symbol in tickers:
		ti = TechIndicators(key=api_key, output_format='pandas') 
		data_ti, meta_data_ti = ti.get_sma(symbol=symbol, interval='1min', time_period=period, series_type='close')

		#Get only most recent price
		sma = data_ti['SMA'].iloc[-1]
		averages_dic[symbol] = sma 

	return averages_dic

def crossover():
	# Set key value pairs for last closing price and moving averages
	close_dic = get_last_price(tickers)
	averages_dic = get_sma(tickers)

	for key in close_dic:

		# buy if close price is 5% higher than 50 day sma
		if(close_dic[key] < averages_dic[key]*0.95):
			# Checks if there's enough free capital to make the purchase
			if buying_power() > close_dic[key]:
				print('Buying at ' + str(close_dic[key]) + 'SMA50 is: ' + str(averages_dic[key]))
				buy(key, 1)

		# sell if close price is 5% higher than 50 day sma
		elif (close_dic[key] > averages_dic[key]*1.05):
			print('Selling at ' + str(close_dic[key]) + 'SMA50 is: ' + str(averages_dic[key]))
			sell(key, 1)
	time.sleep(65)
	
def main():
	crossover()

if __name__ == '__main__':

	api_key = 'API_KEY'

	# Initializes an empty dictionary to be filled with close prices
	close_dic = {}
	# Initializes and empty dictionary to be filled with moving averages
	averages_dic = {}

	# Chooses the stocks to be traded
	tickers = allocate_portfolio()

	api = tradeapi.REST('KEY',
						'SECRET_KEY',
						'https://paper-api.alpaca.markets')
	main()z