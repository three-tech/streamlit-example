import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pandas import DataFrame
from plotly.subplots import make_subplots


def plot_close_volume(data: DataFrame):
    df_melted = data.melt(id_vars=['date'],
                          var_name='stock',
                          value_name='收盘价')
    df_melted['日期'] = pd.to_datetime(df_melted['date'])
    fig = px.line(df_melted, x='日期', y='收盘价', color='stock', title='收盘价走势')
    # 设置x轴日期格式
    fig.update_xaxes(tickformat='%Y-%m-%d')
    fig.update_layout(hovermode="x unified")
    fig.update_traces(hovertemplate="%{y}")
    return fig


def plot_cand_volume(data, dt_breaks=None):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                        vertical_spacing=0.03, subplot_titles=('', '成交量'),
                        row_width=[0.2, 0.7])
    fig.add_trace(go.Candlestick(name=data['name'].iloc[0],
                                 x=data['date'],
                                 open=data['open'],
                                 high=data['high'],
                                 low=data['low'],
                                 close=data['close'],
                                 increasing_line_color='#FF0033',
                                 decreasing_line_color='#009966'
                                 ),
                  row=1, col=1
                  )
    fig.add_trace(go.Bar(x=data['date'], y=data['volume'], showlegend=False), row=2, col=1)
    # Do not show OHLC's rangeslider plot
    fig.update(layout_xaxis_rangeslider_visible=True)

    # 去除休市的日期，保持连续
    # fig.update_xaxes(rangebreaks=[dict(values=dt_breaks)])
    return fig
