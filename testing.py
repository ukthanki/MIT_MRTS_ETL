import pandas as pd
import xlrd

def add_dataframe(list_of_df, year):
    df = pd.read_excel("mrtssales92-present.xls", sheet_name=year, skiprows=4, skipfooter=48)
    df.drop(["Unnamed: 0", "TOTAL"], axis=1, inplace=True)
    df.rename({"Unnamed: 1" : "Kind of Business"}, axis=1, inplace=True)
    df_trans = df.melt(id_vars="Kind of Business",value_vars=df.columns[1:])
    df_trans.replace("(S)", "0", inplace=True)
    df_trans.replace("(NA)", "0", inplace=True)
    df_trans.dropna(axis=0, inplace=True)
    df_trans["Period"] = "01 " + df_trans["variable"]
    df_trans["value"] = df_trans["value"].astype(float)
    df_trans = df_trans.astype({"Period" : "datetime64[ns]"})
    df_trans.drop("variable", axis=1, inplace=True)

    list_of_df.append(df_trans)

list_df = []
years = []
year = 2020
while year >= 1992:
    years.append(str(year))
    year -= 1

for year in years:
    add_dataframe(list_df, year)

print(list_df)   
df_stacked = pd.concat(list_df)
df_stacked.reset_index(inplace=True)
df_stacked.drop("index", axis=1, inplace=True)
print(df_stacked)

print(len(df_stacked))

for row_num in range(0, len(df_stacked)):
    row_data = df_stacked.iloc[row_num]
    value = (row_data[0], row_data[1], row_data[2])
    print(row_data[0], row_data[1], row_data[2])
    sql = "INSERT INTO test (kind_of_business, value, period) VALUES (%s, %s, %s)"
    MyCursor.execute(sql, value)