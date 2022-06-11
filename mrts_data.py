import pandas as pd
url = "https://docs.google.com/spreadsheets/d/1dUQBO9mrMkCemnHBuloCod753e3bt58f/edit#gid=1912690947"
url = url.replace('/edit#gid=', '/export?format=csv&gid=')

df = pd.read_csv(url, skiprows=4, sheet_name="2020")
print(df)