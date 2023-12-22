import streamlit as st
import streamlit_authenticator as stauth

# 如下代码数据，可以来自数据库
names = ['肖永威', '管理员']
usernames = ['admin', 'test']
passwords = ['S0451', 'ad4516']
credentials = {
    "usernames": {
        usernames[0]: {
            "name": names[0],
            "password": passwords[0]
        },
        usernames[1]: {
            "name": names[1],
            "password": passwords[1]
        }
    }
}

hashed_passwords = stauth.Hasher(passwords).generate()
print(hashed_passwords)

# credentials: dict, cookie_name: str, key: str
authenticator = stauth.Authenticate(credentials, 'login', 'test')

name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:
    with st.container():
        cols1, cols2 = st.columns(2)
        cols1.write('欢迎 *%s*' % name)
        with cols2.container():
            authenticator.logout('Logout', 'main')

    main_page = st.sidebar.selectbox('Main Page', ['Page 1', 'Page 2', 'Page 3', 'Page 4'])
elif not authentication_status:
    st.error('Username/password is incorrect')
elif authentication_status is None:
    st.warning('Please enter your username and password')
