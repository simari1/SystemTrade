'''
買いポイント
    株価が下落し、14日RSIが20％以下になったのを確認する
    その後にSMAがゴールデンクロスしたらエントリー

利益確定の目安
    SMAがデットクロスする、または14日RSIが80％になった場合
'''

from backtesting import Strategy
from backtesting.lib import crossover
import talib as ta
from backtesting.test import SMA

class SMAandRSI(Strategy):
    SMA_short = 10 # 短期SMA
    SMA_long = 30 # 長期SMA
    upper_bound = 70
    lower_bound = 30
    rsi_window = 14

    def init(self):
        self.sma1 = self.I(SMA, self.data.Close, self.SMA_short)
        self.sma2 = self.I(SMA, self.data.Close, self.SMA_long)
        self.rsi = self.I(ta.RSI, self.data.Close, self.rsi_window)

    def next(self): # チャートデータの行ごとに呼び出される
        if self.rsi > self.upper_bound\
            or self.sma2 > self.sma1:
            #売りシグナル
            self.position.close()
        elif self.lower_bound > self.rsi\
            and crossover(self.sma1, self.sma2):
            #買いシグナル
            if not self.position:
                self.buy()

class SMAandRSI_WithShortPosition(Strategy):
    SMA_short = 10 # 短期SMA
    SMA_long = 30 # 長期SMA
    #RSI用パラメータ
    upper_bound = 70
    lower_bound = 30
    rsi_window = 14

    def init(self):
        self.sma1 = self.I(SMA, self.data.Close, self.SMA_short)
        self.sma2 = self.I(SMA, self.data.Close, self.SMA_long)
        self.rsi = self.I(ta.RSI, self.data.Close, self.rsi_window)

    def next(self): # チャートデータの行ごとに呼び出される
        if self.rsi > self.upper_bound\
            or self.sma2 > self.sma1:
            #売りシグナル
            if not self.position:
                self.sell()
            else:
                self.position.close()
        elif self.lower_bound > self.rsi\
            and crossover(self.sma1, self.sma2):
            #買いシグナル
            if not self.position:
                self.buy()

class EntryRSIandExitSMA_WithShortPosition(Strategy):
    SMA_short = 10 # 短期SMA
    SMA_long = 30 # 長期SMA
    #RSI用パラメータ
    upper_bound = 70
    lower_bound = 30
    rsi_window = 14

    # SMA_short = 10 # 短期SMA
    # SMA_long = 70 # 長期SMA
    # #RSI用パラメータ
    # upper_bound = 65
    # lower_bound = 35
    # rsi_window = 10

    def init(self):
        self.sma1 = self.I(SMA, self.data.Close, self.SMA_short)
        self.sma2 = self.I(SMA, self.data.Close, self.SMA_long)
        self.rsi = self.I(ta.RSI, self.data.Close, self.rsi_window)

    def next(self): # チャートデータの行ごとに呼び出される
        price = self.data.Close[-1]
        if crossover(self.sma2, self.sma1) or crossover(self.sma1, self.sma2):
            #デッドクロスで手じまい
            self.position.close()
        elif self.upper_bound < self.rsi:
            if not self.position:
                self.sell()
        elif self.lower_bound > self.rsi:
            if not self.position:
                self.buy(tp = 1.15 * price, sl = 0.95*price)