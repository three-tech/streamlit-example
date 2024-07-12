import os

import akshare as ak
import pandas as pd
import streamlit as st
from pandas import DataFrame

from util import file

data_path_kzz = 'data/kzz/'
last_download_date = None
default_his_columns = ['date', 'code', 'symbol', 'name', 'open', 'high', 'low', 'close', 'volume', '收盘价', '纯债价值',
                       '转股价值', '纯债溢价率', '转股溢价率']


@st.cache_data(ttl='12h', show_spinner=False)
def bond_zh_cov() -> DataFrame:
    """
    东方财富网-数据中心-新股数据-可转债数据一览表

    限量: 单次返回当前交易时刻的所有可转债数据
    :return:
    """
    result = ak.bond_zh_cov()
    result["symbol"] = result["债券代码"].apply(lambda x: 'sh' + x if x.startswith('11') else 'sz' + x)
    result.to_csv(data_path_kzz + 'bond_zh_cov.csv')
    return __format__(result)


def bond_zh_hs_cov_spot() -> DataFrame:
    """
    新浪财经-债券-沪深可转债的实时行情数据; 大量抓取容易封IP
    https://vip.stock.finance.sina.com.cn/mkt/#hskzz_z
    :return: 所有沪深可转债在当前时刻的实时行情数据
    """
    result = ak.bond_zh_hs_cov_spot()
    result.to_csv(data_path_kzz + 'bond_zh_hs_cov_spot.csv')
    print('bond_zh_hs_cov_spot下载完成')
    return __format__(result)


@st.cache_data(ttl='12h', show_spinner=False)
def bond_zh_cov_value_analysis(code: str) -> DataFrame:
    """
    目标地址: https://data.eastmoney.com/kzz/detail/113527.html

    描述: 东方财富网-行情中心-新股数据-可转债数据-可转债价值分析
    :return:
    """
    try:
        return ak.bond_zh_cov_value_analysis(code)
    except Exception as e:
        print(f'{code}价值分析下载失败', e)
        return pd.DataFrame(columns=['日期', '收盘价', '纯债价值', '转股价值', '纯债溢价率',
                                     '转股溢价率'])


@st.cache_resource
def bond_zh_hs_cov_daily(symbol: str) -> DataFrame:
    """
    目标地址: https://biz.finance.sina.com.cn/suggest/lookup_n.php?q=sh110048

    描述: 新浪财经-历史行情数据，日频率更新, 新上的标的需要次日更新数据

    限量: 单次返回具体某个沪深可转债的所有历史行情数据
    :param symbol:
    :return:
    """
    try:
        return ak.bond_zh_hs_cov_daily(symbol)
    except Exception as e:
        print(f'{symbol}历史下载失败', e)
        return pd.DataFrame()


@st.experimental_dialog("数据下载中...")
def download_data_with_dialog():
    """
    下载数据
    :return:
    """

    progress_bar = st.progress(0)
    data = bond_zh_hs_cov_spot()
    row_count = data.shape[0] - 1

    for i, (index, row) in enumerate(data.iterrows(), 1):
        progress = i / row_count
        progress = 1 if progress >= 1 else progress

        code = row['code']
        symbol = row['symbol']
        name = row['name']
        text = f'开始下载{code}-{name}...'
        print(text)

        progress_bar.progress(progress, text=f'    {progress * 100:.2f}% {text}')
        # 分析数据
        analysis = bond_zh_cov_value_analysis(code)
        # 历史数据
        history = bond_zh_hs_cov_daily(symbol)
        if history.empty:
            print(f'{text}没有历史数据')
            continue

        merged = pd.merge(left=history, right=analysis, left_on='date', right_on='日期', how='left')
        merged.to_csv(data_path_kzz + f'his/{symbol}.csv')
        tmp = merged[[
            'date', 'open', 'high', 'low', 'close', 'volume', '收盘价', '纯债价值', '转股价值', '纯债溢价率',
            '转股溢价率']]
        tmp.insert(1, 'code', code)
        tmp.insert(2, 'symbol', symbol)
        tmp.insert(3, 'name', name)
        tmp.to_csv(data_path_kzz + f'his/{symbol}.csv')
    # st.cache_resource.clear()
    # st.cache_data.clear()
    progress_bar.empty()
    progress_bar.success('数据下载完成')


def download_data():
    """
    下载数据
    :return:
    """
    data = bond_zh_hs_cov_spot()
    for index, row in data.iterrows():
        code = row['code']
        symbol = row['symbol']
        name = row['name']
        text = f'{code}-{name}'
        print(f'开始下载{text}')

        # 分析数据
        analysis = bond_zh_cov_value_analysis(code)
        # 历史数据
        history = bond_zh_hs_cov_daily(symbol)
        if history.empty:
            print(f'{text}没有历史数据')
            continue

        merged = pd.merge(left=history, right=analysis, left_on='date', right_on='日期', how='left')
        merged.to_csv(data_path_kzz + f'his/{symbol}.csv')
        tmp = merged[[
            'date', 'open', 'high', 'low', 'close', 'volume', '收盘价', '纯债价值', '转股价值', '纯债溢价率',
            '转股溢价率']]
        tmp.insert(1, 'code', code)
        tmp.insert(2, 'symbol', symbol)
        tmp.insert(3, 'name', name)
        tmp.to_csv(data_path_kzz + f'his/{symbol}.csv')
    st.cache_resource.clear()
    st.cache_data.clear()
    st.toast('全量数据下载完成')


@st.cache_resource
def available_symbols():
    """
    获取可用数据
    :return:
    """
    return [name[:-4] for name in os.listdir(data_path_kzz + 'his') if name.endswith('.csv')]


def download_data_by_day(date: str, columns=None) -> DataFrame:
    if columns is None:
        columns = default_his_columns
    result = DataFrame(columns=columns)
    for symbol in available_symbols():
        file = data_path_kzz + f'his/{symbol}.csv'
        tmp = pd.read_csv(file)[columns]
        tmp = tmp[tmp['date'] == date]
        result = pd.concat([result, tmp], ignore_index=True)
    return __format__(result)


def read_data_kzz(name: str) -> DataFrame:
    """
    读取数据
    :return:
    """
    return file.read_data(build_data_path(name))


def build_data_path(name: str) -> str:
    return data_path_kzz + f'{name}.csv'


def __format__(data: DataFrame) -> DataFrame:
    """
    格式化数据
    :param data:
    :return:
    """
    # data = data.iloc[:, 1:]
    if 'date' in data.columns:
        data['date'] = pd.to_datetime(data['date'])
        data.set_index('date', inplace=True)
    return data
