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
            if not self.position:
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
            if not self.position:
                self.sell()
            else:
                self.position.close()
        #-2σより小さいなら買い
        elif self.data.Close < self.lower\
            or crossover(self.lower_bound, self.rsi):
            #買いシグナル
            if not self.position:
                self.buy() # 買い

class EntryRSI50andExitBB(Strategy):
    #ボリンジャーバンド用パラメータ
    n = 25 #移動平均日数
    nu = 2 #何σか
    nd = 2 #何σか
    #RSI用パラメータ
    upper_bound = 70
    lower_bound = 50
    rsi_window = 14

    def init(self):
        self.upper, self.lower = self.I(BB, self.data.Close, self.n, self.nu, self.nd)
        self.rsi = self.I(ta.RSI, self.data.Close, self.rsi_window)

    def next(self): # チャートデータの行ごとに呼び出される
        if self.data.Close > self.upper:
            #売りシグナル
            self.position.close()
        elif crossover(self.rsi, self.lower_bound):
            if not self.position:
                self.buy() # 買い

class EntryRSI50andExitBB_WithShortPosition(Strategy):
    #ボリンジャーバンド用パラメータ
    n = 25 #移動平均日数
    nu = 2 #何σか
    nd = 2 #何σか
    #RSI用パラメータ
    upper_bound = 45
    lower_bound = 55
    rsi_window = 14

    def init(self):
        self.upper, self.lower = self.I(BB, self.data.Close, self.n, self.nu, self.nd)
        self.rsi = self.I(ta.RSI, self.data.Close, self.rsi_window)

    def next(self): # チャートデータの行ごとに呼び出される
        if self.data.Close > self.upper:
            self.position.close()
        elif self.data.Close < self.lower:
            self.position.close()
        elif crossover(self.rsi, self.lower_bound):
            if not self.position:
                self.buy()
        elif crossover(self.upper_bound, self.rsi):
            if not self.position:
                self.sell()