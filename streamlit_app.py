import streamlit as st

kzzPage = st.Page("pages/1 kezhuanzai.py", title="可转债", icon=":material/add_circle:")

st.set_page_config(page_title="量化分析", page_icon="📈", layout="wide", initial_sidebar_state="auto")
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


def login():
    if st.button("Log in"):
        st.session_state.logged_in = True
        st.rerun()


def logout():
    if st.button("Log out"):
        st.session_state.logged_in = False
        st.rerun()


login_page = st.Page(login, title="Log in", icon=":material/login:")
logout_page = st.Page(logout, title="Log out", icon=":material/logout:")

if st.session_state.logged_in:
    pg = st.navigation(
        {
            "Account": [logout_page],
            "Tools": [kzzPage],
        }
    )
else:
    pg = st.navigation([login_page])

pg.run()
