import pandas_datareader.data as web

start = '2024-04-01'

code = "DJIA"
dow = web.DataReader(code, 'fred', start=start)

code = "NIKKEI225"
nikkei = web.DataReader(code, "fred", start=start)

df = dow.join(nikkei)
df
