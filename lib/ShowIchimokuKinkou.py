from pandas_datareader import data
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf
import datetime
from dateutil import relativedelta

#次のときは、買いシグナルとなり「好転した」と言います。
#①転換線が基準線を上抜けたとき
#②遅行スパンがローソク足を上抜けたとき
#③ローソク足が雲を上抜けたとき
#さらに、①②③の買いシグナルが3つそろった場合を「三役好転」と言い、より強い買いシグナルとなります。
def show_ichimokukinkou(start, end, code):
    if __name__ == '__main__':
        import GetCross as gc
    else:
        import lib.GetCross as gc

    df = data.DataReader(code, "yahoo", start, end)
    close = df["Adj Close"]
    date = df.index
    
    #基準線用のデータを作成
    #過去26日間の最高、最低の値の平均
    high = df["High"]
    low = df["Low"]
    max26 = high.rolling(window = 26).max()
    min26 = low.rolling(window = 26).min()
    df["basic_line"] = (max26 + min26) / 2

    #転換線用のデータを作成
    #過去9日間の最高、最低の値の平均
    high9 = high.rolling(window = 9).max()
    low9 = low.rolling(window = 9).min()
    df["turn_line"] = (high9 + low9) / 2

    #先行スパンのデータを作成
    df["span1"] = (df.basic_line + df.turn_line) / 2
    high52 = high.rolling(window = 52).max()
    low52 = low.rolling(window = 52).min()
    df["span2"] = (high52 + low52) / 2

    #遅行線のデータを作成
    df["slow_line"] = df["Adj Close"].shift(-25)

    #ローソク足と一目均衡表の線をplotする
    plt.figure(figsize=(5, 5))
    
    lines = [mpf.make_addplot(df['basic_line']), #基準線
            mpf.make_addplot(df['turn_line']),   #転換線
            mpf.make_addplot(df['slow_line']),#遅行線
        ]
    labels = ["-", "-", "基準", "転換", "遅行"]
    mc = mpf.make_marketcolors(up="#DF0101", down="#00008b", volume="#6E6E6E", edge="inherit", wick="inherit")
    cs  = mpf.make_mpf_style(rc={"font.family":'MS Gothic'}, marketcolors=mc, gridstyle='-')

    fig, ax = mpf.plot(df, type='candle', figsize=(16,6), style = cs, xrotation=0, addplot=lines, returnfig=True, volume = True, title = "一目均衡表",
                    fill_between=dict(y1=df['span1'].values, y2=df['span2'].values, alpha=0.5, color='gray')) 
    ax[0].legend(labels)

if __name__ == '__main__':
    show_ichimokukinkou((datetime.datetime.today() + relativedelta.relativedelta(years=-1)), datetime.datetime.today(), "^N225")