# https://github.com/yuyasugano/backtesting_sample/blob/master/EMA-Strategy-with-Backtesting.py.ipynb

from backtesting import Strategy
from backtesting.lib import crossover
import pandas as pd
import talib as ta

def EMA_Backtesting(values, n):
    close = pd.Series(values)
    return ta.EMA(close, timeperiod=n)

class EmaCrossStrategy(Strategy):

    # Define the two EMA lags as *class variables*
    # for later optimization
    EMAshort = 5
    EMAlong = 10

    def init(self):
        # Precompute two moving averages
        self.ema1 = self.I(EMA_Backtesting, self.data.Close, self.EMAshort)
        self.ema2 = self.I(EMA_Backtesting, self.data.Close, self.EMAlong)

    def next(self):
        # If ema1 crosses above ema2, buy the asset
        if crossover(self.ema1, self.ema2):
            if not self.position:
                self.buy() # 買い
        # Else, if ema1 crosses below ema2, sell it
        elif crossover(self.ema2, self.ema1):
            self.position.close()

class EmaCrossStrategy_WithShortPosition(Strategy):

    # Define the two EMA lags as *class variables*
    # for later optimization
    EMAshort = 5
    EMAlong = 10

    def init(self):
        # Precompute two moving averages
        self.ema1 = self.I(EMA_Backtesting, self.data.Close, self.EMAshort)
        self.ema2 = self.I(EMA_Backtesting, self.data.Close, self.EMAlong)

    def next(self):
        # If ema1 crosses above ema2, buy the asset
        if crossover(self.ema1, self.ema2):
            #買いシグナル
            if not self.position:
                self.buy() # 買い
        # Else, if ema1 crosses below ema2, sell it
        elif crossover(self.ema2, self.ema1):
            #売りシグナル
            if not self.position:
                self.sell()
            else:
                self.position.close()