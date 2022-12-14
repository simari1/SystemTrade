'''
https://www.sevendata.co.jp/shihyou/mix/borirsi.html
買いポイント
    株価がボリンジャーバンドの-2σ以下まで下落
    同時にRSIが30％以下にあるのを確認してエントリー

利益確定の目安
    株価がボリンジャーバンドの+2σに到達
    またはRSIが70％以上になった場合
'''


from backtesting import Strategy
from backtesting.lib import crossover
import talib as ta

def BB(close, n, nu, nd):
    # df["upper"], df["middle"], df["lower"] = ta.BBANDS(close, timeperiod=span02, nbdevdn=2, nbdevup = 2, matype = 0)
    upper, middle, lower = ta.BBANDS(close, timeperiod=n, nbdevup=nu, nbdevdn=nd, matype=0)
    return upper, lower

def CalcATR(phigh, plow, pclose, period):
    high = pd.Series(phigh)
    low = pd.Series(plow)
    close = pd.Series(pclose)
    return ta.ATR(\
        np.array(high).astype("double"),\
        np.array(low).astype("double"),\
        np.array(close).astype("double"),\
        timeperiod=period)

class BBandRSI(Strategy):
    n = 25 #移動平均日数
    nu = 2 #何σか
    nd = 2 #何σか
    upper_bound = 70
    lower_bound = 30
    rsi_window = 14

    def init(self):
        self.upper, self.lower = self.I(BB, self.data.Close, self.n, self.nu, self.nd)
        self.rsi = self.I(ta.RSI, self.data.Close, self.rsi_window)

    def next(self): # チャートデータの行ごとに呼び出される

        #+2σより大きいなら売り
        if self.data.Close > self.upper\
            or crossover(self.rsi, self.upper_bound):
            self.position.close()
        #-2σより小さいなら買い
        elif self.data.Close < self.lower\
            and crossover(self.lower_bound, self.rsi):
            if not self.position:
                self.buy() # 買い

class BBandRSI_WithStopLoss(Strategy):
    n = 25 #移動平均日数
    nu = 2 #何σか
    nd = 2 #何σか
    upper_bound = 70
    lower_bound = 30
    rsi_window = 14
    stop_loss_perc = -7.5

    def init(self):
        self.upper, self.lower = self.I(BB, self.data.Close, self.n, self.nu, self.nd)
        self.rsi = self.I(ta.RSI, self.data.Close, self.rsi_window)

    def next(self): # チャートデータの行ごとに呼び出される
        price = self.data.Close
        #特定パーセントより損が大きければ損切
        if self.position:
            if self.position.pl_pct < self.stop_loss_perc:
                print(self.position.pl_pct)
                self.position.close()
        #売り
        if self.data.High > self.upper\
            or crossover(self.rsi, self.upper_bound):
            self.position.close()
        #買い
        elif self.data.Low < self.lower\
            or crossover(self.lower_bound, self.rsi):
            if not self.position:
                self.buy() # 買い

class BBandRSI_WithShortPosition(Strategy):
    #ボリンジャーバンド用パラメータ
    n = 25 #移動平均日数
    nu = 2 #何σか
    nd = 2 #何σか
    #RSI用パラメータ
    upper_bound = 70
    lower_bound = 30
    rsi_window = 14

    def init(self):
        self.upper, self.lower = self.I(BB, self.data.Close, self.n, self.nu, self.nd)
        self.rsi = self.I(ta.RSI, self.data.Close, self.rsi_window)

    def next(self): # チャートデータの行ごとに呼び出される
        #+2σより大きいなら売り
        if self.data.Close > self.upper\
            or crossover(self.rsi, self.upper_bound):
            #売りシグナル
            if not self.position:
                self.sell()
            else:
                self.position.close()
        #-2σより小さいなら買い
        elif self.data.Close < self.lower\
            or crossover(self.lower_bound, self.rsi):
            #買いシグナル
            if not self.position:
                self.buy() # 買い

class EntryRSI50andExitBB(Strategy):
    #ボリンジャーバンド用パラメータ
    n = 25 #移動平均日数
    nu = 2 #何σか
    nd = 2 #何σか
    #RSI用パラメータ
    upper_bound = 70
    lower_bound = 30
    rsi_window = 14

    def init(self):
        self.upper, self.lower = self.I(BB, self.data.Close, self.n, self.nu, self.nd)
        self.rsi = self.I(ta.RSI, self.data.Close, self.rsi_window)

    def next(self): # チャートデータの行ごとに呼び出される
        rsi_previous = self.rsi[-1]
        rsi_2previous = self.rsi[-2]

        if self.data.Close > self.upper or self.data.Low > self.upper:
            #BBDの上限に当たったら売りシグナル
            if self.position:
                self.position.close()
        elif rsi_2previous < 50 and rsi_previous > 50:
            #RSIの50を下から上へ突き抜けたら
            if not self.position:
                self.buy() # 買い
        elif rsi_previous < 40:
            if self.position and self.trades[-1].size > 0:
                self.position.close()
        elif rsi_previous < 60:
            if self.position and self.trades[-1].size < 0:
                self.position.close()

class EntryRSI50andExitBB_WithShortPosition(Strategy):
    #ボリンジャーバンド用パラメータ
    n = 25 #移動平均日数
    nu = 2 #何σか
    nd = 2 #何σか
    #RSI用パラメータ
    upper_bound = 50
    lower_bound = 50
    rsi_window = 14

    def init(self):
        self.upper, self.lower = self.I(BB, self.data.Close, self.n, self.nu, self.nd)
        self.rsi = self.I(ta.RSI, self.data.Close, self.rsi_window)

    def next(self): # チャートデータの行ごとに呼び出される
        rsi_previous = self.rsi[-1]
        rsi_2previous = self.rsi[-2]

        if self.data.Close > self.upper and self.position:
            #BBDの上にあたったら
            if self.position and self.trades[-1].size > 0:
                self.position.close()
        elif self.data.Close < self.lower and self.position:
            #BBDの下にあたったら
            if self.position and self.trades[-1].size < 0:
                self.position.close()
        elif rsi_2previous < 50 and rsi_previous > 50:
            #RSIの50を下から上へ突き抜けたら
            if not self.position:
                self.buy()
        elif rsi_2previous > 50 and rsi_previous < 50:
            #RSIの50を上から下へ突き抜けたら
            if not self.position:
                self.sell()
        if rsi_previous < 40:
            if self.position and self.trades[-1].size > 0:
                self.position.close()
        if rsi_previous < 60:        
            if self.position and self.trades[-1].size < 0:
                self.position.close()

class EntryRSI50andExitBBWithATRStopLoss(Strategy):
    #ボリンジャーバンド用パラメータ
    n = 25 #移動平均日数
    nu = 2 #何σか
    nd = 2 #何σか
    #RSI用パラメータ
    upper_bound = 50
    lower_bound = 50
    rsi_window = 14

    atr_period = 20

    def init(self):
        self.upper, self.lower = self.I(BB, self.data.Close, self.n, self.nu, self.nd)
        self.rsi = self.I(ta.RSI, self.data.Close, self.rsi_window)
        self.atr = self.I(CalcATR, self.data.High,  self.data.Low, self.data.Close, self.atr_period)

    def next(self): # チャートデータの行ごとに呼び出される
        rsi_previous = self.rsi[-1]
        rsi_2previous = self.rsi[-2]

        if self.data.Close > self.upper and self.position and self.trades[-1].size > 0:
            #順張り中でBBDの上にあたったら利益確定
            self.position.close()
        elif self.position and self.data.Close[-1] < self.trades[-1].entry_price - self.atr[-1] * 2:
            #順張り中でATR2倍より下がったら損切
            self.position.close()
        elif self.data.Close > self.lower and self.position and self.trades[-1].size < 0:
            #空売り中でBBDの上にあたったら利益確定
            self.position.close()
        elif self.position and self.data.Close[-1] > self.trades[-1].entry_price + self.atr[-1] * 2:
            #空売り中でATR2倍より上がったら損切
            self.position.close()
        elif rsi_2previous < 50 and rsi_previous > 50:
            #RSIの50を下から上へ突き抜けたら
            if not self.position:
                self.buy()
        elif rsi_2previous > 50 and rsi_previous < 50:
            #RSIの50を上から下へ突き抜けたら
            if not self.position:
                self.sell()