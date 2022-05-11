
-- Top cities locations for data analyst jobs
SELECT 
    city, COUNT(*) as job_offers
FROM
    job_postings
WHERE
    city != ''
GROUP BY City
ORDER BY COUNT(*) DESC;

-- Industries where Data analysts are in demand

SELECT 
    Industry, COUNT(Industry) AS num_postings
FROM
    job_postings
GROUP BY Industry
ORDER BY num_postings DESC
LIMIT 15;  

-- A function that takes a city as a parameter and returns the top hiring company
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

select f_top_company_by_city(' Melbourne') as Top_hiring_company;

-- inner join on cities and companies to see in which cities every company is hiring 

select  distinct t2.Company, if (t1.City='', 'N/A',  t1.City) as Hiring_cities
from job_postings t1
inner join job_postings t2
where t1.Company= t2.company
and t1.city!= t2.city
order by t2.company;

-- Number of job postings by experience level
select if (Level="", "Not specified",Level) as Experience_level, count(Level) as num_postings
from job_postings
group by Level;

-- Top companies that hire juniors
SELECT 
    Company, COUNT(Company) AS Hiring_company
FROM
    job_postings
WHERE
    Level LIKE '%Entry%'
GROUP BY Company
ORDER BY COUNT(Company) DESC
LIMIT 10;

-- Top cities where entry level jobs are available
select if(City = "" ," Remote", City) as City, count(Level) as entry_level_jobs
from job_postings
group by Level, City
having Level LIKE '%Entry%'
order by count(Level) desc 
; 

-- In demand Data Visualization tools 
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

-- jobs by industry by company 

SELECT 
    Industry, Company, COUNT(Industry) AS num_postings
FROM
    job_postings
GROUP BY Industry , Company
ORDER BY num_postings DESC
;  


-- R vs Python vs SQL vs Nosql 

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

-- most popular job titles
SELECT 
    Title, COUNT(Title)
FROM
    job_postings
GROUP BY title
ORDER BY COUNT(Title) DESC
LIMIT 15;



