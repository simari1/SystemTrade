def optim_func(series):
    if series["# Trades"] < 5:
        return -1
    
    return series["Equity Final [$]"] / series["Exposure Time [%]"]