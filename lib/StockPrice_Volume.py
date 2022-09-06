from pandas_datareader import data
import pandas as pd
import matplotlib.pyplot as plt

def stockprice_volume(start, end, code):
    dframe = data.DataReader(code, "yahoo", start, end)
    dframe = dframe.sort_index()

    date = dframe.index
    price = dframe["Close"]
    span01 = 5
    span02 = 25
    span03 = 50

    dframe["sma01_5"] = price.rolling(window=span01).mean()
    dframe["sma02_25"] = price.rolling(window=span02).mean()
    dframe["sma03_50"] = price.rolling(window=span03).mean()

    plt.figure(figsize=(20, 10))
    plt.subplot(2, 1, 1)
    plt.plot(date, price, label = code, color = "grey")
    plt.plot(date, dframe.sma01_5, label = "sma01_5", color = "blue")
    plt.plot(date, dframe.sma02_25, label = "sma02_25", color = "red")
    plt.plot(date, dframe.sma03_50, label = "sma03_50", color = "green")
    plt.title(code, color = "white", backgroundcolor = "grey", size = 40, loc = "center")
    plt.xlabel("date", color = "grey", size = 30)
    plt.ylabel("price", color = "grey", size = 30)
    plt.legend()

    plt.subplot(2, 1, 2)
    plt.bar(date, dframe.Volume, label="Volume", color = "grey")
    plt.legend()
    plt.show()

stockprice_volume("2020-01-01", "2022-09-01", "^N225")