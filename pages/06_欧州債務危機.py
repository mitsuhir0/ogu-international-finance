import streamlit as st
import datetime
import pandas as pd
import pandas_datareader.data as web
import app
import plotly.express as px

from pandas_datareader import wb
from datetime import datetime


st.markdown("## 欧州債務危機")

st.write("各国で政府債務残高が上昇")
title = "Central government debt, total (% of GDP)"
id = "GC.DOD.TOTL.GD.ZS"
countries = ["US", "JP", "GB", "GR", "ES"]
source = "Source: International Monetary Fund, Government Finance Statistics Yearbook and data files, and World Bank and OECD GDP estimates."
this_year = datetime.today().year
df = (
    wb.download(indicator=id, country=countries, start=1989, end=this_year)
    .unstack(level=0)
    [id]
)
st.write(title)
fig = px.line(df.ffill().dropna())
st.plotly_chart(fig)
st.write(source)


st.write("長期金利の高騰")
title = "Interest Rates: Long-Term Government Bond Yields: 10-Year"
source = "Source: Organization for Economic Co-operation and Development"
code = "IRLTLT01JPM156N"
country = "Japan"
# まず日本
df = web.DataReader(code, "fred", start=2005).rename(columns={code: country})
# 他の国を追加
codes = (
("Greece",   "IRLTLT01GRM156N"),
("Germany",  "IRLTLT01DEM156N"),
# ("Hungary",  "IRLTLT01HUM156N"),
("Ireland",  "IRLTLT01IEM156N"),
("Italy",    "IRLTLT01ITM156N"),
("Portugal", "IRLTLT01PTM156N"),
("Spain",    "IRLTLT01ESM156N"),
)
for country, code in codes:
  add_df = web.DataReader(code, "fred", start=1995).rename(columns={code: country})
  df = df.join(add_df)
# プロット
df = df.loc["2000":]
st.write(title)
fig = px.line(df.ffill().dropna())
st.plotly_chart(fig)
st.write(source)


st.write("ギリシャ経済はその後プラス成長に転じる")
indicator = "NY.GDP.MKTP.KD.ZG"
countries = ["GR", "DE", "IT"]
this_year = datetime.today().year
title = "GDP growth (annual %)"
source = "Source: World Bank and OECD"
df = (
    wb.download(indicator=indicator, country=countries, start=1995, end=this_year)
    .unstack(level=0)
    [indicator]
)
st.write(title)
fig = px.line(df.ffill().dropna())
st.plotly_chart(fig)
st.write(source)

st.write("失業率は改善傾向")
title, code = app.extract_title("Unemployment Rate: Aged 15-64: All Persons for Greece (LRUN64TTGRQ156S)")
source = "Source: Organization for Economic Co-operation and Development"
df = web.DataReader(code, "fred", start=1990)
st.write(title)
fig = px.line(df.ffill().dropna())
st.plotly_chart(fig)
st.write(source)


st.markdown("## EUとユーロ")
st.write("基礎的条件の収斂")
indicator = "FP.CPI.TOTL.ZG"
countries = ["DE", "BE", "FR", "IT", "LU", "NL", "DK", "IE", "GB"]
title = "Inflation, consumer prices (annual %)"
source = "Source: International Monetary Fund, International Financial Statistics"
this_year = datetime.today().year
ser = (
    wb.download(indicator=indicator, country=countries, start=1900, end=this_year)
    .unstack(level=0)
    [indicator]
)
ser.index = pd.to_datetime(ser.index)
st.write(title)
st.line_chart(ser)
st.write(source)
