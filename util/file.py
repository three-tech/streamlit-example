import pandas as pd
import streamlit as st
from pandas import DataFrame


@st.cache_resource(show_spinner=False)
def read_data(file_name: str) -> DataFrame:
    """
    读取数据
    :return:
    """
    data = pd.read_csv(file_name, dtype={'代码': str})
    data = remove_columns(data, ['Unnamed: 0', '序号'])

    if 'date' in data.columns:
        data['date'] = pd.to_datetime(data['date'])
    return data


def remove_columns(data: DataFrame, columns: list) -> DataFrame:
    """
    删除列
    :param data:
    :param columns:
    :return:
    """
    for column in columns:
        if column in data.columns:
            data = data.drop(columns=[column], inplace=False)
    return data
