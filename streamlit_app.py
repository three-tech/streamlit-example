import time

import numpy as np
import pandas as pd
import streamlit as st

x = st.slider(min_value=1, max_value=1000, key='Enter a number', value=50, step=1, format='%d',
              label='Enter a number')  # 👈 this is a widget
st.write(x, 'squared is', x * x)
st.markdown("""---""")

st.text_input("Your name👈", key="name")

st.markdown("""---""")
if st.checkbox('Show dataframe'):
    chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=['a', 'b', 'c'])
    chart_data

df = pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
})
st.markdown("""---""")
option = st.selectbox(
    'Which number do you like best?',
    df['first column'])

'You selected: ', option

st.markdown("""---""")
add_selectbox = st.sidebar.selectbox(
    'How would you like to be contacted?',
    ('Email', 'Home phone', 'Mobile phone')
)

# Add a slider to the sidebar:
add_slider = st.sidebar.slider(
    'Select a range of values',
    0.0, 100.0, (25.0, 75.0)
)

'Starting a long computation...'

# Add a placeholder
latest_iteration = st.empty()
bar = st.progress(0)

for i in range(100):
    # Update the progress bar with each iteration.
    latest_iteration.text(f'Iteration {i + 1}')
    bar.progress(i + 1)
    time.sleep(0.1)

'...and now we\'re done!'
st.markdown("""---""")
