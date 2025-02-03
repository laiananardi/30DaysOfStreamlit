import pandas as pd
import streamlit as st

# Correct import for ydata-profiling
from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report

# Load dataset
df = pd.read_csv("https://storage.googleapis.com/tf-datasets/titanic/train.csv")

# Generate profile report
pr = ProfileReport(df, explorative=True)

# Display report in Streamlit
st.title("Pandas Profiling Report")
st_profile_report(pr)
