from cProfile import label
import yaml
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import datetime

# Function created for efficiency and automation
def add_dataframe(list_of_df, year):
    """Appends a DataFrame to a list that corresponds to the year of a specific sheet of the MRTS Sales Data."""
    df = pd.read_excel("mrtssales92-present.xls", sheet_name=year, skiprows=4, nrows=67)
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

# Secure Connection to the Database
db = yaml.safe_load(open("db.yaml"))
config = {
    "user":     db["user"],
    "password": db["pwrd"],
    "host":     db["host"],
    "auth_plugin":  "mysql_native_password"
}
cnx = mysql.connector.connect(**config)

MyCursor=cnx.cursor()
queries = []

# Creating the database and the table `mrts`
queries.append("DROP DATABASE IF EXISTS mrtsdb")
queries.append("CREATE DATABASE mrtsdb")
queries.append("USE mrtsdb")
queries.append("""CREATE TABLE mrts (
    kind_of_business VARCHAR (300) NOT NULL,
    value FLOAT NOT NULL,
    period DATE NULL) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4 COLLATE=utf8mb4_0900_ai_ci""")

for query in queries:
    MyCursor.execute(query)


list_df = []
years = []
year = 2020
while year >= 1992:
    years.append(str(year))
    year -= 1

for year in years:
    add_dataframe(list_df, year)
    
df_stacked = pd.concat(list_df)
df_stacked.reset_index(inplace=True)
df_stacked.drop("index", axis=1, inplace=True)

# Inserting each row of the DataFrame to the MySQL table and committing
for row_num in range(0, len(df_stacked)):
    row_data = df_stacked.iloc[row_num]
    value = (row_data[0], row_data[1], row_data[2])
    sql = "INSERT INTO mrts (kind_of_business, value, period) VALUES (%s, %s, %s)"
    MyCursor.execute(sql, value)

cnx.commit()
##################################### QUERIES #####################################
# ---------------------------------------------------------------------------------------------------------------------------
# (1) Dr. Sanchez's Test Query
# query1 = """
# SELECT DATE_FORMAT(period, "%d-%m-%Y"), CAST(SUM(value) AS UNSIGNED) AS sales FROM mrts
# WHERE kind_of_business = "Retail and food services sales, total"
# GROUP BY 1"""
# MyCursor.execute(query1)
# month = []
# sales = []
# for row in MyCursor.fetchall():
#     print(row)
#     month.append(row[0])
#     sales.append(row[1])
# plt.plot(month, sales)
# plt.show()

# ---------------------------------------------------------------------------------------------------------------------------
# (2) Data Verification Query 1
# query2 = "SELECT SUM(`value`) FROM mrts WHERE period = '2008-03-01'"
# MyCursor.execute(query2)
# for row in MyCursor.fetchall():
#     print(row)

# ---------------------------------------------------------------------------------------------------------------------------
# (3) Data Verification Query 2
# query3 = """SELECT `value` FROM mrts WHERE kind_of_business = 'Health and personal care stores' AND period = '2015-06-01';"""
# MyCursor.execute(query3)
# for row in MyCursor.fetchall():
#     print(row)

# ---------------------------------------------------------------------------------------------------------------------------
# (4) Retail and food services sales, total Monthly Trend
# query4 = """
# SELECT `value`, period FROM mrts WHERE kind_of_business = "Retail and food services sales, total" ORDER BY period"""
# MyCursor.execute(query4)
# month = []
# sales = []
# for row in MyCursor.fetchall():
#     sales.append(row[0])
#     month.append(row[1])
    
# plt.plot(month, sales)
# plt.title("Retail and food services sales, total - Monthly")
# plt.xlabel("Year")
# plt.ylabel("Sales (USD, Million)")
# plt.show()

# ---------------------------------------------------------------------------------------------------------------------------
# (5) Retail and food services sales, total Yearly Trend
# query5 = """
# SELECT SUM(`value`), YEAR(period) FROM mrts WHERE kind_of_business = 'Retail and food services sales, total'
# GROUP BY 2 ORDER BY period
# """
# MyCursor.execute(query5)
# month = []
# sales = []
# for row in MyCursor.fetchall():
#     sales.append(row[0])
#     month.append(row[1])
    
# plt.plot(month, sales)
# plt.title("Retail and food services sales, total - Yearly")
# plt.xlabel("Year")
# plt.ylabel("Sales (USD, Million)")
# plt.show()

# ---------------------------------------------------------------------------------------------------------------------------
# (6) Three Industries - Trend Comparison - Yearly
# query6a = """
# SELECT SUM(`value`), YEAR(period) FROM mrts WHERE kind_of_business = 'Book stores' GROUP BY YEAR(period) ORDER BY period
# """
# MyCursor.execute(query6a)
# Year = []
# book_sales = []
# for row in MyCursor.fetchall():
#     book_sales.append(row[0])
#     Year.append(row[1])
# plt.plot(Year, book_sales)


# query6b = """
# SELECT SUM(`value`), YEAR(period) FROM mrts WHERE kind_of_business = 'Sporting goods stores' GROUP BY YEAR(period) ORDER BY period
# """
# MyCursor.execute(query6b)
# Year = []
# sports_sales = []
# for row in MyCursor.fetchall():
#     sports_sales.append(row[0])
#     Year.append(row[1])
# plt.plot(Year, sports_sales)


# query6c = """
# SELECT SUM(`value`), YEAR(period) FROM mrts WHERE kind_of_business = 'Hobby, toy, and game stores' GROUP BY YEAR(period) ORDER BY period;"""
# MyCursor.execute(query6c)
# Year = []
# htg_sales = []
# for row in MyCursor.fetchall():
#     htg_sales.append(row[0])
#     Year.append(row[1])    
# plt.plot(Year, htg_sales)

# plt.title("Trend Comparison - Yearly")
# plt.xlabel("Year")
# plt.ylabel("Sales (USD)")
# plt.legend(labels=["Book stores", "Sporting goods stores", "Hobby, toy, and game stores"])
# plt.show()

# ---------------------------------------------------------------------------------------------------------------------------
# (7) Three Industries - Trend Comparison - Monthly
# query7a = """
# SELECT SUM(`value`), period FROM mrts WHERE kind_of_business = 'Book stores' GROUP BY period ORDER BY period
# """
# MyCursor.execute(query7a)
# Month = []
# book_sales = []
# for row in MyCursor.fetchall():
#     book_sales.append(row[0])
#     Month.append(row[1])
# plt.plot(Month, book_sales)


# query7b = """
# SELECT SUM(`value`), period FROM mrts WHERE kind_of_business = 'Sporting goods stores' GROUP BY period ORDER BY period
# """
# MyCursor.execute(query7b)
# Month = []
# sports_sales = []
# for row in MyCursor.fetchall():
#     sports_sales.append(row[0])
#     Month.append(row[1])
# plt.plot(Month, sports_sales)


# query7c = """
# SELECT SUM(`value`), period FROM mrts WHERE kind_of_business = 'Hobby, toy, and game stores' GROUP BY period ORDER BY period
# """
# MyCursor.execute(query7c)
# Month = []
# htg_sales = []
# for row in MyCursor.fetchall():
#     htg_sales.append(row[0])
#     Month.append(row[1])    
# plt.plot(Month, htg_sales)

# plt.title("Trend Comparison - Monthly")
# plt.xlabel("Month")
# plt.ylabel("Sales (USD)")
# plt.legend(labels=["Book stores", "Sporting goods stores", "Hobby, toy, and game stores"])
# plt.show()

# ---------------------------------------------------------------------------------------------------------------------------
# (9) New car dealers - Rolling Sum 2020

# query9a = """
# SELECT period, SUM(`value`) OVER(ORDER BY period) AS rolling_sum FROM mrts WHERE kind_of_business = "New car dealers" AND YEAR(period) = "2020";"""
# MyCursor.execute(query9a)
# Month = []
# cumulative_sales = []
# for row in MyCursor.fetchall():
#     Month.append(row[0])
#     cumulative_sales.append(row[1])
# plt.plot(Month, cumulative_sales)
# plt.title("New Car Dealers, 2020 Cumulative Sales")
# plt.xlabel("Month")
# plt.ylabel("Cumulative Sales (USD)")
# plt.show()

# query9b = """
# SELECT period, AVG(`value`) OVER(ORDER BY period ROWS BETWEEN 5 PRECEDING AND CURRENT ROW) AS rolling_average FROM mrts WHERE kind_of_business = 'Gasoline stations' and period BETWEEN '2000-01-01' and '2008-12-01'"""
# MyCursor.execute(query9b)
# Month = []
# average6mo_sales = []
# for row in MyCursor.fetchall():
#     Month.append(row[0])
#     average6mo_sales.append(row[1])
# plt.plot(Month, average6mo_sales)
# plt.title("Gasoline Stations, Last 6-months Average Sales, 2000-2008")
# plt.xlabel("Year")
# plt.ylabel("Last 6-months Average Sales (USD)")
# plt.show()

###################################################################################
MyCursor.close()

cnx.close()

# ---------------------------------------------------------------------------------------------------------------------------
# df_mens_stores = df_stacked[df_stacked["Kind of Business"] == "Men's clothing stores"].copy()
# df_mens_stores["Year"] = pd.DatetimeIndex(df_mens_stores["Period"]).year
# mens_pct = df_mens_stores.groupby("Year").agg({"value" : "sum"}).pct_change()

# df_womens_stores = df_stacked[df_stacked["Kind of Business"] == "Women's clothing stores"].copy()
# df_womens_stores["Year"] = pd.DatetimeIndex(df_womens_stores["Period"]).year
# womens_pct = df_womens_stores.groupby("Year").agg({"value" : "sum"}).pct_change()

# combined_df = pd.DataFrame()
# combined_df["Men's Clothing Stores Sales"] = mens_pct["value"].copy()
# combined_df["Women's Clothing Stores Sales"] = womens_pct["value"]
# combined_df.plot(title="Percent Change", ylabel="% Change")
# plt.show()

# ---------------------------------------------------------------------------------------------------------------------------

# df_mens_stores = df_stacked[df_stacked["Kind of Business"] == "Men's clothing stores"].copy()
# df_mens_stores["Year"] = pd.DatetimeIndex(df_mens_stores["Period"]).year
# df_womens_stores = df_stacked[df_stacked["Kind of Business"] == "Women's clothing stores"].copy()
# df_womens_stores["Year"] = pd.DatetimeIndex(df_womens_stores["Period"]).year

# mens_sales = df_mens_stores.groupby("Year").agg({"value" : "sum"})
# womens_sales = df_womens_stores.groupby("Year").agg({"value" : "sum"})
# combined_sales = mens_sales.copy()
# combined_sales.rename({"value":"Men's Sales"}, axis=1, inplace=True)
# combined_sales["Women's Sales"] = womens_sales["value"]
# combined_sales["Total"] = combined_sales["Men's Sales"] + combined_sales["Women's Sales"]
# combined_sales["Men's Percentage (%)"] = round((combined_sales["Men's Sales"]/combined_sales["Total"])*100, 2)
# combined_sales["Men's Percentage (%)"].plot(title="Men's Sales Percentage of Total", xlabel="Year", ylabel="Percentage, %")
# plt.show()

# ---------------------------------------------------------------------------------------------------------------------------
