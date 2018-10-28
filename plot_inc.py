# coding=utf8

import time
import os
import json
import pickle
import pandas as pd

# df: datafram数据
# path: dataframe存放目录,不是文件是目录
# fileName: 存放dataframe的文件名
# info:指示画图的方法：默认是折线图，支持的参数有:enable,plotIndex,mode,marker

'''
例子1：
df有last和text两列，last是float,text是字符串类型，是对每个点的描述

plot_inc.showData(priceDF[["last", "text"]], './plot/', 'last_price', {
    "enable": True, # 是否显示
    "plotIndex": 1 # 默认有上下两个图，1代表上面的图，2是下面的图
})


例子2：
mode: line或markers 或 lines+markers 代表折线图还是点图，点图点的形状用symbol指明, 具体参考https://plot.ly/python/reference/#scatter中的mode
marker: 只有当mode包含markers时才有效， 代表的是点的格式 具体参考https://plot.ly/python/reference/#scatter中的market


plot_inc.showData(tradeDF[["openLong", "text"]], './plot/', 'trade_openLong', {
    "enable": True,
    "plotIndex": 1,
    "mode": "markers",
    "marker": {
        "symbol": "triangle-up", #向上箭头
        "size": 20
    }
})
'''

def showData(df, path, fileName, info):
    path = path + fileName
    try:
        os.makedirs(path)
    except:
        pass
    confPath = path + "\\config.json"
    info['fileName'] = fileName + ".dat"
    open(confPath, 'w').write(json.dumps(info))
    datPath = path + "\\" + fileName + ".dat"
    pickle.dump(df, open(datPath, 'wb'))
