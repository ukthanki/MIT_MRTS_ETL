[Go to Back to Home Page](https://ukthanki.github.io/)

# MIT Data Engineering Professional Certification

## Monthly Retail Trade Survey ETL

<p align="center">
    <img width="100%" src="https://github.com/ukthanki/MIT_MRTS_ETL/assets/42117481/287fc16c-81d0-4b9a-b483-1e6aa881755e">
</p>

Up to this point in the course, we had learned the following topics:
1. NumPy
2. Pandas
3. SQL
4. Linear Regression
5. ETL Fundamentals

In this project, we explored the Monthly Retail Trade Survey (MRTS) data set for the years 1992-2020 and perform an Extract-Transformation-Load (ETL) process through a variety of steps. This involved processing the data in Python, programmatically creating a MySQL database and table, loading the data into the table, and then using Python to query from the database and analyze it for trends, percentage changes, as well as rolling time windows paired with visualization for enhanced understanding of the data.

You can learn more about MRTS [here](https://www.census.gov/retail/about_the_surveys.html).

We first started by studying the data in question and its structure so that we can assess how to load it into a Data Frame. Since we were looking at a wide range of years, each year was a separate tab in the raw Excel spreadsheet. In order to analyze the data effectively, we had to compile all of the relevant data into a single Data Frame.

The data had a similar structure in each tab and it was determined that the following cleaning process could be used repeatedly for each year's MRTS data:
- Reading the sheet into a Data Frame, skipping the first 4 and reading the next 67 rows
- Dropping the first Unnamed column
- Renaming the second Unnamed column to "Kind of Business"
- Transposing the Data Frame
- Replacing all "(S)" and "(NA)" entries with "0"
- Removing NaN rows
- Adding a DateTime column and converting the numeric values to Floats

I saw this as an opportunity to be more efficient with my code by creating a function that does this for all of the required tabs in the Excel spreadsheet, as shown below:

```python
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

```

The function is then used in the code below to efficiently output a single Data Frame with all of the data:

```python
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
```

I created a separate YAML file that contained the credentials of the database connection that had to be established to load the data into a designated table. The benefit of this type of file is that it stores this sensitive information in a separate file so that it is not hard-coded in the main file.

Once the connection was made, I created the table and loaded the records from the Data Frame into the table, as shown below:

```python
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

...

# Inserting each row of the DataFrame to the MySQL table and committing
for row_num in range(0, len(df_stacked)):
    row_data = df_stacked.iloc[row_num]
    value = (row_data[0], row_data[1], row_data[2])
    sql = "INSERT INTO mrts (kind_of_business, value, period) VALUES (%s, %s, %s)"
    MyCursor.execute(sql, value)

cnx.commit()

```

| ![image](https://github.com/ukthanki/MIT_House_Price_Prediction_Project/assets/42117481/809779b0-251f-41d9-bbee-21ad7f6c7746)| 
|:--:| 
| **Figure 1.** Null entry counts in each field in the original dataset. |



**You can view the full Project in the "module_8.py" and "Module 8_Umang_Thanki.ipynb" files in the Repository.**

