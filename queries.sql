SELECT 
    *
FROM
    jobs_australia.job_postings;
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
LIMIT 10;  

-- Number of job postings by experience level
select if (Level="", "Not specified",Level) as Experience_level, count(Level) as num_postings
from job_postings
group by Level;

-- Top companies that hire juniors
select Company, count(Company) as Hiring_company
from job_postings
where Level LIKE '%Entry%'
group by Company 
order by Count(Company) DESC
limit 10;

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

-- jobs by indeustry by company 

select Industry, Company, count(Industry) as num_postings
from job_postings
group by Industry, Company
order by num_postings DESC
;  


-- R vs Python vs SQL vs Nosql 

select case 
when Requirements like '%Python%' then 'Python' 
when Requirements like '% R %' then 'R'
-- when Requirements like '%sql%' then 'sql'
else 'Not specified' end as programming_tools, count(*)
from job_postings
GROUP BY (case 
when Requirements like '%Python%' then 'Python' 
when Requirements like '% R %' then 'R'
-- when Requirements like '%sql%' then 'sql'
else 'Not specified' end);

-- most popular job titles
select Title, count(Title)
from job_postings

group by title
order by count(Title) desc 
limit 15;


-- which cloud service AWS vs Azure vs Google Cloud vs IBM
