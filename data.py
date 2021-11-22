import pandas as pd

def read_danmu(file):
    df = pd.read_csv(file, encoding='utf-8', error_bad_lines=False, sep=',', header=None)
    progress = list(df.loc[:][1])
    danmu = list(df.loc[:][6])
    return progress, danmu