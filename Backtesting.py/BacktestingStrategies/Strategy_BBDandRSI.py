'''
https://www.sevendata.co.jp/shihyou/mix/borirsi.html
買いポイント
    株価がボリンジャーバンドの-2σ以下まで下落
    同時にRSIが30％以下にあるのを確認してエントリー

利益確定の目安
    株価がボリンジャーバンドの+2σに到達
    またはRSIが70％以上になった場合
'''


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
    upper_bound = 70
    lower_bound = 30
    rsi_window = 14

    def init(self):
        self.upper, self.lower = self.I(BB, self.data.Close, self.n, self.nu, self.nd)
        self.rsi = self.I(ta.RSI, self.data.Close, self.rsi_window)

    def next(self): # チャートデータの行ごとに呼び出される
        #+2σより大きいなら売り
        if self.data.Close > self.upper\
            or crossover(self.rsi, self.upper_bound):
            self.position.close()
        #-2σより小さいなら買い
        elif self.data.Close < self.lower\
            or crossover(self.lower_bound, self.rsi):
            self.buy() # 買い

class BBandRSI_WithShortPosition(Strategy):
    #ボリンジャーバンド用パラメータ
    n = 25 #移動平均日数
    nu = 2 #何σか
    nd = 2 #何σか
    #RSI用パラメータ
    upper_bound = 70
    lower_bound = 30
    rsi_window = 14

    def init(self):
        self.upper, self.lower = self.I(BB, self.data.Close, self.n, self.nu, self.nd)
        self.rsi = self.I(ta.RSI, self.data.Close, self.rsi_window)

    def next(self): # チャートデータの行ごとに呼び出される
        #+2σより大きいなら売り
        if self.data.Close > self.upper\
            or crossover(self.rsi, self.upper_bound):
            #売りシグナル
            if self.position.is_long or not self.position:
                #買いポジションを持っていた場合損切
                self.position.close()
                self.sell()
        #-2σより小さいなら買い
        elif self.data.Close < self.lower\
            or crossover(self.lower_bound, self.rsi):
            #買いシグナル
            if self.position.is_short or not self.position:
                #売りポジションを持っていた場合損切
                self.position.close()
                self.buy()