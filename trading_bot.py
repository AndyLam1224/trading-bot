import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt 
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
import time
import alpaca_trade_api as tradeapi


api_key = 'J9YASUS5QZIWIKH7'
api_key2 = '1AZ1UX26Z6TUV8T7'
tickers = ['MSFT']
#tickers = ['MSFT','AAPL','TSLA','AMZN','FB']
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
		ts = TimeSeries(key=api_key,output_format='pandas')
		close_price = api.get_barset(symbol,barTimeframe,limit=1)
		close_dic[symbol] = close_price
		print(symbol + ': ' + str(close_price))
		return close_dic

# get 50 day simple moving averages	using alpha vantage
def get_sma():
	period = 50

	for symbol in tickers:
		ti = TechIndicators(key=api_key2, output_format='pandas') 
		data_ti, meta_data_ti = ti.get_sma(symbol=symbol, interval='1min', time_period=period, series_type='close')
		sma = data_ti['SMA'].iloc[-1]
		averages_dic[symbol] = sma 
	return averages_dic

average_dic = get_sma()

def main():
	close_dic = get_last_price()
	print(close_dic)
	for key in close_dic:
		print(key)
		# sell if close price is 5% higher than 50 day sma
		if(close_dic[key] < averages_dic[key]*0.95):
			print('works')
			buy(key)
		elif (close_dic[key] > averages_dic[key]*1.05):
			print('sell works')
			sell(key)
	time.sleep(65)

main()