#https://optrip.xyz/?p=3346
from backtesting import Backtest, Strategy # バックテスト、ストラテジー
from backtesting.lib import crossover
import talib as ta

def MACD(close, MACDshort, MACDlong, MACDsignal):
    macd, macdsignal, macdhist = ta.MACD(close, fastperiod=MACDshort, slowperiod=MACDlong, signalperiod=MACDsignal)
    return macd, macdsignal

class MACDCross(Strategy):
    MACDshort = 12 #短期EMAの期間
    MACDlong = 26 #長期EMAの期間
    MACDsignal = 9 #シグナル（MACDのSMA）の期間

    def init(self):
        self.macd, self.macdsignal = self.I(MACD, self.data.Close, self.MACDshort, self.MACDlong, self.MACDsignal)

    def next(self): # チャートデータの行ごとに呼び出される
        if crossover(self.macd, self.macdsignal): #macdがsignalを上回った時
            if not self.position:
                self.buy() # 買い
            else:
                self.position.close()
                self.buy() # 買い
        elif crossover(self.macdsignal, self.macd): #signalがmacdを上回った時
            self.position.close()


class MACDCross_WithShortPosition(Strategy):
    MACDshort = 12 #短期EMAの期間
    MACDlong = 26 #長期EMAの期間
    MACDsignal = 9 #シグナル（MACDのSMA）の期間

    def init(self):
        self.macd, self.macdsignal = self.I(MACD, self.data.Close, self.MACDshort, self.MACDlong, self.MACDsignal)

    def next(self): # チャートデータの行ごとに呼び出される
        if crossover(self.macd, self.macdsignal): #macdがsignalを上回った時
            #買いシグナル
            if not self.position:
                self.buy() # 買い
            else:
                self.position.close()
                self.buy() # 買い
        elif crossover(self.macdsignal, self.macd): #signalがmacdを上回った時
            #売りシグナル
            if not self.position:
                self.sell()
            else:
                self.position.close()
                self.sell()