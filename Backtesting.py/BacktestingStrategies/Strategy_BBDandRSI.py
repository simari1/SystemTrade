#https://optrip.xyz/?p=3557
from backtesting import Strategy
from backtesting.lib import crossover
import pandas as pad
import talib as ta
 
def BB(close, n, nu, nd):
    # df["upper"], df["middle"], df["lower"] = ta.BBANDS(close, timeperiod=span02, nbdevdn=2, nbdevup = 2, matype = 0)
    upper, middle, lower = ta.BBANDS(close, timeperiod=n, nbdevup=nu, nbdevdn=nd, matype=0)
    return upper, lower

class BBandRSI(Strategy):
    n = 25 #移動平均日数
    nu = 2 #何σか
    nd = 2 #何σか
    upper_bound = 60
    lower_bound = 40
    rsi_window = 14
 
    def init(self):
        self.upper, self.lower = self.I(BB, self.data.Close, self.n, self.nu, self.nd)
        self.rsi = self.I(ta.RSI, self.data.Close, self.rsi_window)
 
    def next(self): # チャートデータの行ごとに呼び出される
         #+2σより大きいなら売り
        if self.data.Close > self.upper or self.data.Open > self.upper\
            or crossover(self.rsi, self.upper_bound):
            self.position.close()
        #-2σより小さいなら買い
        elif self.data.Close < self.lower or self.data.Open < self.lower\
            or crossover(self.lower_bound, self.rsi):
            self.buy() # 買い

class BBandRSI_WithShortPosition(Strategy):
    n = 25 #移動平均日数
    nu = 2 #何σか
    nd = 2 #何σか
    upper_bound = 60
    lower_bound = 40
    rsi_window = 14
 
    def init(self):
        self.upper, self.lower = self.I(BB, self.data.Close, self.n, self.nu, self.nd)
        self.rsi = self.I(ta.RSI, self.data.Close, self.rsi_window)
 
    def next(self): # チャートデータの行ごとに呼び出される
         #+2σより大きいなら売り
        if self.data.Close > self.upper or self.data.Open > self.upper\
            or crossover(self.rsi, self.upper_bound):
            #売りシグナル
            if self.position.is_long or not self.position:
                #買いポジションを持っていた場合損切
                self.position.close()
                self.sell()
        #-2σより小さいなら買い
        elif self.data.Close < self.lower or self.data.Open < self.lower\
            or crossover(self.lower_bound, self.rsi):
            #買いシグナル
            if self.position.is_short or not self.position:
                #売りポジションを持っていた場合損切
                self.position.close()
                self.buy()