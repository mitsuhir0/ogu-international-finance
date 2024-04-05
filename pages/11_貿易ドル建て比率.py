import streamlit as st
import datetime
import pandas as pd

from datetime import datetime

def query_world_usd_share(df: pd.DataFrame) -> pd.DataFrame:
  return ( 
      df
      .query("Area == 'WORLD'")
      .query("currency_1st == 'USD'")
      [["Year & Month", "share_1st"]]
      .set_index("Year & Month")
  )

st.write("日本の貿易におけるドル建て比率は高い")
base = "https://www.customs.go.jp/toukei/shinbun/tuuka/"
export_url = base + "timeseriesSCT_e.csv"
import_url = base + "timeseriesSCT_i.csv"
export = pd.read_csv(export_url, encoding="shift-jis", skiprows=4).pipe(query_world_usd_share)
import_to_japan = pd.read_csv(import_url, encoding="shift_jis", skiprows=4).pipe(query_world_usd_share)
df = export.join(import_to_japan, lsuffix="export", rsuffix="import")
df.columns = ["export from Japan", "import to Japan"]

date_format = '%Y%b'
index = [datetime.strptime(idx[:7], date_format) for idx in df.index]
datetime_index = pd.DatetimeIndex(index)
df.index = datetime_index
st.write("Dollar Share")
st.line_chart(df)
st.write("Source: Trade Statistics of Japan")
