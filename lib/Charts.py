import matplotlib.pyplot as plt

def get_pie_ratio(company_labels, sizes, chart_title):
    plt.figure(figsize=(10, 10)) # グラフ自体のサイズ（幅、高さ）
    plt.rcParams['font.family'] = "MS Gothic"
    print(chart_title)
    plt.title(chart_title)
    plt.pie(
        x=sizes,
        labels=company_labels,
        counterclock=False, # 時計回りに比率が高い順の設定
        startangle=90, # 表示のアングルを調整
        textprops={'color':"w", "fontsize": "20"}
    )
    plt.title('Pie Chart', fontsize=25) # グラフタイトル
    plt.show() # グラフを表示