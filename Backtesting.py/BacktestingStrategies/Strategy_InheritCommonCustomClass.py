import importlib
from backtesting import Strategy
from backtesting.lib import crossover
import talib as ta
from backtesting.lib import crossover
# from BacktestingStrategies.Super_Strategies.CustomClass import SuperStrategy
import BacktestingStrategies.Super_Strategies.CustomClass as ss
importlib.reload(ss)
class RsiOscillator(Strategy, ss.SuperStrategy):
    """テスト用に共通のスーパークラスを継承したカスタムクラス

    Args:
        Strategy (_type_): Backtesting.pyのStrategyクラスを継承
        ss (_type_): カスタムスーパークラスを継承したもの
    """
    upper_bound=60
    lower_bound=40
    rsi_window=12
    atr_window=14
    atr_stoploss=4
    atr_takeprofit=8

    def init(self):
        # RSI = ta.RSI(close, timeperiod=14)
        # param 1 --- function to calculate indicator values
        # param 2 --- pass data
        self.rsi = self.I(ta.RSI, self.data.Close, self.rsi_window)
        self.atr = self.I(ta.ATR, self.data.High , self.data.Low, self.data.Close, self.atr_window)

        #Dataframe作成
        self.setdata(self.data)

    def next(self): # チャートデータの行ごとに呼び出される
        if self.position:
            price = self.trades[-1].entry_price
            if self.data.Low[-1] > price + (self.atr[-1] * self.atr_takeprofit) or\
                self.data.Low[-1] < price - (self.atr[-1] * self.atr_stoploss):
                #ATR損切/利確
                if self.data.Low[-1] > price + (self.atr[-1] * self.atr_takeprofit):
                    print("take profit  " + str(self.data.index[-1]) + "  " +
                    str(price) + "  " + str(price + (self.atr[-1] * self.atr_takeprofit)))
                if self.data.Low[-1] < price - (self.atr[-1] * self.atr_stoploss):
                    print("stop loss  " + str(self.data.index[-1]) + "  " +
                    str(price) + "  " + str(price - (self.atr[-1] * self.atr_stoploss)))
                self.position.close()
            elif crossover(self.upper_bound, self.rsi):
                #RSI利益確定
                print("RSI close " + str(self.data.index[-1]))
                self.position.close()
        elif crossover(self.lower_bound, self.rsi):
            if not self.position:
                self.buy() # 買い