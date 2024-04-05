import streamlit as st
import pandas_datareader.data as web
import plotly.express as px

title = "Japanese Yen to U.S. Dollar Spot Exchange Rate"
source = "Source: Board of Governors of the Federal Reserve System (US)"
code = "DEXJPUS"
df = web.DataReader(code, data_source='fred', start=1950)
st.write(title)
fig = px.line(df.ffill().dropna())
st.plotly_chart(fig)
st.write(source)
