import pandas as pd

class SuperStrategy:
    """ProdのStrategyに共通で継承されるべきスーパークラス
    """
    def setdata(self, sdata):
        """初期処理
        dataに売り買い用のサイン列を追加する
        """
        print("Hello from Super")

        df = pd.DataFrame(
            data={'Open': sdata.Open, 
                'High': sdata.High,
                'Low': sdata.Low,
                'Close':  sdata.Close,
                }
        )
        print("Hello from Super2")
        print(df.head())
        print(df.count())
        print("Hello from Super3")