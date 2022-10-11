def optim_func(series):
    if series["# Trades"] < 7:
        return -1
    if series["Max. Drawdown [%]"] > 20:
        return -1
    if series["Win Rate [%]"] < 60:
        return -1
    if series["Worst Trade [%]"] < -20:
        return -1
    if series["Profit Factor"] < 1:
        return -1
    if series["Sharpe Ratio"] < 1.5:
        return -1
    if series["SQN"] < 2:
        return -1
    return series["Equity Final [$]"]