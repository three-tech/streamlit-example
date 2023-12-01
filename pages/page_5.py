import time
from dataclasses import make_dataclass

import pandas as pd
import streamlit as st

Point = make_dataclass("Point", [("x", int), ("y", int)])
df = pd.DataFrame(data={'a': [1, 2], 'b': [3, 4]})
# st.balloons()
# st.snow()

data = b'Hello, world!'
key = 'key'
value = 'value'
objects = [1, 2, 3]
my_dataframe = pd.DataFrame(data=['a', 'b', 'c'], index=objects)

st.markdown('# Display text')
st.text('Fixed width text')
st.markdown('_Markdown_')  # see #*
st.caption('Balloons. Hundreds of them...')
st.latex(r''' e^{i\pi} + 1 = 0 ''')
st.write('Most objects')  # df, err, func, keras!
st.write(['st', 'is <', 3])  # see *
st.title('My title')
st.header('My header')
st.subheader('My sub')
st.code('for i in range(8): foo()')

# * optional kwarg unsafe_allow_html = True
st.markdown('-----')
st.markdown('# Display interactive widgets')
st.button('Hit me')
# st.data_editor('Edit data', data)
st.checkbox('Check me out')
st.radio('Pick one:', ['nose', 'ear'])
st.selectbox('Select', [1, 2, 3])
st.multiselect('Multiselect', [1, 2, 3])
st.slider('Slide me', min_value=0, max_value=10)
st.select_slider('Slide to select', options=[1, '2'])
st.text_input('Enter some text')
st.number_input('Enter a number')
st.text_area('Area for textual entry')
st.date_input('Date input')
st.time_input('Time entry')
st.file_uploader('File uploader')
st.download_button('On the dl', data)
st.camera_input("一二三,茄子!")
st.color_picker('Pick a color')

st.markdown('-----')
st.markdown('# Display data')
st.dataframe(df)
st.table(df.iloc[0:10])
st.json({'foo': 'bar', 'fu': 'ba'})
st.metric(label="Temp", value="273 K", delta="1.2 K")

st.markdown('-----')
st.markdown('# Columns')
col1, col2 = st.columns(2)
col1.write('Column 1')
col2.write('Column 2')

# Three columns with different widths
col1, col2, col3 = st.columns([3, 1, 1])
# col1 is wider

# Using 'with' notation:
with col1:
    st.write('This is column 1')

st.markdown('-----')
st.markdown('# Tabs')
# Insert containers separated into tabs:
tab1, tab2 = st.tabs(["Tab 1", "Tab2"])
tab1.write("this is tab 1")
tab2.write("this is tab 2")

# You can also use "with" notation:
with tab1:
    st.radio('Select one:', [1, 2])

st.markdown('-----')
st.markdown('# Control flow')
# Stop execution immediately:
# st.stop()
# Rerun script immediately:
# st.experimental_rerun()

# Group multiple widgets:
with st.form(key='my_form'):
    username = st.text_input('Username')
    password = st.text_input('Password')
    st.form_submit_button('Login')

st.markdown('-----')
st.markdown('# Placeholders, help, and options')
# Replace any single element.
element = st.empty()
element.line_chart(my_dataframe)
element.text_input('my_dataframe')  # Replaces previous.

# Insert out of order.
elements = st.container()
elements.line_chart(df)
st.write("Hello")
elements.text_input('text_input')  # Appears above "Hello".

st.help(pd.DataFrame)
# st.set_option(key, value)
# st.get_option(key)
# st.set_page_config(layout='wide')
st.experimental_show(objects)
st.experimental_get_query_params()
# st.experimental_set_query_params(**params)

st.markdown('-----')
st.markdown('# Display code')
st.echo()
with st.echo():
    st.write('Code will be executed and printed')

st.markdown('-----')
st.markdown('# Display progress and status')
# Show a spinner during a process
with st.spinner(text='In progress'):
    time.sleep(3)
    st.success('Done')

# Show and update progress bar
bar = st.progress(50)
time.sleep(3)
bar.progress(100)

st.balloons()
st.snow()
# st.toast('Mr Stay-Puft')
st.error('Error message')
st.warning('Warning message')
st.info('Info message')
st.success('Success message')
# st.exception(e)
