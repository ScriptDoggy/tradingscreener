import os
import csv
import os.path
import talib
import yfinance as yf
import pandas as pd
from datetime import datetime
import requests

class screener():


	def dl_watchlist():
		df = pd.read_csv(
			"https://datahub.io/core/s-and-p-500-companies/r/constituents.csv")
		df.head()
		df.to_csv('symbols.csv')

		todate = datetime.today().strftime('%Y-%m-%d')

		with open('symbols.csv') as f:
			for line in f:
				if "," not in line:
					continue
				symbol = line.split(",")[1]
				data = yf.download(symbol, start="2021-01-01", end=todate)
				data.to_csv('data/daily/{}.csv'.format(symbol))


	def delete():
		for root, _, files in os.walk("D:\Screener python project\tradingscreener\data\daily"):
			for f in files:
				fullpath = os.path.join(root, f)
				try:
					if os.path.getsize(fullpath) < 3 * 1024:  # set file size in kb
						print(fullpath)
						os.remove(fullpath)
				except WindowsError:
					print("Error" + fullpath)


	dl_watchlist()
	delete()


	def consolidating(df, percentage=2):
		close_price = df[-15:]

		print(close_price)
		max_close = close_price['Close'].max()
		min_close = close_price['Close'].min()

		threshold = 1 - (percentage / 100)
		if min_close > (max_close * threshold):
			return True

		return False


	def is_breaking_out(df, percentage=2.5):
		last_close = df[-1:]['Close'].values[0]

		if screener.consolidating(df[:-1], percentage=percentage):
			recent_closes = df[-16:-1]

			if last_close > recent_closes['Close'].max():
				return True

		return False


	if __name__ == "__main__":
		for filename in os.listdir('data/daily'):
			df = pd.read_csv('data/daily/{}'.format(filename))

			if consolidating(df, percentage=2.5):
				print("{} is consolidating".format(filename))

			if is_breaking_out(df):
				print("{} is breaking out".format(filename))
