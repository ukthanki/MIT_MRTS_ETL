import csv

with open("test_csv.csv") as csv_file:

    csv_reader = csv.reader(csv_file, delimiter=",")
    for row in csv_reader:
        print(row)