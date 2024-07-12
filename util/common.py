import datetime

import streamlit as st

last_download_time = {}


@st.experimental_dialog("全量数据下载提示")
def download_all_data_dialog(data_type: str):
    last_time = last_download_time[data_type]
    if last_time is None:
        st.write("第一次下载，请耐心等待")
        last_download_time[data_type] = datetime.datetime.now()
