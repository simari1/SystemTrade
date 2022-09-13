#https://optrip.xyz/?p=3557
from backtesting import Strategy
from backtesting.lib import crossover
import pandas as pad
import talib as ta
 
def BB(close, n, nu, nd):
    # df["upper"], df["middle"], df["lower"] = ta.BBANDS(close, timeperiod=span02, nbdevdn=2, nbdevup = 2, matype = 0)
    upper, middle, lower = ta.BBANDS(close, timeperiod=n, nbdevup=nu, nbdevdn=nd, matype=0)
    return upper, lower

class BBsigma(Strategy):
    n = 25 #移動平均日数
    nu = 2 #何σか
    nd = 2 #何σか
 
    def init(self):
        self.upper, self.lower = self.I(BB, self.data.Close, self.n, self.nu, self.nd)
 
    def next(self): # チャートデータの行ごとに呼び出される
         #+3σより大きいなら売り
        if self.data.Close > self.upper:
            self.position.close()
        #-3σより小さいなら買い
        elif self.data.Close < self.lower:
            self.buy() # 買い