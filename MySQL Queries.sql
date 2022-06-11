-- query1
SELECT DATE_FORMAT(period, "%d-%m-%Y"), SUM(`value`) AS sales FROM mrts
WHERE kind_of_business = "Retail and food services sales, total"
GROUP BY 1;

-- query2
SELECT SUM(`value`) FROM mrts WHERE period = "2008-03-01";

-- query3
SELECT `value` FROM mrts WHERE kind_of_business = "Health and personal care stores" AND period = "2015-06-01";

-- query4
SELECT `value`, period FROM mrts WHERE kind_of_business = "Retail and food services sales, total" ORDER BY period;

-- query5
SELECT SUM(`value`), YEAR(period) FROM mrts WHERE kind_of_business = "Retail and food services sales, total" GROUP BY 2 ORDER BY period;

-- query 6
SELECT SUM(`value`), period FROM mrts WHERE kind_of_business = 'Book stores' GROUP BY period ORDER BY period;
SELECT SUM(`value`), YEAR(period) FROM mrts WHERE kind_of_business = 'Book stores' GROUP BY YEAR(period) ORDER BY period;

SELECT SUM(`value`), period FROM mrts WHERE kind_of_business = 'Sporting goods stores' GROUP BY period ORDER BY period;
SELECT SUM(`value`), YEAR(period) FROM mrts WHERE kind_of_business = 'Sporting goods stores' GROUP BY YEAR(period) ORDER BY period;

SELECT SUM(`value`), period FROM mrts WHERE kind_of_business = 'Hobby, toy, and game stores' GROUP BY period ORDER BY period;
SELECT SUM(`value`), YEAR(period) FROM mrts WHERE kind_of_business = 'Hobby, toy, and game stores' GROUP BY YEAR(period) ORDER BY period;

-- query 8
SELECT `value`, YEAR(period) FROM mrts WHERE kind_of_business = "Men's clothing stores" GROUP BY YEAR(period) ORDER BY period;

-- query 9
SELECT * FROM mrts WHERE kind_of_business = "New car dealers" AND YEAR(period) = "2020";
SELECT period, SUM(`value`) OVER(ORDER BY period) AS rolling_sum FROM mrts WHERE kind_of_business = "New car dealers" AND YEAR(period) = "2020";

SELECT period, AVG(`value`) OVER(ORDER BY period ROWS BETWEEN 5 PRECEDING AND CURRENT ROW) AS rolling_average FROM mrts WHERE kind_of_business = "Gasoline stations" and period BETWEEN "2000-01-01" and "2008-12-01";

-- General
SELECT kind_of_business, SUM(`value`) AS total_sales FROM mrts GROUP BY kind_of_business ORDER BY `value` DESC;