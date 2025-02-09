import streamlit as st
import requests

st.title(":currency_exchange: Currency Converter")
st.caption("Convert currencies in real-time!")

# Select currencies
base_currency = st.selectbox(":earth_americas: From Currency:", ["USD", "EUR", "GBP", "JPY", "BRL"])
target_currency = st.selectbox(":coin: To Currency:", ["USD", "EUR", "GBP", "JPY", "BRL"])

# Input amount
amount = st.number_input(":dollar: Enter Amount:", min_value=0.01, value=100.00, step=1.00, format="%.2f")

# Fetch exchange rates automatically when values change
try:
    url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
    response = requests.get(url)
    data = response.json()

    if "rates" in data and target_currency in data["rates"]:
        rate = float(data["rates"][target_currency])  # Ensure it's a float
        converted_amount = amount * rate

        # Display exchange rate with 2 decimal places
        st.info(f":chart_with_upwards_trend: Exchange Rate: **1 {base_currency} = {rate:.2f} {target_currency}**")

        # Display conversion result
        st.success(f":white_check_mark: {amount} {base_currency} = {converted_amount:.2f} {target_currency}")

    else:
        st.error(":x: Invalid currency selection.")
except Exception as e:
    st.error(":warning: Error fetching exchange rates. Please try again later.")
