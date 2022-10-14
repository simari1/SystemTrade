#https://optrip.xyz/?p=3346
from backtesting import Strategy # バックテスト、ストラテジー
import talib as ta
from backtesting.lib import crossover

def MACD(close, MACDshort, MACDlong, MACDsignal):
    macd, macdsignal, macdhist = ta.MACD(close, fastperiod=MACDshort, slowperiod=MACDlong, signalperiod=MACDsignal)
    return macd, macdsignal, macdhist
class MACDCross(Strategy):
    # MACDshort=20
    # MACDlong=40
    # MACDsignal=10
    # MACDThresholdPlus=30
    # MACDThresholdMinus=-120

    MACDshort = 12 #短期EMAの期間
    MACDlong = 26 #長期EMAの期間
    MACDsignal = 9 #シグナル（MACDのSMA）の期間
    MACDThresholdPlus = 0
    MACDThresholdMinus = -150

    # MACDshort = 12 #短期EMAの期間
    # MACDlong = 26 #長期EMAの期間
    # MACDsignal = 9 #シグナル（MACDのSMA）の期間
    # MACDThresholdPlus = 100
    # MACDThresholdMinus = -100

    def init(self):
        self.macd, self.macdsignal, self.macdhist = self.I(MACD, self.data.Close, self.MACDshort, self.MACDlong, self.MACDsignal)

    def next(self): # チャートデータの行ごとに呼び出される
        if self.macd < self.MACDThresholdMinus and\
            self.macdsignal < self.MACDThresholdMinus and\
            crossover(self.macd, self.macdsignal):\
            #macdがsignalを上回った時
            if not self.position:
                self.buy() # 買い
        elif self.position and self.macdhist[-1] < self.macdhist[-2] and self.macdhist[-2] < self.macdhist[-3]:
            self.position.close()
        elif self.position and crossover(self.macdsignal, self.macd):
            self.position.close()

class MACDCross_WithShortPosition(Strategy):
    # MACDshort=15
    # MACDlong=30
    # MACDsignal=10
    # MACDThresholdPlus=460
    # MACDThresholdMinus=-80

    MACDshort = 12 #短期EMAの期間
    MACDlong = 26 #長期EMAの期間
    MACDsignal = 9 #シグナル（MACDのSMA）の期間
    MACDThresholdPlus = 460
    MACDThresholdMinus = -140

    # MACDshort = 12 #短期EMAの期間
    # MACDlong = 26 #長期EMAの期間
    # MACDsignal = 9 #シグナル（MACDのSMA）の期間
    # MACDThresholdPlus = 100
    # MACDThresholdMinus = -100

    def init(self):
        self.macd, self.macdsignal, self.macdhist = self.I(MACD, self.data.Close, self.MACDshort, self.MACDlong, self.MACDsignal)

    def next(self): # チャートデータの行ごとに呼び出される
        if self.macd < self.MACDThresholdMinus and\
            self.macdsignal < self.MACDThresholdMinus and\
            crossover(self.macd, self.macdsignal):\
            #macdがsignalを上回った時
            if not self.position:
                self.buy() # 買い
        elif self.macd > self.MACDThresholdPlus and\
            self.macdsignal > self.MACDThresholdPlus and\
            crossover(self.macdsignal, self.macd):
            if not self.position:
                self.sell() # 買い
        elif self.position.is_long and self.macdhist[-1] < self.macdhist[-2] and self.macdhist[-2] < self.macdhist[-3]:
            self.position.close()
        elif self.position.is_short and self.macdhist[-1] > self.macdhist[-2] and self.macdhist[-2] > self.macdhist[-3]:
            self.position.close()
        elif self.position.is_long and crossover(self.macdsignal, self.macd):
            self.position.close()
        elif self.position.is_short and crossover(self.macd, self.macdsignal):
            self.position.close()