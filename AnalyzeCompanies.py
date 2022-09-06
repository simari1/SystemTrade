import pandas as pd
import matplotlib.pyplot as plt

def get_pie_ratio(comapny_labels):
    plt.figure(figsize=(10, 8)) # グラフ自体のサイズ（幅、高さ）
    plt.rcParams['font.family'] = "MS Gothic"
    plt.pie(
        sizes,
        labels=comapny_labels,
        counterclock=False, # 時計回りに比率が高い順の設定
        startangle=90,  # 表示のアングルを調整
    )
    plt.title('Pie Chart', fontsize=25) # グラフタイトル
    plt.show() # グラフを表示

#東証一部の銘柄の構成比
data_frame = pd.read_csv("./data/prime.csv", encoding="shift-jis")
sizes = data_frame["33業種区分"].value_counts() # まとまったカテゴリーの要素
labels = data_frame["33業種区分"].value_counts().index # カテゴリーネーム
get_pie_ratio(labels)