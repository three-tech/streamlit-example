import streamlit as st

from service.data import dataStock

st.title("股票分析")
with st.sidebar:
    st.header("策略配置")
    st.button("下载全量数据", on_click=dataStock.download_data)

st.subheader("**股票**实时可交易数据数据一览表")
with st.spinner('读取数据中...'):
    bond_zh_cov = dataStock.read_data_kzz('stock_zh_a_spot')
    st.dataframe(bond_zh_cov)

st.markdown('---')
