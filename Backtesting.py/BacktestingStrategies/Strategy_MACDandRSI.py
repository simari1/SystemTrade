'''
https://www.sevendata.co.jp/shihyou/mix/macdrsi.html
買いポイント
    株価が下落し、14日RSIが20％以下になったのを確認する
    その後にMACDがゴールデンクロスしたらエントリー

利益確定の目安
    MACDがデットクロスする、または14日RSIが80％になった場合
'''


from backtesting import Strategy
from backtesting.lib import crossover
import pandas as pad
import talib as ta

def MACD(close, n1, n2, ns):
    macd, macdsignal, macdhist = ta.MACD(close, fastperiod=n1, slowperiod=n2, signalperiod=ns)
    return macd, macdsignal

class MACDandRSI(Strategy):
    #MACD用パラメータ
    MACDshort = 12 #短期EMAの期間
    MACDlong = 26 #長期EMAの期間
    MACDsignal = 9 #シグナル（MACDのSMA）の期間
    #RSI用パラメータ
    upper_bound = 70
    lower_bound = 30
    rsi_window = 14

    def init(self):
        self.macd, self.macdsignal = self.I(MACD, self.data.Close, self.MACDshort, self.MACDlong, self.MACDsignal)
        self.rsi = self.I(ta.RSI, self.data.Close, self.rsi_window)

    def next(self): # チャートデータの行ごとに呼び出される
        if self.rsi[-1] > self.upper_bound\
            or crossover(self.macdsignal, self.macd):
            self.position.close()
        elif self.rsi[-1] < self.lower_bound\
            and crossover(self.macd, self.macdsignal):
            if not self.position:
                self.buy() # 買い
            else:
                self.position.close()
                self.buy() # 買い

class MACDandRSI_WithShortPosition(Strategy):
    #MACD用パラメータ
    MACDshort = 12 #短期EMAの期間
    MACDlong = 26 #長期EMAの期間
    MACDsignal = 9 #シグナル（MACDのSMA）の期間
    #RSI用パラメータ
    upper_bound = 70
    lower_bound = 30
    rsi_window = 14

    def init(self):
        self.macd, self.macdsignal = self.I(MACD, self.data.Close, self.MACDshort, self.MACDlong, self.MACDsignal)
        self.rsi = self.I(ta.RSI, self.data.Close, self.rsi_window)

    def next(self): # チャートデータの行ごとに呼び出される
        if self.rsi[-1] > self.upper_bound\
            or crossover(self.macdsignal, self.macd):
            #売りシグナル
            if not self.position:
                self.sell()
            else:
                self.position.close()
                self.sell()
        elif self.rsi[-1] < self.lower_bound\
            and crossover(self.macd, self.macdsignal):
            #買いシグナル
            if not self.position:
                self.buy() # 買い
            else:
                self.position.close()
                self.buy() # 買い