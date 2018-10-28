# coding=utf8
import json
import pandas as pd
import os, time, sys

sys.path.append('../')
import plot_inc


def readCSV(filePath):
    df = pd.read_csv(filePath)
    df.index = pd.to_datetime(df.index)
    return df


priceDF = readCSV('./ticker.csv')

plot_inc.showData(priceDF[["buy1Price", "sell1Price"]], './plot/', 'price', {
    "enable": True,
    "plotIndex": 1
})

priceDF['text'] = 'label:xxxx' #当鼠标移到线条上时显示的注解
plot_inc.showData(priceDF[["last", "text"]], './plot/', 'last_price', {
    "enable": True,
    "plotIndex": 2
})

tradeDF = readCSV('./trade.csv')

plot_inc.showData(tradeDF[["openLong", "text"]], './plot/', 'trade_openLong', {
    "enable": True,
    "plotIndex": 1,
    "mode": "markers",
    "marker": {
        "symbol": "triangle-up",
        "size": 20
    }
})

plot_inc.showData(tradeDF[["closeLong", "text"]], './plot/', 'trade_closeLong', {
    "enable": True,
    "plotIndex": 1,
    "mode": "markers",
    "marker": {
        "symbol": "triangle-down",
        "size": 20
    }
})

print("ok")
