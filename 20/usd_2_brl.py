
import streamlit as st
import pandas as pd
import requests


import requests

# Define base currency and target currency
base_currency = "USD"
target_currency = "BRL"

st.title("Currency Converter")
st.caption("Convert from :blue[USD] to :green[BRL]! :moneybag:")

amount =st.number_input(":dollar: Enter Amount:", min_value=0.01, value=100.00, step=1.00, format="%.2f", key="amount")

# Get the exchange rate

try:
    # Fetch exchange rates
    url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
    response = requests.get(url)
    data = response.json()
    if "rates" in data and target_currency in data["rates"]:
        rate = data["rates"].get(target_currency)
        converted_amount = amount * rate
        st.markdown(f":chart_with_upwards_trend: Exchange Rate: **1 {base_currency} = {rate:.2f} {target_currency}**")
        st.markdown(f"<span style='background-color:green; color:white; padding:5px; border-radius:5px;'>{amount} {base_currency} = {converted_amount:.2f} {target_currency}</span>", unsafe_allow_html=True)
        
    else:
        st.markdown(":x: Invalid currency selection.")
except Exception as e:
    st.error(":warning: Error fetching exchange rates. Please try again later.")
