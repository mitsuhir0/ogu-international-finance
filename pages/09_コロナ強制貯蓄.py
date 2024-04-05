import streamlit as st
import pandas_datareader.data as web

st.write("コロナ禍ショックによる強制貯蓄")
title = "Real Personal Consumption Expenditures"
source = "Source: U.S. Bureau of Economic Analysis"
code = "PCEC96"
df = web.DataReader(code, "fred", start=2000)
st.write(title)
st.line_chart(df)
st.write(source)
