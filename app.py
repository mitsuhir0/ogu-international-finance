import streamlit as st
import datetime
import pandas as pd
import pandas_datareader.data as web
import matplotlib.pyplot as plt

from pandas_datareader import wb
from datetime import datetime

st.set_page_config(layout="wide")


def extract_title(string: str) -> list[str]:
    # カッコの位置を探す
    left_paren = string.index("(")
    right_paren = string.index(")")

    # カッコ以前の文字列とカッコ内の文字列を取り出す
    before = string[:left_paren].strip()
    inside = string[slice(left_paren+1, right_paren)]

    return [before, inside]


def query_world_usd_share(df: pd.DataFrame) -> pd.DataFrame:
  return ( 
      df
      .query("Area == 'WORLD'")
      .query("currency_1st == 'USD'")
      [["Year & Month", "share_1st"]]
      .set_index("Year & Month")
  )

today = datetime.today()
st.title("国際金融論B 参考資料")
st.write(f"{today.year}-{today.month}-{today.day}")

st.markdown("## 金融関連指標")

st.markdown("### 為替レート")

title = "Japanese Yen to U.S. Dollar Spot Exchange Rate"
source = "Source: Board of Governors of the Federal Reserve System (US)"
code = "DEXJPUS"
df = web.DataReader(code, data_source='fred', start=2005)
st.write(title)
st.line_chart(df)
st.write(source)


st.write("日本の貿易におけるドル建て比率は高い")
export_url = "https://www.customs.go.jp/toukei/shinbun/tuuka/timeseriesSCT_e.csv"
import_url = "https://www.customs.go.jp/toukei/shinbun/tuuka/timeseriesSCT_i.csv"
export = pd.read_csv(export_url, encoding="shift-jis", skiprows=4).pipe(query_world_usd_share)
import_to_japan = pd.read_csv(import_url, encoding="shift_jis", skiprows=4).pipe(query_world_usd_share)
df = export.join(import_to_japan, lsuffix="export", rsuffix="import")
df.columns = ["export from Japan", "import to Japan"]

date_format = '%Y%b'
df.index = [datetime.strptime(idx[:7], date_format) for idx in df.index]
st.write("Dollar Share")
st.line_chart(df)
st.write("Source: Trade Statistics of Japan")


st.markdown("### 株価")

title = "Dow Jones Industrial Average"
source = "Source: S&P Dow Jones Indices LLC"
code = "DJIA"
df = web.DataReader(code, 'fred', start=2000)
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
    .apply(lambda x: x.div(x[0])*100)
)
title = f"{idx.year}-{idx.month}-{idx.day}=100"
st.write(title)
st.line_chart(df.dropna())

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
    .apply(lambda x: x.div(x[0])*100)
    .drop("DEXJPUS", axis=1)
)
title = f"{idx.year}-{idx.month}-{idx.day}=100"
st.write(title)
st.line_chart(df.dropna())


st.markdown("### 政策金利")

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
st.line_chart(df)


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


st.markdown("## 世界的金融危機")

st.markdown("* [住宅価格指数](https://fred.stlouisfed.org/series/csushpinsa)")


st.write("失業率は上昇")
title, code = extract_title("Unemployment Rate (UNRATE)	")
source = "Source: U.S. Bureau of Labor Statistics"
df = web.DataReader(code, "fred", start=1990)
st.write(title)
st.line_chart(df)
st.write(source)


st.write("300行以上の銀行が経営破綻に陥った")
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
ser = (
    ser.reindex(range(ser.index.min(), ser.index.max()+1), fill_value=0)
)
st.write(asset_name)
st.bar_chart(ser)
st.write(source)
st.markdown("- [Bank Failures in Brief](https://www.fdic.gov/bank/historical/bank/)")


st.markdown("先進国は軒並みGDPマイナス成長を記録")
indicator = "NY.GDP.MKTP.KD.ZG"
countries = ["US", "JP", "DE", "GB", "CA"]
title = "GDP growth (annual %)"
source = "Source: World Bank and OECD"
this_year = datetime.today().year
df = (
    wb.download(indicator=indicator, country=countries, start=2000, end=this_year)
    .unstack(level=0)
    [indicator]
)
st.write(title)
st.line_chart(df)
st.write(source)

st.write("当局はMBSをたくさん購入")
title, code = extract_title("Assets: Securities Held Outright: Mortgage-Backed Securities: Wednesday Level (WSHOMCB)")
src = "Source: Board of Governors of the Federal Reserve System (US)"
df = web.DataReader(code, "fred", start=1900)
st.write(title)
st.line_chart(df)
st.write(source)


st.write("FRBの資産が膨れ上がる")
title = "Assets: Total Assets: Total Assets \n(Less Eliminations from Consolidation): Wednesday Level"
source = "Source: Board of Governors of the Federal Reserve System (US)"
code = "WALCL"
df = web.DataReader(code, "fred", start="2000")
st.write(title)
st.line_chart(df)
st.write(source)


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
st.line_chart(df)
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
st.line_chart(df)
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
st.line_chart(df)
st.write(source)

st.write("失業率は改善傾向")
title, code = extract_title("Unemployment Rate: Aged 15-64: All Persons for Greece (LRUN64TTGRQ156S)")
source = "Source: Organization for Economic Co-operation and Development"
df = web.DataReader(code, "fred", start=1990)
st.write(title)
st.line_chart(df)
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


st.write("### その他の指標")

st.write("2022・23年に円安抑制の為替介入を実施")
title, code = extract_title("Japan Intervention: Japanese Bank purchases of USD against JPY (JPINTDUSDJPY)")
source = "Source: Bank of Japan"
df = web.DataReader(code, "fred", start=1990)
st.write(title)
st.line_chart(df)
st.write(source)


st.write("世界的インフレ傾向")
indicator = "FP.CPI.TOTL.ZG"
countries = ["US", "GB", "DE", "JP", "KR"]
title = "Inflation, consumer prices (annual %)"
source = "Source: International Monetary Fund, International Financial Statistics"
this_year = datetime.today().year
ser = (
    wb.download(indicator=indicator, country=countries, start=2000, end=this_year)
    .unstack(level=0)
    [indicator]
)
ser.index = pd.to_datetime(ser.index)
st.write(title)
st.line_chart(ser)
st.write(source)


st.write("コロナ禍ショックによる強制貯蓄")
title = "Real Personal Consumption Expenditures"
source = "Source: U.S. Bureau of Economic Analysis"
code = "PCEC96"
df = web.DataReader(code, "fred", start=2000)
st.write(title)
st.line_chart(df)
st.write(source)


st.write("原油相場")
title = "Crude Oil Prices: West Texas Intermediate (WTI), - Cushing, Oklahoma"
code = "DCOILWTICO"
source = "Source: U.S. Energy Information Administration"
st.write(title)
st.line_chart(web.DataReader(code, "fred", start=2000))


st.markdown("* [不安定な暗号資産相場](https://fred.stlouisfed.org/series/CBBTCUSD)")
st.markdown("* [ボラティリティ](https://fred.stlouisfed.org/series/VIXCLS)")
