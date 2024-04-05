import streamlit as st
import pandas_datareader.data as web

title = "Japanese Yen to U.S. Dollar Spot Exchange Rate"
source = "Source: Board of Governors of the Federal Reserve System (US)"
code = "DEXJPUS"
df = web.DataReader(code, data_source='fred', start=2005)
st.write(title)
st.line_chart(df)
st.write(source)
