import streamlit as st

# 用户名和密码的默认值
DEFAULT_USERNAME = "xx"
DEFAULT_PASSWORD = "xx"

# 检查会话状态中是否有登录状态，如果没有，初始化为 False
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False


# st.title("登录")
c = st.columns([4, 3, 4])
with c[1]:
    st.header("登录")
    with st.form("login_form"):
        username = st.text_input("用户名", value="")
        password = st.text_input("密码", value="", type="password")
        submit = st.form_submit_button("登录", use_container_width=False)
        if submit:
            if username == DEFAULT_USERNAME and password == DEFAULT_PASSWORD:
                st.success("登录成功！")
                # 更新会话状态为已登录
                st.session_state.logged_in = True
                st.experimental_rerun()  # 重新运行脚本以显示主页面
            else:
                st.error("用户名或密码错误，请重新输入。")
