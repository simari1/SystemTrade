import pandas as pd
import pandas_datareader.data as web
import datetime
import os
import time

def extract_stock_data(df_data, name):
    start = datetime.date(2015,1,1)
    end = datetime.date.today()

    directory = f"./data/stocks_price_data/{name}"
    if not os.path.exists(directory):
        os.makedirs(directory)

    for index, row in df_data.iterrows():
        code = row["コード"]
        try:
            df = web.DataReader(f'{code}.T', 'yahoo', start, end)
        except:
            import traceback
            traceback.print_exc()
        df.to_csv(f"{directory}/_stock_price_data_{code}.csv")
        time.sleep(1)

df_data_j = pd.read_excel("./data/data_j.xls")

df_data_prime = df_data_j[df_data_j["市場・商品区分"] == "プライム（内国株式）"]
df_data_prime.to_csv("./data/prime.csv", index=None, encoding="cp932")
print("prime: " + str(len(df_data_prime)))

df_data_standard = df_data_j[df_data_j["市場・商品区分"] == "スタンダード（内国株式）"]
df_data_standard.to_csv("./data/standard.csv", index=None, encoding="cp932")
print("standard: " + str(len(df_data_standard)))

df_data_etf = df_data_j[df_data_j["市場・商品区分"] == "ETF・ETN"]
df_data_etf.to_csv("./data/etfetn.csv", index=None, encoding="cp932")
print("etfetn: " + str(len(df_data_etf)))

extract_stock_data(df_data_prime, "prime")
extract_stock_data(df_data_standard, "standard")
extract_stock_data(df_data_etf, "etf")
