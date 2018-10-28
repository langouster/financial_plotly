# financial_plotly

## 效果演示
![image](https://raw.githubusercontent.com/langouster/financial_plotly/master/example/screenshot/example.png)

![image](https://raw.githubusercontent.com/langouster/financial_plotly/master/example/screenshot/zoom.png)

## 说明

此项目主要用于画财经图，如量化分析数据，它是对 https://plot.ly/python/ 的二次封装，用于把python的dataframe直接画图，而不再需要操作画图相关的api。

除了不需要复杂的api就可以显示图外，还可以自动重新采样显示有大量数据的dataframe，当对图的某部分放大时会重新加载这个部分的数据以显示更多细节，而不是简单的图形放大。

图标的x轴使用dataframe的index, 我一般用datetime时间。

* 只测试了python 2.7版本，其他版本未测试

## 使用方法

使用前需要安装plot的依赖库:

```
pip install dash plotly dash_core_components dash_html_components
```

工程分为两个文件：plot.py和plot_inc.py

* plot_inc.py文件是需要包含到您的工程里的，里面只有一个函数showData，用于把dataframe保存到文件中。
然后plot.py会检测到数据有更新，plot.py重新加载数据，浏览器刷新就可以看到最新的数据

* plot.py文件用于画图，不需要修改, 直接运行，它有一个参数指明dataframe的存放目录，和showData的path参数指向一个目录。
启动成功后它将启动一个webserver，然后用浏览器打开 http://127.0.0.1:8050/ 就可以看到图形了，参考run.bat