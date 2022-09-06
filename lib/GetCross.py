from pandas_datareader import data
import pandas as pd
import numpy as np

#ゴールデンクロス
#https://myfrankblog.com/find_golden_cross_and_dead_cross_by_python/
#SMA5 - SMA25をdiff(0), その1日前の値をdiff(1)とする
# 1) 2（(+1)-(-1)）だとゴールデンクロスを意味する
# 2)-2（(-1)-(+1)）だとデッドクロスを意味する
# 3)そのほかは何もないので無視する
def find_cross(short, long):
    # 差分を計算する
    diff = short - long
    # diffの各値を直前のデータで引く　2ならゴールデンクロス(GC), -2ならデッドクロス(DC)と判定する
    cross = np.where(\
                np.sign(diff) - np.sign(diff.shift(1)) == 2, "GC",\
                np.where(np.sign(diff) - np.sign(diff.shift(1)) == -2, "DC",\
                np.nan))
    return cross