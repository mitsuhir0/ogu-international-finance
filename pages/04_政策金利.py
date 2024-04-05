import streamlit as st
import pandas_datareader.data as web
import plotly.express as px

st.write("日本は低金利政策が続いている")
us =  "DFF"
uk = "IUDSOIA"
jp =  "IRSTCI01JPM156N"
ecb = "ECBMRRFR"
df_us = web.DataReader(us, "fred", start=2008)
df_jp = web.DataReader(jp, "fred", start=2008)
df_ecb = web.DataReader(ecb, "fred", start=2008)
df_uk = web.DataReader(uk, "fred", start=2008)
df = (
    df_us
    .join(df_jp)
    .join(df_ecb)
    .join(df_uk)
    .ffill()
    .rename(columns={
        us: "United States",
        jp: "Japan",
        ecb: "ECB",
        uk: "United Kingdom"
        })
)
fig = px.line(df.ffill().dropna())
st.plotly_chart(fig)


title = "Federal Funds Effective Rate (DFF)"
source = "Source: Board of Governors of the Federal Reserve System (US)"
code =  "DFF"
df = web.DataReader(code, "fred", start=2007)
st.write(title)
fig = px.line(df.ffill().dropna())
st.plotly_chart(fig)
st.write(source)


code =  "IRSTCI01JPM156N"
title = "Interest Rates: Immediate Rates (< 24 Hours): Call Money/Interbank Rate: Total for Japan"
source = "Source: Organization for Economic Co-operation and Development"
df = web.DataReader(code, "fred", start=2008)
st.write(title)
fig = px.line(df.ffill().dropna())
st.plotly_chart(fig)
st.write(source)


title = "ECB Main Refinancing Operations Rate: Fixed Rate Tenders for Euro Area"
source = "Source: European Central Bank"
code = "ECBMRRFR"
df = web.DataReader(code, "fred", start=2008)
st.write(title)
fig = px.line(df.ffill().dropna())
st.plotly_chart(fig)
st.write(source)


title = "Daily Sterling Overnight Index Average (SONIA) Rate"
source = "Source: Bank of England"
code = "IUDSOIA"
df = web.DataReader(code, "fred", start=2008)
st.write(title)
fig = px.line(df.ffill().dropna())
st.plotly_chart(fig)
st.write(source)
