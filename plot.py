# coding=utf8
import json
from textwrap import dedent as d

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly
import pickle
import thread
import os, time, sys

g_dfList = []

MINTS = pd.to_datetime('1970-1-1')
MAXTS = pd.to_datetime('2200-1-1')

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(
        id='basic-interactions',
        style={"height": "100vh"}
    ),

])


@app.callback(
    dash.dependencies.Output('basic-interactions', 'figure'),
    [Input('basic-interactions', 'relayoutData')],
    state=[dash.dependencies.State('basic-interactions', 'figure')]
)
def display_selected_data(relayoutData, state):
    hiddenList = []
    if state is not None:
        lines = state.get('data', {})
        for line in lines:
            if line.get('visible', 'legendonly') == 'legendonly':
                hiddenList.append(line['name'])

    if relayoutData is None:
        return showDF(MINTS, MAXTS, hiddenList)
    elif relayoutData.get('autosize', False):
        return showDF(MINTS, MAXTS, hiddenList)
    else:
        start = relayoutData.get('xaxis.range[0]', MINTS)
        if type(start) == unicode:
            start = pd.to_datetime(start)
        end = relayoutData.get('xaxis.range[1]', MAXTS)
        if type(end) == unicode:
            end = pd.to_datetime(end)
        return showDF(start, end, hiddenList)


def showDF(start, end, hiddenList):
    global g_dfList
    fig = plotly.tools.make_subplots(rows=2, cols=1, specs=[[{}], [{}]],
                                     shared_xaxes=True, shared_yaxes=True, row_width=[1, 2],
                                     vertical_spacing=0.001)

    for dfInfo in g_dfList:
        index = dfInfo.get('plotIndex', 1)
        mode = dfInfo.get('mode', 'lines')
        marker = dfInfo.get('marker', {})
        text = dfInfo.get('text', None)

        tmp = dfInfo['df']
        if len(tmp) == 0:
            continue
        tmp = limitDFNum(tmp[(tmp.index > start) & (tmp.index < end)])
        for colName in dfInfo['df'].columns:
            visible = True
            if colName in hiddenList:
                visible = 'legendonly'
            trace = go.Scatter(
                x=tmp.index,
                name=colName,
                y=tmp[colName],
                visible=visible,
                mode=mode,
                text=text,
                marker=marker,
            )
            fig.append_trace(trace, index, 1)

    # height=800, width=1080,
    fig['layout'].update(xaxis=dict(
        tickformat="%y-%m-%d %H:%M:%S",
        # rangeselector=dict(),
        # rangeslider=dict(), #选择区域活动条
        # type='date'
    ))
    return fig


# 样本量太大的时候抽样显示就可以了
def limitDFNum(df):
    if len(df) < 3000:  # 防止是0长度
        return df

    cols = {}
    for c in df.columns:
        cols[c] = "avg"

    frac = 3000.0 / len(df)  # 抽样百分比  一个图画3000个数据点 防止数据量太大时画图太慢
    if frac > 0.9:
        return df
    return df.sample(frac=frac).copy().sort_index()


def draw():

    app.run_server(debug=False)
    pass


def getDrawFileList():
    ret = []
    path = ''
    if len(sys.argv) == 2:
        path = sys.argv[1]
    else:
        path = path + './draw_data/'
    for f in os.listdir(path):
        subpath = path + '/' + f
        if not os.path.isfile(subpath):
            ret.append(subpath)

    return ret


def loadOneData(path):
    try:
        config = open(path + '/config.json').read()
        config = json.loads(config)
        if config is None:
            return None
        if not config.get('enable'):
            return None
        df = pickle.load(open(path + '/' + config['fileName'], 'rb'))
        config.pop('fileName')
        if 'text' in df.columns:
            config.update({
                'text': df['text'].values
            })
            del df['text']
        config.update({
            'df': df
        })
        return config
    except:
        return None


def getDirLastModifyTime():
    lastTS = 0
    drawFiles = getDrawFileList()
    for filePath in drawFiles:
        filePath = filePath + '/config.json'
        t = os.path.getmtime(filePath)
        if t > lastTS:
            lastTS = t
    return lastTS


if __name__ == '__main__':
    lastTS = 0

    thread.start_new_thread(draw, ())
    while True:
        ts = getDirLastModifyTime()
        if ts == lastTS:
            time.sleep(1)
            continue
        lastTS = ts
        tmp = []
        time.sleep(1)  # 有可能数据正在更新，所以等一下再读
        drawFiles = getDrawFileList()
        for filePath in drawFiles:
            info = loadOneData(filePath)
            if info is not None:
                tmp.append(info)
        g_dfList = tmp
        print(time.strftime("%Y-%m-%d %H:%M:%S"))
