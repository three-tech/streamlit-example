import pandas
import plotly.graph_objs as go
import talib
from plotly.subplots import make_subplots


def plot_mutuality_sub(df):
    # 写入你自己的文件
    df['RSI'] = talib.RSI(df['close'], timeperiod=28)
    a = pandas.DataFrame()
    b = pandas.DataFrame()
    df.fillna(0)
    for i in range(56):
        a[f's{i}_high'] = df['high'].shift(i)
        b[f's{i}_low'] = df['low'].shift(i)
    a.fillna(0)
    b.fillna(0)

    # 唐奇安上阻力线 - 由过去N天的当日最高价的最大值形成。
    df['t_up'] = a.max(axis=1)
    # #
    # 唐奇安下支撑线 - 由过去N天的当日最低价的最小值形成。
    #
    df['t_low'] = b.min(axis=1)
    # 中心线 - （上线 + 下线）/ 2
    df['t_middle'] = (df['t_up'] + df['t_low']) / 2

    fig = make_subplots(rows=1, cols=1, shared_xaxes=True, row_heights=[9], subplot_titles="日K线", )
    fig = go.FigureWidget(fig)
    fig.add_trace(go.Candlestick(x=df.date, open=df.open, high=df.high, low=df.low, close=df.close,
                                 increasing_line_color='green', decreasing_line_color='red', name='日K'), row=1,
                  col=1)

    # # 加唐奇安通道
    # fig.add_trace(go.Scatter(x=df.date, y=df.t_up, marker_color='yellow', name='T', line=dict(width=1)), row=1, col=1)
    # fig.add_trace(go.Scatter(x=df.date, y=df.t_low, marker_color='blue', name='M', line=dict(width=1), fill='tonextx',
    #                          fillcolor='rgba(0,191,255,0.1)'), row=1, col=1)
    # fig.add_trace(go.Scatter(x=df.date, y=df.t_middle, marker_color='blue', name='L', line=dict(width=1)),
    #               row=1, col=1)
    # fig.add_trace(go.Scatter(x=df.date, y=df.RSI, marker_color='white', name='R', line=dict(width=1)), row=2, col=1)

    fig.update_layout(xaxis_rangeslider_visible=True, xaxis_rangeslider_thickness=0.4)
    fig.update_layout(height=800)
    fig.update_xaxes(tickformat='%Y-%m-%d')
    fig.update_layout(hovermode="x unified")
    fig["layout"]["template"] = "plotly_dark"

    return fig
