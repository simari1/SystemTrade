from backtesting import Strategy
from backtesting.lib import crossover, barssince
import talib as ta
from backtesting.lib import crossover, resample_apply

'''
POC用のStrategyを含む
'''

class RsiOscillator(Strategy):
    upper_bound = 70
    lower_bound = 30
    rsi_window = 14

    def init(self):
        # RSI = ta.RSI(close, timeperiod=14)
        # param 1 --- function to calculate indicator values
        # param 2 --- pass data
        self.rsi = self.I(ta.RSI, self.data.Close, self.rsi_window)

    def next(self): # チャートデータの行ごとに呼び出される
        if crossover(self.rsi, self.upper_bound):
            self.position.close()
        elif crossover(self.rsi, self.lower_bound):
            if not self.position:
                self.buy() # 買い

class RsiOscillator_WithShortPosition(Strategy):
    upper_bound = 60
    lower_bound = 40
    rsi_window = 14

    def init(self):
        self.daily_rsi = self.I(ta.RSI, self.data.Close, self.rsi_window)

    #[-1]が一番最近のデータを表す
    def next(self): # チャートデータの行ごとに呼び出される
        if crossover(self.daily_rsi, self.upper_bound):
            #売りシグナル
            if not self.position:
                self.sell()
            else:
                self.position.close()
        elif crossover(self.lower_bound, self.daily_rsi):
            #買いシグナル
            if not self.position:
                self.buy() # 買い

class RsiOscillator_WithWeekly(Strategy):
    upper_bound = 70
    lower_bound = 30
    rsi_window = 14

    def init(self):
        self.daily_rsi = self.I(ta.RSI, self.data.Close, self.rsi_window)
        self.weekly_rsi = resample_apply(\
            "W-FRI", ta.RSI, self.data.Close, self.rsi_window\
            )

    #[-1]が一番最近のデータを表す
    def next(self): # チャートデータの行ごとに呼び出される
        if (crossover(self.daily_rsi, self.upper_bound)
            and self.weekly_rsi[-1] > self.upper_bound):
            self.position.close()
        elif (crossover(self.lower_bound, self.daily_rsi)
        and self.weekly_rsi[-1] < self.lower_bound):
            self.buy()

class RsiOscillator_WithStopLoss(Strategy):
    upper_bound = 70
    lower_bound = 30
    rsi_window = 14

    def init(self):
        self.rsi = self.I(ta.RSI, self.data.Close, self.rsi_window)

    def next(self): # チャートデータの行ごとに呼び出される
        price = self.data.Close[-1]
        if crossover(self.rsi, self.upper_bound):
            self.position.close()
        elif crossover(self.rsi, self.lower_bound):
            #take profit, stop loss
            self.buy(size = 1, tp = 1.15 * price, sl = 0.95*price)

class RsiOscillator_BuySize(Strategy):
    upper_bound = 70
    lower_bound = 30
    rsi_window = 14

    def init(self):
        self.rsi = self.I(ta.RSI, self.data.Close, self.rsi_window)

    def next(self): # チャートデータの行ごとに呼び出される
        price = self.data.Close[-1]
        if crossover(self.rsi, self.upper_bound):
            self.position.close()
        elif self.lower_bound > self.rsi[-1]:
            self.buy(size = 1)

class RsiOscillator_BarsSince(Strategy):
    upper_bound = 70
    lower_bound = 30
    rsi_window = 14

    def init(self):
        self.rsi = self.I(ta.RSI, self.data.Close, self.rsi_window)

    def next(self): # チャートデータの行ごとに呼び出される
        price = self.data.Close[-1]
        if (self.rsi[-1] > self.upper_bound and\
            barssince(self.rsi < self.upper_bound) == 3):
            #rsiが上限より小さくなってから3日間経ったらポジションを閉じる
            self.position.close()
        elif self.lower_bound > self.rsi[-1]:
            self.buy(size = 1)


class RsiOscillator_Entry50(Strategy):
    upper_bound = 70
    lower_bound = 30
    rsi_window = 14

    def init(self):
        # RSI = ta.RSI(close, timeperiod=14)
        # param 1 --- function to calculate indicator values
        # param 2 --- pass data
        self.rsi = self.I(ta.RSI, self.data.Close, self.rsi_window)

    def next(self): # チャートデータの行ごとに呼び出される
        rsi_previous = self.rsi[-1]
        rsi_2previous = self.rsi[-2]

        if rsi_previous > self.upper_bound:
            if self.position:
                self.position.close()
        elif rsi_previous < 40:
            if self.position:
                self.position.close()
        elif rsi_2previous < 50 and rsi_previous > 50:
            #RSIの50を下から上へ突き抜けたら
            if not self.position:
                self.buy() # 買い

class RsiOscillator_Entry50_WithShortPosition(Strategy):
    upper_bound = 70
    lower_bound = 30
    rsi_window = 14

    def init(self):
        self.daily_rsi = self.I(ta.RSI, self.data.Close, self.rsi_window)

    #[-1]が一番最近のデータを表す
    def next(self): # チャートデータの行ごとに呼び出される
        rsi_previous = self.daily_rsi[-1]
        rsi_2previous = self.daily_rsi[-2]

        if rsi_previous > self.upper_bound:
            #順張り利確
            if self.position and self.trades[-1].size > 0:
                self.position.close()
        elif rsi_2previous < 50 and rsi_previous > 50:
            #RSIの50を下から上へ突き抜けたら
            if not self.position:
                self.buy() # 買い
        if rsi_previous < self.lower_bound:
            #空売り利確
            if self.position and self.trades[-1].size < 0:
                self.position.close()
        elif rsi_2previous > 50 and rsi_previous < 50:
            #RSIの50を下から上へ突き抜けたら
            if not self.position:
                self.sell() # 買い
        elif rsi_previous < 40:
            if self.position and self.trades[-1].size > 0:
                self.position.close()
        elif rsi_previous < 60:
            if self.position and self.trades[-1].size < 0:
                self.position.close()