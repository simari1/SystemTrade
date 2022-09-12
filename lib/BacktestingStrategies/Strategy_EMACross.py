# https://github.com/yuyasugano/backtesting_sample/blob/master/EMA-Strategy-with-Backtesting.py.ipynb

from backtesting import Strategy
from backtesting.lib import crossover
import pandas as pad
import talib as ta

def EMA_Backtesting(values, n):
    close = pad.Series(values)
    return ta.EMA(close, timeperiod=n)

class EmaCrossStrategy(Strategy):
    
    # Define the two EMA lags as *class variables*
    # for later optimization
    n1 = 5
    n2 = 10
    
    def init(self):
        # Precompute two moving averages
        self.ema1 = self.I(EMA_Backtesting, self.data.Close, self.n1)
        self.ema2 = self.I(EMA_Backtesting, self.data.Close, self.n2)
    
    def next(self):       
        # If ema1 crosses above ema2, buy the asset
        if crossover(self.ema1, self.ema2):
            self.position.close()
            self.buy()

        # Else, if ema1 crosses below ema2, sell it
        elif crossover(self.ema2, self.ema1):
            self.position.close()
            # 空売りなし
            # self.sell()