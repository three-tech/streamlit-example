import datetime

import numpy as np
import pandas as pd
import plotly.express as px
import talib as ta


# calculate moving average crossover
def moving_average_cross(data, fast_avg, slow_avg):
    ta.MACD(data, fast_avg, slow_avg)
    short_rolling = data.rolling(window=fast_avg).mean()
    long_rolling = data.rolling(window=slow_avg).mean()
    signals = np.where(short_rolling > long_rolling, 1, -1)
    return np.roll(signals, 1)


def draw_plot(data, fast_avg, slow_avg):
    plot_date = data.iloc[0]['date']
    plot_date = datetime.datetime.strptime(plot_date, '%Y-%m-%d').date()
    ticker = data.iloc[0]['name']

    data = data[['date', 'close']]
    data['date'] = pd.to_datetime(data['date'])
    # 设置'date'列为索引
    data.set_index('date', inplace=True)
    short_rolling = data['close'].rolling(window=fast_avg).mean()
    long_rolling = data['close'].rolling(window=slow_avg).mean()
    signals = np.roll(np.where(short_rolling > long_rolling, 1, -1), -1)
    portfolio = data['close'] * signals
    portfolio_return = portfolio.loc[(portfolio > 0) & (portfolio.index.date >= plot_date)].cumprod().dropna()
    df = pd.DataFrame(data.loc[data.index.date >= plot_date].cumprod())
    df.columns = [ticker]
    df['Strategy'] = portfolio_return
    fig = px.line(data, labels={'Date': '', 'value': '', 'variable': ''}, title='快慢线策略')
    fig.update_layout(hovermode="x unified")
    fig.update_traces(hovertemplate="%{y}")
    # fig.layout.yaxis.tickformat = '.2%'
    return fig
