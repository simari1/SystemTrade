#https://qiita.com/Fujinoinvestor/items/f2bdaabb766db443ddc0

from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import SMA

class SmaCross(Strategy):
    n1 = 10 # 短期SMA
    n2 = 30 # 長期SMA

    def init(self):
        self.sma1 = self.I(SMA, self.data.Close, self.n1) 
        self.sma2 = self.I(SMA, self.data.Close, self.n2)

    def next(self): #チャートデータの行ごとに呼び出される
        if crossover(self.sma1, self.sma2): #sma1がsma2を上回った時
            self.buy() # 買い
        elif crossover(self.sma2, self.sma1):
            self.position.close() # 売り

class SmaCross_WithShortPosition(Strategy):
    n1 = 10 # 短期SMA
    n2 = 30 # 長期SMA

    def init(self):
        self.sma1 = self.I(SMA, self.data.Close, self.n1) 
        self.sma2 = self.I(SMA, self.data.Close, self.n2)

    def next(self): #チャートデータの行ごとに呼び出される
        if crossover(self.sma1, self.sma2): #sma1がsma2を上回った時
            #買いシグナル
            if self.position.is_short or not self.position:
                #売りポジションを持っていた場合損切
                self.position.close()
                self.buy()
        elif crossover(self.sma2, self.sma1):
            #売りシグナル
            if self.position.is_long or not self.position:
                #買いポジションを持っていた場合損切
                self.position.close()
                self.sell()