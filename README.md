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

In this project, we explored the Monthly Retail Trade Survey (MRTS) data set for the years 1992-2020 and perform an Extract-Transformation-Load (ETL) process through a variety of steps. We then analyzed the data for trends, percentage changes, as well as rolling time windows paired with visualization for enhanced understanding of the data.

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

I saw this as an opportunity to be more efficient with my code by creating a function

| ![image](https://github.com/ukthanki/MIT_House_Price_Prediction_Project/assets/42117481/809779b0-251f-41d9-bbee-21ad7f6c7746)| 
|:--:| 
| **Figure 1.** Null entry counts in each field in the original dataset. |

**You can view the full Project in the "module_8.py" and "Module 8_Umang_Thanki.ipynb" files in the Repository.**

