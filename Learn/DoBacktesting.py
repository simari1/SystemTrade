
import pandas_datareader.data as web
import datetime
from decimal import Decimal
from dateutil import relativedelta

# start = datetime.date(2021,1,1)
start = datetime.datetime.today() + relativedelta.relativedelta(years=-1)
end = datetime.date.today()
# data = web.DataReader('7203.T', 'yahoo', start, end)
data = web.DataReader('BTC-JPY', 'yahoo', start, end)
# data = web.DataReader('1321.T', 'yahoo', start, end)
# data = web.DataReader('^N225', 'yahoo', start, end)
# data = web.DataReader('AAPL', 'yahoo', start, end)
data = data.astype("double")
print(data)

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

# バックテストを設定
bt = Backtest(
    data, # チャートデータ
    MACDCross, # 売買戦略
    cash=10000000, # 最初の所持金
    commission=0.00495, # 取引手数料
    margin=1.0, # レバレッジ倍率の逆数（0.5で2倍レバレッジ）
    trade_on_close=True, # True：現在の終値で取引，False：次の時間の始値で取引
    exclusive_orders=True #自動でポジションをクローズ(オープン)
)

output = bt.run() # バックテスト実行
print(output) # 実行結果(データ)
bt.plot() # 実行結果（グラフ）

# #最適化
output2=bt.optimize(n1=range(10, 100, 10),n2=range(10, 300, 10),ns=range(10, 50, 5), maximize='Equity Final [$]', method='grid')
print(output2)
bt.plot()
