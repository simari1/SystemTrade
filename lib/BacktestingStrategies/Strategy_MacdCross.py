from backtesting import Backtest, Strategy # バックテスト、ストラテジー
from backtesting.lib import crossover
import talib as ta

def MACD(close, n1, n2, ns):
    macd, macdsignal, macdhist = ta.MACD(close, fastperiod=n1, slowperiod=n2, signalperiod=ns)
    return macd, macdsignal

class MACDCross(Strategy):
    n1 = 12 #短期EMAの期間
    n2 = 26 #長期EMAの期間
    ns = 9 #シグナル（MACDのSMA）の期間
    # n1 = 30 #短期EMAの期間
    # n2 = 40 #長期EMAの期間
    # ns = 10 #シグナル（MACDのSMA）の期間

    def init(self):
        self.macd, self.macdsignal = self.I(MACD, self.data.Close, self.n1, self.n2, self.ns)

    def next(self): # チャートデータの行ごとに呼び出される
        if crossover(self.macd, self.macdsignal): #macdがsignalを上回った時
            self.buy() # 買い
        elif crossover(self.macdsignal, self.macd): #signalがmacdを上回った時
            self.position.close() # 売り