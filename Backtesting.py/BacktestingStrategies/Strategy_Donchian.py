from backtesting import Strategy
import pandas as pd
import talib as ta
import numpy as np

"""
エントリー
    直近X日間の高値ブレイクでエントリー
    直近Y日間の安値ブレイクでエントリー

手じまい
    直近Y日間の安値割れ（買いの場合）or
    直近X日間の高値更新（売りの場合）
"""

def CalcDonchian_High(values, dnchn_span_long):
    dnchnline = pd.Series(values)
    return dnchnline.rolling(window = dnchn_span_long).max()

def CalcDonchian_Low(values, dnchn_span_short):
    dnchnline = pd.Series(values)
    return dnchnline.rolling(window = dnchn_span_short).min()

def CalcATR(phigh, plow, pclose, period):
    high = pd.Series(phigh)
    low = pd.Series(plow)
    close = pd.Series(pclose)
    return ta.ATR(\
        np.array(high).astype("double"),\
        np.array(low).astype("double"),\
        np.array(close).astype("double"),\
        timeperiod=period)

class DnchnBreakout(Strategy):
    dnchn_long = 20
    dnchn_short = 10
    atr_period = 20

    def init(self):
        self.dnchn_high = self.I(CalcDonchian_High, self.data.High, self.dnchn_long)
        self.dnchn_low = self.I(CalcDonchian_Low, self.data.Low, self.dnchn_short)
        self.atr = self.I(CalcATR, self.data.High,  self.data.Low, self.data.Close, self.atr_period)

    def next(self): #チャートデータの行ごとに呼び出される
        price = self.data.Close[-1]
        if price > self.dnchn_high[-2]:
            if not self.position:
                self.buy() # 買い
        elif price < self.dnchn_low[-2]:
            #売りポジションを持っていた場合損切
            self.position.close() # 売り

class DnchnBreakout_WithShortPosition(Strategy):
    dnchn_long = 20
    dnchn_short = 10
    atr_period = 20

    def init(self):
        self.dnchn_high = self.I(CalcDonchian_High, self.data.High, self.dnchn_long) 
        self.dnchn_low = self.I(CalcDonchian_Low, self.data.Low, self.dnchn_short)
        self.atr = self.I(CalcATR, self.data.High,  self.data.Low, self.data.Close, self.atr_period)

    def next(self): #チャートデータの行ごとに呼び出される
        price = self.data.Close[-1]
        if price > self.dnchn_high[-2]:
            if not self.position:
                self.buy() # 買い
        elif price < self.dnchn_low[-2]:
            #売りシグナル
            if not self.position:
                self.sell()
            else:
                self.position.close()

class DnchnBreakout_WithATRStopLoss(Strategy):
    dnchn_long = 20
    dnchn_short = 10
    atr_period = 20

    def init(self):
        self.dnchn_high = self.I(CalcDonchian_High, self.data.High, self.dnchn_long)
        self.dnchn_low = self.I(CalcDonchian_Low, self.data.Low, self.dnchn_short)
        self.atr = self.I(CalcATR, self.data.High,  self.data.Low, self.data.Close, self.atr_period)

    def next(self): #チャートデータの行ごとに呼び出される
        price = self.data.Close[-1]
        atr = self.atr[-1]
        if self.position and\
            self.trades[-1].size > 0 and\
            self.trades[-1].entry_price < price - atr * 2:
            #順張りの場合はエントリー値よりATRの2倍分下がったら損切
            self.position.close()
        elif self.position and\
            self.trades[-1].size < 0 and\
            self.trades[-1].entry_price > price + atr * 2:
            #空売りの場合はエントリー値よりATRの2倍分上がったらしたら損切
            self.position.close()
        elif price > self.dnchn_high[-2]:
            if not self.position:
                self.buy() # 買い
        elif price < self.dnchn_low[-2]:
            #売りポジションを持っていた場合売り
            self.position.close() # 売り