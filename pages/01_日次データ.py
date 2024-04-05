import pandas_datareader.data as web
import streamlit as st
import plotly.express as px

start = '2024-04-01'

code = "DJIA"
dow = web.DataReader(code, 'fred', start=start)

code = "NIKKEI225"
nikkei = web.DataReader(code, "fred", start=start)

df = dow.join(nikkei).ffill()
fig = px.line(df)
st.plotly_chart(fig)
