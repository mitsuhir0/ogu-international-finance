import streamlit as st
import pandas_datareader.data as web
import app
import plotly.express as px

st.write("2022・23年に円安抑制の為替介入を実施")
title, code = app.extract_title("Japan Intervention: Japanese Bank purchases of USD against JPY (JPINTDUSDJPY)")
source = "Source: Bank of Japan"
df = web.DataReader(code, "fred", start=1990)
st.write(title)
fig = px.line(df.ffill().dropna())
st.plotly_chart(fig)
st.write(source)
