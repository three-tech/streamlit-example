import akshare as ak
import streamlit as st
from pandas import DataFrame

from util import file

data_path_stock = 'data/stock/'


def stock_zh_a_spot() -> DataFrame:
    """
    东方财富网-沪深京 A 股-实时行情
    :return: 东方财富网-
    """
    stock_zh_a_spot_df = ak.stock_zh_a_spot()
    stock_zh_a_spot_df.to_csv(data_path_stock + 'stock_zh_a_spot.csv', index=False)
    return stock_zh_a_spot_df


def read_data_kzz(name: str) -> DataFrame:
    """
    读取数据
    :return:
    """
    return file.read_data(build_data_path(name))


def build_data_path(name: str) -> str:
    return data_path_stock + f'{name}.csv'


def download_data():
    st.toast('开始下载全量可转债数据...')
    stock_zh_a_spot()
    st.toast('全量数据下载完成')

    st.cache_resource.clear()
    st.cache_data.clear()
