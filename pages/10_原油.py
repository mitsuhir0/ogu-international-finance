import streamlit as st
import pandas_datareader.data as web
import plotly.express as px


st.write("原油相場")
title = "Crude Oil Prices: West Texas Intermediate (WTI), - Cushing, Oklahoma"
code = "DCOILWTICO"
source = "Source: U.S. Energy Information Administration"
st.write(title)
df = web.DataReader(code, "fred", start=2000)
fig = px.line(df.ffill().dropna())
st.plotly_chart(fig)
