import streamlit as st

st.header('st.checkbox')

st.subheader('Example 1')

st.write ('What would you like to order?')

icecream = st.checkbox('Ice cream')
coffee = st.checkbox('Coffee')
cola = st.checkbox('Cola')

if icecream:
    st.write("Great! Here's some more 🍦")

if coffee: 
    st.write("Okay, here's some coffee ☕")

if cola:
    st.write("Here you go 🥤")

st.subheader('Example 2')

check = st.checkbox('Click Here!')

st.write ('State:', check)

if check:
    st.write(":smile:"*3)

st.subheader('Example 3')

check_2 = st.checkbox('Uncheck to remove cake', value=True)

if check_2:
    st.write(":cake:"*3)    