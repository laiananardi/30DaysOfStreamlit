import streamlit as st

st.title('st.query_params')

with st.expander('About this app'):
  st.write("`st.query_params` allows the retrieval of query parameters directly from the URL of the user's browser.")

# 1. Instructions
st.header('1. Instructions')
st.markdown('''
In the above URL bar of your internet browser, append the following:
`?firstname=Jack&surname=Beanstalk`
after the base URL `http://share.streamlit.io/dataprofessor/st.query_params/`
such that it becomes 
`http://share.streamlit.io/dataprofessor/st.query_params/?firstname=Jack&surname=Beanstalk`
''')

# 3. Retrieving and displaying information from the URL
st.header('2. Retrieving and displaying information from the URL')

firstname = st.query_params["firstname"]
surname = st.query_params["surname"]

st.write(f'Hello **{firstname} {surname}**, how are you?')