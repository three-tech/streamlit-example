import pandas as pd
import streamlit as st
from pandas import DataFrame

import service.data.dataKzz as dataKzz
from service.plot.multi_sub import plot_mutuality_sub
from service.plot.plot_line import plot_close_volume

st.title("可转债分析")
with st.sidebar:
    st.header("策略配置")
    st.button("下载全量数据", on_click=dataKzz.download_data)

    st.markdown("### 均线策略参数配置")
    c1, c2, c3 = st.columns([1, 1, 1])
    with c1:
        fast = st.number_input("快线周期", value=5, key="ma_period")
    with c2:
        slow = st.number_input("慢线周期", value=10, key="ma_period2")

st.header("可转债数据一览表")
with st.spinner('读取数据中...'):
    bond_zh_cov = dataKzz.read_data('bond_zh_cov')
    st.dataframe(bond_zh_cov)

st.markdown('---')
with st.expander("下载数据"):
    st.header("下载数据")
    c1, c2 = st.columns([1, 4])
    with c1:
        date = st.date_input("选择数据下载日期", format="YYYY-MM-DD")
    with c2:
        columns = st.multiselect("选择下载属性", dataKzz.default_his_columns,
                                 default=['date', 'symbol', 'name', 'open', 'high', 'low', 'close', 'volume'],
                                 placeholder="")
    if st.button("下载"):
        with st.spinner('下载数据中...'):
            st.dataframe(dataKzz.download_data_by_day(f'{date}', columns), use_container_width=True)
            st.success("数据下载成功")

st.markdown('---')
st.header("分析数据")
symbols = dataKzz.available_symbols()
available_symbols = bond_zh_cov[bond_zh_cov["symbol"].isin(symbols)]

names = st.multiselect("选择要分析的可转债", available_symbols["债券简称"], placeholder="可以多选")
tmp = available_symbols[available_symbols["债券简称"].isin(names)]
st.dataframe(tmp)

close = DataFrame(columns=["date"])
for name in names:
    row = available_symbols[available_symbols["债券简称"] == name]
    symbol = row["symbol"].values[0]
    # 获取日频交易
    with st.spinner('下载数据中...'):
        bond_zh_hs_cov_daily_df = dataKzz.read_data(f'his/{symbol}')
        tmp = bond_zh_hs_cov_daily_df[['date', 'close']]
        tmp[name] = tmp["close"]
        tmp = tmp.drop(columns=["close"])
        close = pd.merge(left=close, right=tmp, left_on='date', right_on='date',
                         how='outer')

        with st.expander(f"{name}日频交易数据"):
            st.dataframe(bond_zh_hs_cov_daily_df)
        st.plotly_chart(plot_mutuality_sub(bond_zh_hs_cov_daily_df))
        # st.plotly_chart(plot_cand_volume(bond_zh_hs_cov_daily_df), use_container_width=True)
# 画出收盘趋势
if len(names) > 0:
    st.plotly_chart(plot_close_volume(close))
# row = bond_zh_cov[bond_zh_cov["债券代码"] == name]
# symbol = row["symbol"].values[0]
# # 获取日频交易
# with st.spinner('下载数据中...'):
#     bond_zh_hs_cov_daily_df = ak.bond_zh_hs_cov_daily(symbol)
#     st.markdown(f"### {name}日频交易数据")
#     st.dataframe(bond_zh_hs_cov_daily_df)
#     st.line_chart(bond_zh_hs_cov_daily_df, x='date', x_label='日期', y_label='高开低收', use_container_width=True)
