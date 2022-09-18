#https://optrip.xyz/?p=3557
from backtesting import Strategy
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
        #2σより大きいなら売り
        if self.data.Close > self.upper or self.data.Open > self.upper:
            self.position.close()
        #-2σより小さいなら買い
        elif self.data.Close < self.lower or self.data.Open < self.lower:
            if not self.position:
                self.buy() # 買い

        # メモ：これは以下と同じ
        # if self.data.Close[-1] > self.upper[-1] :
        #     self.position.close()
        # elif self.data.Close[-1]  < self.lower[-1] :
        #     self.buy() # 買い

class BBsigma_WithShortPosition(Strategy):
    n = 25 #移動平均日数
    nu = 2 #何σか
    nd = 2 #何σか

    def init(self):
        self.upper, self.lower = self.I(BB, self.data.Close, self.n, self.nu, self.nd)

    def next(self): # チャートデータの行ごとに呼び出される
        if self.data.Close > self.upper or self.data.Open > self.upper:
            #売りシグナル
            if not self.position:
                self.sell()
            else:
                self.position.close()
        elif self.data.Close < self.lower or self.data.Open < self.lower:
            #買いシグナル
            if not self.position:
                self.buy() # 買い