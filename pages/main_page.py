import streamlit as st

st.markdown("# Main page 🎈")
st.sidebar.markdown("# Main page 🎈")

# 创建一个标题元素
st.title("My Streamlit App")

# 创建一个容器元素
with st.container():
    # 在容器中创建一个文本框元素
    name_input = st.text_input("Enter your name:")

    # 在容器中创建一个按钮元素
    submit_button = st.button("Submit")

# 创建一个文本元素，并显示在 Streamlit 应用程序中
if submit_button:
    st.write(f"Hello, {name_input}!")
