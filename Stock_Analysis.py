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

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

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
orig_date = pd.to_datetime(cur_date, format="%Y-%m-%d") - pd.DateOffset(months = month) #gets the date the specified months back

start = datetime.datetime(orig_date.year, orig_date.month, orig_date.day)
end = datetime.datetime(cur_date.year, cur_date.month, cur_date.day)

orig_date_2 = pd.to_datetime(cur_date, format="%Y-%m-%d") - pd.DateOffset(days = 200)
start_2 = datetime.datetime(orig_date_2.year, orig_date_2.month, orig_date_2.day)
end_2 = end

df = pdr.DataReader(ticker, "yahoo", start, end)
df_2 = pdr.DataReader(ticker, "yahoo", start_2, end_2)
del df["Adj Close"]
del df_2["Adj Close"]

benchmark = pdr.DataReader("SPY", "yahoo", start, end)
sp_closing = benchmark["Close"]
closing_prices = df["Close"]
closing_prices_2 = df_2["Close"]

mvavg_50days = closing_prices_2.rolling(50, min_periods = 1).mean()
mvavg_200days = closing_prices_2.rolling(200, min_periods = 1).mean()


mvavg_plot = closing_prices.rolling(31, min_periods = 1).mean()
emvavg_plot = closing_prices.ewm(halflife = 0.5, min_periods = 1).mean()
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
plt.plot(closing_prices_2, label = "Closing Prices of {0}".format(ticker))
plt.plot(mvavg_50days, "g--", label = "50 Day Moving Average")
plt.plot(mvavg_200days, "r--", label = "200 Day Moving Average")
plt.title("Closing Prices vs. 50 Day Moving Average & 200 Day Moving Average")
plt.legend()

plt.figure(2)
plt.scatter(closing_prices, sp_closing)
plt.xlabel("Returns: {0}".format(ticker))
plt.ylabel("Returns: SPDR S&P 500 Trust ETF")
plt.title("{0} vs the S&P 500 ETF".format(ticker))

plt.figure(3)
closing_prices.plot(label = ticker)
mvavg_plot.plot(label = "Moving Average")
emvavg_plot.plot(label = "Exponential Moving Average")
plt.title("Moving Average Over the Last {0} Month(s) vs. Stock Prices".format(month))
plt.legend()

plt.figure(4)
rets = closing_prices / closing_prices.shift(1) - 1
rets.plot(label = 'Expected Returns')
plt.title("Expected Returns Over %s Month(s)"%(month))
plt.legend()

plt.show()
exit()
