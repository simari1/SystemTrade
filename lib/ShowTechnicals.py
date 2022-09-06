from pandas_datareader import data
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import talib as ta
import numpy as np
from dateutil import relativedelta

def show_technicals(start, end, code):
    if __name__ == '__main__':
        import GetCross as gc
    else:
        import lib.GetCross as gc

    df = data.DataReader(code, "yahoo", start, end)
    close = df["Adj Close"]
    date = df.index

    span01 = 5
    span02 = 25
    span03 = 75

    df["sma01"] = close.rolling(window = span01).mean()
    df["sma02"] = close.rolling(window = span02).mean()
    df["sma03"] = close.rolling(window = span03).mean()
    df["macd"], df["macdsignal"], df["macdhist"] = ta.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
    df["RSI"] = ta.RSI(close, timeperiod=14)
    df["upper"], df["middle"], df["lower"] = ta.BBANDS(close, timeperiod=span02, nbdevdn=2, nbdevup = 2, matype = 0)

    plt.figure(figsize=(30, 40))
    
    plt.subplot(5, 1, 1)
    plt.plot(date, close, label = "Stock price", color = "grey", lw=1)
    plt.plot(date, df.sma01, label = "sma01_" + str(span01), color = "slateblue",  lw=2)
    plt.plot(date, df.sma02, label = "sma02_" + str(span02), color = "red", lw=3)
    plt.plot(date, df.sma03, label = "sma03_" + str(span03), color = "green", lw=5)
    plt.fill_between(date, df["upper"], df["lower"], color = "gray", alpha = 0.3)
    plt.title("Price with Bolinger", color = "white", backgroundcolor = "grey", size = 40, loc = "center")
    plt.rcParams["font.size"] = 18
    
    #ゴールデン・デッドクロスの検出
    df["cross_SMA"] = gc.find_cross(df["sma02"], df["sma03"])
    df["cross_SMA2"] = gc.find_cross(df["sma01"], df["sma02"])
    #https://stackoverflow.com/questions/44355016/pandas-plot-data-frame-object-with-marker
    df_tmp = df.copy().reset_index()
    df_tmp["tmpindex"] = df_tmp.index - 1
    plt.plot(date, df.sma02, '-o', markevery=df_tmp[df_tmp.cross_SMA == "GC"].tmpindex.tolist(), markerfacecolor='red', markeredgecolor='red', markersize=20)
    plt.plot(date, df.sma02, '-X', markevery=df_tmp[df_tmp.cross_SMA == "DC"].tmpindex.tolist(), markerfacecolor='green', markeredgecolor='green', markersize=20)
    plt.plot(date, df.sma02, '-o', markevery=df_tmp[df_tmp.cross_SMA2 == "GC"].tmpindex.tolist(), markerfacecolor='red', markeredgecolor='red', markersize=20)
    plt.plot(date, df.sma02, '-X', markevery=df_tmp[df_tmp.cross_SMA2 == "DC"].tmpindex.tolist(), markerfacecolor='green', markeredgecolor='green', markersize=20)

    plt.grid()
    plt.legend()

    plt.subplot(5, 1, 2)
    plt.bar(date, df.Volume, label="Volume", color = "grey")
    plt.rcParams["font.size"] = 18
    plt.legend()

    plt.subplot(5, 1, 3)
    plt.fill_between(date, df["macdhist"], alpha = 0.5, color = "grey", label="MACD hist")
    plt.title("MACD History", color = "white",size = 40, backgroundcolor = "grey")
    plt.axhline(y = 0, color = "grey", linestyle="dashed")
    plt.rcParams["font.size"] = 18
    plt.legend()

    plt.subplot(5, 1, 4)
    plt.plot(date, df.macd, label = "macd", color = "green",  lw=2)
    plt.plot(date, df.macdsignal, label = "macdsignal", color = "red", lw=3)
    
    #ゴールデン・デッドクロスの検出
    df["cross_MACD"] = gc.find_cross(df["macd"], df["macdsignal"])
    #https://stackoverflow.com/questions/44355016/pandas-plot-data-frame-object-with-marker
    df_tmp = df.copy().reset_index()
    df_tmp["tmpindex"] = df_tmp.index - 1
    plt.plot(date, df.macd, '-o', markevery=df_tmp[df_tmp.cross_MACD == "GC"].tmpindex.tolist(), markerfacecolor='red', markeredgecolor='red', markersize=20)
    plt.plot(date, df.macdsignal, '-X', markevery=df_tmp[df_tmp.cross_MACD == "DC"].tmpindex.tolist(), markerfacecolor='green', markeredgecolor='green', markersize=20)

    plt.title("MACD", color = "white",size = 40, backgroundcolor = "grey")
    plt.rcParams["font.size"] = 18
    plt.legend()

    plt.subplot(5, 1, 5)
    plt.fill_between(date, df["RSI"], alpha = 0.5, color = "grey", label="RSI")
    plt.title("RSI", color = "white",size = 40, backgroundcolor = "grey")
    plt.axhline(y = 30, color = "grey", linestyle="dashed")
    plt.axhline(y = 70, color = "grey", linestyle="dashed")
    plt.ylim(0, 100)
    plt.rcParams["font.size"] = 18
    plt.legend()
    plt.show()

if __name__ == '__main__':
    show_technicals((datetime.datetime.today() + relativedelta.relativedelta(years=-1)), datetime.datetime.today(), "^N225")