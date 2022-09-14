#https://qiita.com/Fujinoinvestor/items/f2bdaabb766db443ddc0

from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import SMA

class SmaCross(Strategy):
    SMA_short = 10 # 短期SMA
    SMA_long = 30 # 長期SMA

    def init(self):
        self.sma1 = self.I(SMA, self.data.Close, self.SMA_short) 
        self.sma2 = self.I(SMA, self.data.Close, self.SMA_long)

    def next(self): #チャートデータの行ごとに呼び出される
        if crossover(self.sma1, self.sma2): #sma1がsma2を上回った時
            if not self.position:
                self.buy() # 買い
        elif crossover(self.sma2, self.sma1):
            self.position.close() # 売り

class SmaCross_WithShortPosition(Strategy):
    SMA_short = 10 # 短期SMA
    SMA_long = 30 # 長期SMA

    def init(self):
        self.sma1 = self.I(SMA, self.data.Close, self.SMA_short) 
        self.sma2 = self.I(SMA, self.data.Close, self.SMA_long)

    def next(self): #チャートデータの行ごとに呼び出される
        if crossover(self.sma1, self.sma2): #sma1がsma2を上回った時
            #買いシグナル
            if not self.position:
                self.buy() # 買い
        elif crossover(self.sma2, self.sma1):
            #売りシグナル
            if not self.position:
                self.sell()
            else:
                self.position.close()