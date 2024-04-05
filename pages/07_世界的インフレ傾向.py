import streamlit as st
import datetime
import pandas as pd

from pandas_datareader import wb
from datetime import datetime

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
