import datetime
import streamlit as st
import pandas as pd
import pandas_datareader.data as web
import app
from pandas_datareader import wb
import plotly.express as px


st.markdown("## 世界的金融危機")
st.markdown("* [住宅価格指数](https://fred.stlouisfed.org/series/csushpinsa)")


st.write("失業率は上昇")
title, code = app.extract_title("Unemployment Rate (UNRATE)	")
source = "Source: U.S. Bureau of Labor Statistics"
df = web.DataReader(code, "fred", start=1990)
st.write(title)
fig = px.line(df.ffill().dropna())
st.plotly_chart(fig)
st.write(source)


st.write("300行以上の銀行が経営破綻に陥った")
# 米国金融機関の経営破綻
title = "Bank Failures in Brief (US)"
source = "Source: The Federal Deposit Insurance Corporation (FDIC)"
url = "https://www.fdic.gov/resources/resolutions/bank-failures/in-brief/documents/bfb-all-data.csv"
asset_name = "Approx. Asset (Millions)"
# データの読み込み
df = (
    pd.read_csv(url, encoding='shift-jis')
    .assign(year=lambda x: pd.to_datetime(x["Closing Date"], format='mixed').dt.year) # 年月のフォーマット
    .assign(asset=lambda x: x[asset_name].replace('[\$,]', '', regex=True).astype(float)) # ドル表示を数値化
)
# 破綻件数を年ごとに集計
ser= (
    df
    .groupby("year")
    .count()
    ["Closing Date"]
)
# 0件をindexに追加してプロット
ser = (
    ser.reindex(range(ser.index.min(), ser.index.max()+1), fill_value=0)
)
st.write(title)
fig = px.bar(ser)
st.plotly_chart(fig)
st.write(source)

# 金額の集計
ser = (
    df.
    groupby("year")
    ['asset']
    .sum()
)
# プロット
ser = (
    ser.reindex(range(ser.index.min(), ser.index.max()+1), fill_value=0)
)
st.write(asset_name)
fig = px.bar(ser)
st.plotly_chart(fig)
st.write(source)
st.markdown("- [Bank Failures in Brief](https://www.fdic.gov/bank/historical/bank/)")


st.markdown("先進国は軒並みGDPマイナス成長を記録")
indicator = "NY.GDP.MKTP.KD.ZG"
countries = ["US", "JP", "DE", "GB", "CA"]
title = "GDP growth (annual %)"
source = "Source: World Bank and OECD"
this_year = datetime.datetime.today().year
df = (
    wb.download(indicator=indicator, country=countries, start=2000, end=this_year)
    .unstack(level=0)
    [indicator]
)
st.write(title)
fig = px.line(df.dropna())
st.plotly_chart(fig)
st.write(source)

st.write("当局はMBSをたくさん購入")
title, code = app.extract_title("Assets: Securities Held Outright: Mortgage-Backed Securities: Wednesday Level (WSHOMCB)")
src = "Source: Board of Governors of the Federal Reserve System (US)"
df = web.DataReader(code, "fred", start=1900)
st.write(title)
fig = px.line(df.ffill().dropna())
st.plotly_chart(fig)
st.write(source)


st.write("FRBの資産が膨れ上がる")
title = "Assets: Total Assets: Total Assets \n(Less Eliminations from Consolidation): Wednesday Level"
source = "Source: Board of Governors of the Federal Reserve System (US)"
code = "WALCL"
df = web.DataReader(code, "fred", start="2000")
st.write(title)
fig = px.line(df.ffill().dropna())
st.plotly_chart(fig)
st.write(source)
