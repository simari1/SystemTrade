#https://www.youtube.com/watch?v=9m987swadQU
from backtesting import Strategy
from backtesting.lib import resample_apply

class Momentum(Strategy):

    small_threshold = 0
    large_threshold = 3
    period_long = 7
    period_short = 2

    def momentum(self, data):
        return data.pct_change(periods=7).to_numpy() * 100

    def init(self):
        self.pct_change_long = resample_apply(str(self.period_long) + "D", self.momentum, self.data.Close)
        self.pct_change_short = resample_apply(str(self.period_short) + "D", self.momentum, self.data.Close)

    def next(self): # チャートデータの行ごとに呼び出される
        change_long = self.pct_change_long[-1]
        change_short = self.pct_change_long[-1]

        if self.position:
            # print("change_short:" + str(change_short) + "   " + "self.small_threshold:" + str(self.small_threshold))

            #check if close
            if self.position.is_long and change_short < self.small_threshold:
                self.position.close()
            elif self.position.is_short and change_short > -1 * self.small_threshold:
                self.position.close()
        else:
            #check if buy/sell
            if change_long > self.large_threshold and change_short > self.small_threshold:
                self.buy()
            elif change_long < -1 * self.large_threshold and change_short < -1 * self.small_threshold:
                self.sell()
