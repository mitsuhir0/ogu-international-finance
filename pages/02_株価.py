import streamlit as st
import pandas_datareader.data as web
import plotly.express as px

title = "Dow Jones Industrial Average"
source = "Source: S&P Dow Jones Indices LLC"
code = "DJIA"
df = web.DataReader(code, 'fred', start=2000)
st.write(title)
fig = px.line(df.ffill())
st.plotly_chart(fig)
st.write(source)

title = "Nikkei Stock Average, Nikkei 225"
source = "Source: Nikkei Industry Research Institute"
code = "NIKKEI225"
df = web.DataReader(code, "fred", start=1900)
st.write(title)
fig = px.line(df.ffill())
st.plotly_chart(fig)
st.write(source)


# ダウと日経平均をそろえる。為替レートでドル建てにする
st.write("ダウ平均と日経はどちらも上昇傾向だが…")
code = "DEXJPUS"
er = web.DataReader(code, data_source='fred', start=2010)

code = "NIKKEI225"
nikkei = web.DataReader(code, "fred", start=1900)

code = "DJIA"
dow = web.DataReader(code, 'fred', start=2000)

idx = dow.index[0]
df = (
    dow
    .join(nikkei)
    .apply(lambda x: x.div(x.iloc[0])*100)
)
title = f"{idx.year}-{idx.month}-{idx.day}=100"
st.write(title)
fig = px.line(df.ffill().dropna())
st.plotly_chart(fig)

# ドル建て
st.write("ドル建てにすると違ってみえる")
df = (
    dow
    .join(nikkei)
    .join(er)
)
df = (
    df
    .assign(NIKKEI225_doller=df.NIKKEI225/df.DEXJPUS)
    .apply(lambda x: x.div(x.iloc[0])*100)
    .drop("DEXJPUS", axis=1)
)
title = f"{idx.year}-{idx.month}-{idx.day}=100"
st.write(title)
fig = px.line(df.ffill().dropna())
st.plotly_chart(fig)
