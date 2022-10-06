'''
https://www.sevendata.co.jp/shihyou/mix/borimacd.html
買いポイント
    MACDがシグナル線より上
    その後にボリンジャー2σより上

利益確定の目安
    # 株価が+1σを下回る
    またはMACDがデットクロス
'''


from backtesting import Strategy
from backtesting.lib import crossover
import talib as ta

def MACD(close, n1, n2, ns):
    macd, macdsignal, macdhist = ta.MACD(close, fastperiod=n1, slowperiod=n2, signalperiod=ns)
    return macd, macdsignal

def BB(close, n, nu, nd):
    # df["upper"], df["middle"], df["lower"] = ta.BBANDS(close, timeperiod=span02, nbdevdn=2, nbdevup = 2, matype = 0)
    upper, middle, lower = ta.BBANDS(close, timeperiod=n, nbdevup=nu, nbdevdn=nd, matype=0)
    return upper, lower

class MACDandBBD(Strategy):
    #MACD用パラメータ
    MACDshort = 12 #短期EMAの期間
    MACDlong = 26 #長期EMAの期間
    MACDsignal = 9 #シグナル（MACDのSMA）の期間
    MACDThreshold = 0
    #ボリンジャー用パラメータ
    bolperiod = 25 #移動平均日数
    bolupper_sigma = 2 #何σか
    bollower_sigma = 2 #何σか

    def init(self):
        self.macd, self.macdsignal = self.I(MACD, self.data.Close, self.MACDshort, self.MACDlong, self.MACDsignal)
        self.bolupper_sigma, self.bollower_sigma = self.I(BB, self.data.Close, self.bolperiod, self.bolupper_sigma, self.bollower_sigma)

    def next(self): # チャートデータの行ごとに呼び出される
        if self.macd < self.MACDThreshold and self.macdsignal < self.MACDThreshold and crossover(self.macd, self.macdsignal)\
            and crossover(self.data.Close, self.bolupper_sigma):
            if not self.position:
                self.buy() # 買い
        elif self.macd > self.MACDThreshold and self.macdsignal > self.MACDThreshold and crossover(self.macdsignal, self.macd):
            self.position.close() # 手じまい

class MACDandBBD_WithShortPosition(Strategy):
    #MACD用パラメータ
    MACDshort = 12 #短期EMAの期間
    MACDlong = 26 #長期EMAの期間
    MACDsignal = 9 #シグナル（MACDのSMA）の期間
    MACDThreshold = 0
    #ボリンジャー用パラメータ
    bolperiod = 25 #移動平均日数
    bolupper_sigma = 2 #何σか
    bollower_sigma = 2 #何σか

    def init(self):
        self.macd, self.macdsignal = self.I(MACD, self.data.Close, self.MACDshort, self.MACDlong, self.MACDsignal)
        self.bolupper_sigma, self.bollower_sigma = self.I(BB, self.data.Close, self.bolperiod, self.bolupper_sigma, self.bollower_sigma)

    def next(self): # チャートデータの行ごとに呼び出される
        if self.macd < self.MACDThreshold and self.macdsignal < self.MACDThreshold and crossover(self.macd, self.macdsignal)\
            and crossover(self.data.Close, self.bolupper_sigma):
            #買いシグナル
            if not self.position:
                self.buy() # 買い
        elif self.macd > self.MACDThreshold and self.macdsignal > self.MACDThreshold and crossover(self.macdsignal, self.macd):
            #売りシグナル
            if not self.position:
                self.sell()
            else:
                self.position.close()