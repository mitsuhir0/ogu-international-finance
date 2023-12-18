import streamlit as st
import datetime
import pandas as pd
import pandas_datareader.data as web
import matplotlib.pyplot as plt

from pandas_datareader import wb
from datetime import datetime

st.set_page_config(layout="wide")

def read_fred(key: str) -> pd.Series:
  """pandas_datareaderを使ってFREDからデータを取得"""
  ser = web.DataReader(key, data_source='fred', start='1900-01').iloc[:, 0]
  return ser


def extract_title(string: str) -> tuple[str]:
    # カッコの位置を探す
    left_paren = string.index("(")
    right_paren = string.index(")")

    # カッコ以前の文字列とカッコ内の文字列を取り出す
    before = string[:left_paren].strip()
    inside = string[slice(left_paren+1, right_paren)]

    # タプルにして返す
    return (before, inside)


title = "Japanese Yen to U.S. Dollar Spot Exchange Rate"
source = "Source: Board of Governors of the Federal Reserve System (US)"
code = "DEXJPUS"
df = web.DataReader(code, data_source='fred', start=2005)
st.write(title)
st.line_chart(df)
st.write(source)


title = "Assets: Total Assets: Total Assets \n(Less Eliminations from Consolidation): Wednesday Level"
source = "Source: Board of Governors of the Federal Reserve System (US)"
code = "WALCL"
df = web.DataReader(code, "fred", start="2000")
st.write(title)
st.line_chart(df)
st.write(source)


title = "Real Personal Consumption Expenditures"
source = "Source: U.S. Bureau of Economic Analysis"
code = "PCEC96"
df = web.DataReader(code, "fred", start=2018)
st.write(title)
st.line_chart(df)
st.write(source)


title = "Dow Jones Industrial Average"
source = "Source: S&P Dow Jones Indices LLC"
code = "DJIA"
df = web.DataReader(code, 'fred', start=2000)
st.write(title)
st.line_chart(df)
st.write(source)


title = "Federal Funds Effective Rate (DFF)"
source = "Source: Board of Governors of the Federal Reserve System (US)"
code =  "DFF"
df = web.DataReader(code, "fred", start=2007)
st.write(title)
st.line_chart(df)
st.write(source)


code =  "IRSTCI01JPM156N"
title = "Interest Rates: Immediate Rates (< 24 Hours): Call Money/Interbank Rate: Total for Japan"
source = "Source: Organization for Economic Co-operation and Development"
df = web.DataReader(code, "fred", start=2008)
plt.axhline(y=0, color='red', linewidth=0.5)
st.write(title)
st.line_chart(df)
st.write(source)


title = "ECB Main Refinancing Operations Rate: Fixed Rate Tenders for Euro Area"
source = "Source: European Central Bank"
code = "ECBMRRFR"
df = web.DataReader(code, "fred", start=2008)
st.write(title)
st.line_chart(df)
st.write(source)


title = "Daily Sterling Overnight Index Average (SONIA) Rate"
source = "Source: Bank of England"
code = "IUDSOIA"
df = web.DataReader(code, "fred", start=2008)
st.write(title)
st.line_chart(df)
st.write(source)


title = "Nikkei Stock Average, Nikkei 225"
source = "Source: Nikkei Industry Research Institute"
code = "NIKKEI225"
df = web.DataReader(code, "fred", start=1900)
st.write(title)
st.line_chart(df)
st.write(source)


title, code = extract_title("Assets: Securities Held Outright: Mortgage-Backed Securities: Wednesday Level (WSHOMCB)")
src = "Source: Board of Governors of the Federal Reserve System (US)"
df = web.DataReader(code, "fred", start=1900)
st.write(title)
st.line_chart(df)
st.write(source)


st.markdown("* [住宅価格指数、コピーライトにより複製不可](https://fred.stlouisfed.org/series/csushpinsa)")


title, code = extract_title("Unemployment Rate (UNRATE)	")
src = "Source: U.S. Bureau of Labor Statistics"
df = web.DataReader(code, "fred", start=1990)
st.write(title)
st.line_chart(df)
st.write(source)


# 米国金融機関の経営破綻
title = "Bank Failures in Brief (US)"
source = "Source: The Federal Deposit Insurance Corporation (FDIC)"
url = "https://www.fdic.gov/bank/historical/bank/bfb-data.csv"
asset_name = "Approx. Asset (Millions)"

# データの読み込み
df = (
    pd.read_csv(url, encoding='shift-jis')
    .assign(year=lambda x: pd.to_datetime(x["Closing Date"]).dt.year) # 年月のフォーマット
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
fig, ax = plt.subplots()
ser = (
    ser.reindex(range(ser.index.min(), ser.index.max()+1), fill_value=0)
)
st.write(title)
st.bar_chart(ser)
st.write(source)


# 金額の集計
ser = (
    df.
    groupby("year")
    ['asset']
    .sum()
)
# プロット
fig, ax = plt.subplots()
ser = (
    ser.reindex(range(ser.index.min(), ser.index.max()+1), fill_value=0)
)
st.write(asset_name)
st.bar_chart(ser)
st.write(source)

st.markdown("- [Bank Failures in Brief](https://www.fdic.gov/bank/historical/bank/)")


indicator = "NY.GDP.MKTP.KD.ZG"
countries = ["US", "EU", "JP"]
title = "GDP growth (annual %)"
source = "Source: World Bank and OECD"
this_year = datetime.today().year
df = (
    wb.download(indicator=indicator, country=countries, start=2000, end=this_year)
    .unstack(level=0)
    [indicator]
)
ax.axhline(y=0, color='k', linewidth=0.5)
st.write(title)
st.line_chart(df)
st.write(source)


title = "Central government debt, total (% of GDP)"
id = "GC.DOD.TOTL.GD.ZS"
countries = ["US", "JP", "GR", "GB", "ES"]
source = "Source: International Monetary Fund, Government Finance Statistics Yearbook and data files, and World Bank and OECD GDP estimates."
this_year = datetime.today().year
df = (
    wb.download(indicator=id, country=countries, start=1989, end=this_year)
    .unstack(level=0)
    [id]
)
st.write(title)
st.line_chart(df)
st.write(source)


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
ax.axvline(x='1999', color='k', linewidth=0.5)
st.write(title)
st.line_chart(ser)
st.write(source)


title, code = extract_title("Japan Intervention: Japanese Bank purchases of USD against JPY (JPINTDUSDJPY)")
source = "Source: Bank of Japan"
df = web.DataReader(code, "fred", start=1990)
st.write(title)
st.line_chart(df)
st.write(source)


title = "Interest Rates: Long-Term Government Bond Yields: 10-Year"
source = "Source: Organization for Economic Co-operation and Development"
code = "IRLTLT01JPM156N"
country = "Japan"
# まず日本
df = web.DataReader(code, "fred", start=1995).rename(columns={code: country})
# 他の国を追加
codes = (
("Greece",   "IRLTLT01GRM156N"),
("Germany",  "IRLTLT01DEM156N"),
("Hungary",  "IRLTLT01HUM156N"),
("Ireland",  "IRLTLT01IEM156N"),
("Italy",    "IRLTLT01ITM156N"),
("Portugal", "IRLTLT01PTM156N"),
("Spain",    "IRLTLT01ESM156N"),
)
for country, code in codes:
  add_df = web.DataReader(code, "fred", start=1995).rename(columns={code: country})
  df = df.join(add_df)
# プロット
fig, ax = plt.subplots()
df = df.loc["2000":]#.plot(title=title, ax=ax)
st.write(title)
st.line_chart(df)
st.write(source)


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
ax.axhline(y=0, color='k', linewidth=0.5)
st.write(title)
st.line_chart(df)
st.write(source)


title, code = extract_title("Unemployment Rate: Aged 15-64: All Persons for Greece (LRUN64TTGRQ156S)")
source = "Source: Organization for Economic Co-operation and Development"
df = web.DataReader(code, "fred", start=1990)
st.write(title)
st.line_chart(df)
st.write(source)