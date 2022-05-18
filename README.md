# Analyzing Data Analytics Job Market Trends in Australia      

This analysis of the Australian Data Analytics job market provides some insights on the hiring trends from more than a 1000 Data Analyst job postings on **LinkedIn**
Hopefully, these insights will help me and everyone who visits my repository in the job search process. 
## Insights 
 Our Analysis provides answers to different questions such as: 
 - What are the top Locations where Data Analytics jobs are in demand? 
 - What are the main employers expectations in terms of technical skills? 
 - What are the companies that hire the most in this field? 
 - What are the most popular job titles related to the field? 
 - Where is the best place for a junior profile to apply? 
 - Which industries hire Data Analysts the most ? 


 ![Data Analyst Job Trend in Autralia 2022(1)](https://user-images.githubusercontent.com/54501663/167870887-86c19e2c-921b-4357-a4df-d6dbfdce19a9.png)

  
## Steps

 1. Data Scraping: Extracted over 1000 recent job postings from LinkedIn using **Python** and **Selenium**
 2. Data wrangling : using **Python** and **Regex** to split columns, remove unnecessary elements and handle empty records. 
 3.  Data Querying and exploring: using **mySQL**
 4.  Data visualization: Exporting data and Visualizing it using Tableau public  
## Dataset 
Our data-set contains information  (1000 records) about job offers: City, Company, job title, experience level,  Demographics...etc 
| Date | Company  | Title  | City | Region | Country | Level | Type | Requirements | Industry | Link
|--|--|--|--|--|--|--|--|--|--|--|

## Sample  SQL Queries 
All queries [here.](https://github.com/aouataf-djillani/Data-Analytics-Job-Market-Analysis_Australia/blob/master/source/queries.sql) 

- Top cities locations for data analyst jobs
```sql
SELECT 
    city, COUNT(*) as job_offers
FROM
    job_postings
WHERE
    city != ''
GROUP BY City
ORDER BY COUNT(*) DESC;
```sql
-- Top industries where Data analysts are in demand
```sql
SELECT 
    Industry, COUNT(Industry) AS num_postings
FROM
    job_postings
GROUP BY Industry
ORDER BY num_postings DESC
LIMIT 15;  
```
- A function that takes a city as a parameter and returns the top hiring company
```sql
delimiter $$
create function f_top_company_by_city(p_City text)
returns text 
deterministic reads sql data
begin 
declare v_company text; 
select Company into v_company
from job_postings
where City=p_City 
group by Company 
order by count(Company) desc
limit 1;
return v_company ; 
end $$
delimiter ; 
-- testing the function 
select f_top_company_by_city(' Melbourne') as Top_hiring_company;
```
- Inner join on cities and companies to check if a company is hiring in different cities 
```sql
select  distinct t2.Company, if (t1.City='', 'N/A',  t1.City) as Hiring_cities
from job_postings t1
inner join job_postings t2
where t1.Company= t2.company
and t1.city!= t2.city
order by t2.company;
```
- Number of job postings by experience level
```sql
select if (Level="", "Not specified",Level) as Experience_level, count(Level) as num_postings
from job_postings
group by Level;
```
- Top companies that hire juniors
```sql
SELECT 
    Company, COUNT(Company) AS Hiring_company
FROM
    job_postings
WHERE
    Level LIKE '%Entry%'
GROUP BY Company
ORDER BY COUNT(Company) DESC
LIMIT 10;
```
- Top cities where entry level jobs are available
```sql
select if(City = "" ," Remote", City) as City, count(Level) as entry_level_jobs
from job_postings
group by Level, City
having Level LIKE '%Entry%'
order by count(Level) desc 
; 
```
- In demand Data Visualization tools 
```sql
SELECT 
    CASE
        WHEN Requirements LIKE '%power bi%' THEN 'power bi'
        WHEN Requirements LIKE '%Tableau%' THEN 'Tableau'
        WHEN Requirements LIKE '%QlikView%' THEN 'QlikView'
        WHEN Requirements LIKE '%Plotly%' THEN 'Plotly'
        WHEN Requirements LIKE '%Excel%' THEN 'Excel'
        ELSE 'Not specified'
    END AS Visualization_tools,
    COUNT(*)
FROM
    job_postings
GROUP BY (CASE
    WHEN Requirements LIKE '%power bi%' THEN 'Power Bi'
    WHEN Requirements LIKE '%Tableau%' THEN 'Tableau'
    WHEN Requirements LIKE '%QlikView%' THEN 'QlikView'
    WHEN Requirements LIKE '%Plotly%' THEN 'Plotly'
    WHEN Requirements LIKE '%Excel%' THEN 'Excel'
    ELSE 'not specified'
END);
```
- jobs by industry by company 
```sql
SELECT 
    Industry, Company, COUNT(Industry) AS num_postings
FROM
    job_postings
GROUP BY Industry , Company
ORDER BY num_postings DESC
;  
```
- In-demand programming languages in this field 
```sql
SELECT 
    CASE
        WHEN Requirements LIKE '%Python%' THEN 'Python'
        WHEN Requirements LIKE '% R %' THEN 'R'
        WHEN Requirements LIKE '%sql%' THEN 'sql'
        WHEN Requirements LIKE '%NoSql%' THEN 'NoSql'
        ELSE 'Not specified'
    END AS programming_tools,
    COUNT(*)
FROM
    job_postings
GROUP BY (CASE
    WHEN Requirements LIKE '%Python%' THEN 'Python'
    WHEN Requirements LIKE '% R %' THEN 'R'
    WHEN Requirements LIKE '%sql%' THEN 'sql'
    WHEN Requirements LIKE '%NoSql%' THEN 'NoSql'
    ELSE 'Not specified'
END);
```
- Most popular job titles on LinkedIn 
```sql
SELECT 
    Title, COUNT(Title)
FROM
    job_postings
GROUP BY title
ORDER BY COUNT(Title) DESC
LIMIT 15;
```

