import streamlit as st

import pages.style as sd

welcome = st.Page("pages/0 welcome.py", title="声明", icon="🍸")
loginPage = st.Page("pages/login.py", title="登录", icon=":material/login:")
kzzPage = st.Page("pages/1 kezhuanzai.py", title="可转债", icon="🔥")
stockPage = st.Page("pages/2 stock.py", title="股票", icon="⬆")

st.set_page_config(page_title="量化分析", page_icon="📈", layout="wide", initial_sidebar_state="auto", )
st.markdown(sd.footer_style, unsafe_allow_html=True)
st.markdown(sd.hide_streamlit_style, unsafe_allow_html=True)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


def logout():
    if st.button("Log out"):
        st.session_state.logged_in = False
        st.rerun()


logout_page = st.Page(logout, title="登出", icon=":material/logout:")

if st.session_state.logged_in:
    pg = st.navigation(
        {
            "声明": [welcome],
            "工具": [kzzPage, stockPage],
            "账户": [logout_page],
        }
    )
else:
    pg = st.navigation([loginPage])

pg.run()
