import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

st.header('Line chart')

chart_data = pd.DataFrame(
     np.random.randn(20, 3),
     columns=['a', 'b', 'c'])

# st.line_chart(data=None, *, x=None, y=None, x_label=None, y_label=None, color=None, width=None, height=None, use_container_width=True)

st.line_chart(data=chart_data,x="a", x_label="A", y=["b", "c"],y_label=["B", "C"], color=[ "#0000FF", "#00FF00"])

st.line_chart(data=chart_data, color=[ "#FF0000","#0000FF", "#00FF00"])

st.line_chart(data=chart_data, color=[ "#FF0000","#0000FF", "#00FF00"], width=300, height=300, use_container_width = False)


c = (
   alt.Chart(chart_data)
   .mark_circle()
   .encode(x="a", y="b", size="c", color="c", tooltip=["a", "b", "c"])
)

st.altair_chart(c, use_container_width=True)