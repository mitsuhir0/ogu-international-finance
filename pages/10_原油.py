import streamlit as st
import pandas_datareader.data as web


st.write("原油相場")
title = "Crude Oil Prices: West Texas Intermediate (WTI), - Cushing, Oklahoma"
code = "DCOILWTICO"
source = "Source: U.S. Energy Information Administration"
st.write(title)
st.line_chart(web.DataReader(code, "fred", start=2000))
