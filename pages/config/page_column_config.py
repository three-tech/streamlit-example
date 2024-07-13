import streamlit as st

column_configuration = {
    "转股溢价率": st.column_config.TextColumn(
        help="转股溢价率",
        width="small",

    ),
    "close": st.column_config.LineChartColumn(
        "价格走势 (日K)",
        help="所有日期的价格走势图",
        width="large",
        # y_min=0,
        # y_max=1,
    ),
}
