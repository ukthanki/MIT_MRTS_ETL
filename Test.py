import yaml
import mysql.connector
import csv

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
queries.append("DROP DATABASE IF EXISTS testdatabase")
queries.append("CREATE DATABASE testdatabase")
queries.append("USE testdatabase")
queries.append("""CREATE TABLE test (
    first_name VARCHAR (20) NOT NULL,
    last_name VARCHAR (20) NOT NULL,
    age VARCHAR (3) NULL) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4 COLLATE=utf8mb4_0900_ai_ci""")

for query in queries:
    MyCursor.execute(query)
# inserts = []

with open("test_csv.csv") as csv_file:

    csv_reader = csv.reader(csv_file, delimiter=",")
    for row in csv_reader:
        if row[0] != "first name":
            value = (row[0], row[1], row[2])
            sql = "INSERT INTO test (first_name, last_name, age) VALUES (%s, %s, %s)"
            MyCursor.execute(sql, value)

cnx.commit()

query = ("SELECT * FROM test")
MyCursor.execute(query)

for row in MyCursor.fetchall():
    print(row)

MyCursor.close()

cnx.close()