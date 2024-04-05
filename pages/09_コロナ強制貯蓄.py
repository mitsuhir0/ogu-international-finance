import streamlit as st
import pandas_datareader.data as web
import plotly.express as px

st.write("コロナ禍ショックによる強制貯蓄")
title = "Real Personal Consumption Expenditures"
source = "Source: U.S. Bureau of Economic Analysis"
code = "PCEC96"
df = web.DataReader(code, "fred", start=2000)
st.write(title)
fig = px.line(df.ffill().dropna())
st.plotly_chart(fig)
st.write(source)
