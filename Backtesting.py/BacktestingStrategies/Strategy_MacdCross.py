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
    # MACDshort = 30 #短期EMAの期間
    # MACDlong = 40 #長期EMAの期間
    # MACDsignal = 10 #シグナル（MACDのSMA）の期間

    def init(self):
        self.macd, self.macdsignal = self.I(MACD, self.data.Close, self.MACDshort, self.MACDlong, self.MACDsignal)

    def next(self): # チャートデータの行ごとに呼び出される
        if crossover(self.macd, self.macdsignal): #macdがsignalを上回った時
            self.buy() # 買い
        elif crossover(self.macdsignal, self.macd): #signalがmacdを上回った時
            self.position.close() # 売り


class MACDCross_WithShortPosition(Strategy):
    MACDshort = 12 #短期EMAの期間
    MACDlong = 26 #長期EMAの期間
    MACDsignal = 9 #シグナル（MACDのSMA）の期間
    # MACDshort = 30 #短期EMAの期間
    # MACDlong = 40 #長期EMAの期間
    # MACDsignal = 10 #シグナル（MACDのSMA）の期間

    def init(self):
        self.macd, self.macdsignal = self.I(MACD, self.data.Close, self.MACDshort, self.MACDlong, self.MACDsignal)

    def next(self): # チャートデータの行ごとに呼び出される
        if crossover(self.macd, self.macdsignal): #macdがsignalを上回った時
            #買いシグナル
            if self.position.is_short or not self.position:
                #売りポジションを持っていた場合損切
                self.position.close()
                self.buy()
        elif crossover(self.macdsignal, self.macd): #signalがmacdを上回った時
            #売りシグナル
            if self.position.is_long  or not self.position:
                #買いポジションを持っていた場合損切
                self.position.close()
                self.sell()