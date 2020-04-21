"""
This is a program which automatically fetches, organizes, and graphs stock data for a user's desired ticker.
It allows the user to see the High, Low, Open, Close, and Volume of a ticker for the past 2 weeks.
It also provides metrics such as the Average Volume, Volatility, and Stochastic Oscillator.
On top of that, it provides graphs the show the Volume, Moving Average, Expected Returns, and correlation to the S&P 500.
It is designed to assist in the technical analysis of a stock and graph its fundemantal metrics.
"""
import math
import datetime
import pandas as pd
from pandas import Series, DataFrame
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import style
import pandas_datareader.data as pdr

__author__ = "Kaushik Chatterjee"
__maintainer__ = "Kaushik Chatterjee"
__license__ = "MIT"
__version__ = "1.0.0"
__status__ = "Development"

mpl.rc("figure", figsize = (7, 8))
style.use("seaborn")

ticker = input("Please enter the ticker of the desired stock: ").upper()

month = int(input("How many months back should we fetch the historic data? "))

cur_date = datetime.datetime.today() #gets the current date 
orig_date = pd.to_datetime(cur_date, format="%Y-%m-%d") - pd.DateOffset(months = month) #gets the date a year back

start = datetime.datetime(orig_date.year, orig_date.month, orig_date.day)
end = datetime.datetime(cur_date.year, cur_date.month, cur_date.day)

df = pdr.DataReader(ticker, "yahoo", start, end)
del df["Adj Close"]

benchmark = pdr.DataReader("SPY", "yahoo", start, end)
sp_closing = benchmark["Close"]

closing_prices = df["Close"]

mvavg_plot = closing_prices.rolling(31, min_periods = 1).mean()
std_dev = np.std(closing_prices)
avg_vol = df["Volume"].mean()

stoch_osc_low = min(df.tail(14)["High"].tolist())
stoch_osc_high = max(df.tail(14)["High"].tolist())
stoch_osc_closing = df["Close"].tolist()
stoch_osc_recentclose = stoch_osc_closing[len(stoch_osc_closing) - 1]
stochastic_oscillator = ((stoch_osc_recentclose - stoch_osc_low) / (stoch_osc_high - stoch_osc_low)) * 100


print("\nHere is a table showing the statistics of", ticker, "for the past week:")
print(df.tail(14))
print("\nThe volatility of", ticker, "is ${:.3f}".format(std_dev))
print("The average volume of", ticker, "is {:.3f}".format(avg_vol), "and the relative volume is {:.3f}".format(df["Volume"].tolist()[len(df["Volume"].tolist()) - 1] / avg_vol))
print("The stochastic oscillator of", ticker, "is %{:.3f}".format(stochastic_oscillator))

plt.figure(1)
vol = df.tail(7)["Volume"].tolist()
label = [x for x in range(1, len(vol) + 1)]
plt.bar(label, vol)
plt.title("Volume Over Last 7 Days")
plt.xlabel("Day No.")
plt.ylabel("Volume")

plt.figure(2)
plt.scatter(closing_prices, sp_closing)
plt.xlabel("Returns: {0}".format(ticker))
plt.ylabel("Returns: SPDR S&P 500 Trust ETF")
plt.title("{0} vs the S&P 500 ETF".format(ticker))

plt.figure(3)
closing_prices.plot(label = ticker)
mvavg_plot.plot(label = "Moving Average")
plt.title("Moving Average vs. Stock Prices")
plt.legend()

plt.figure(4)
rets = closing_prices / closing_prices.shift(1) - 1
rets.plot(label = 'Expected Returns')
plt.title("Expected Returns Over %s Month(s)"%(month))
plt.legend()

plt.show()