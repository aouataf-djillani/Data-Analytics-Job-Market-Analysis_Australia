from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
import pandas as pd
from selenium.webdriver.common.by import By
import local_settings as l

driver_path = '/home/aouataf/Documents/chromedriver'
driver = webdriver.Chrome(executable_path=driver_path)
#Maximizing browser window to avoid hidden elements
driver.set_window_size(1024, 600)
driver.maximize_window()

## Opening linkedin website
driver.get('https://www.linkedin.com/login')
## waiting load
time.sleep(2)

## Search for login and password inputs, send credentions 
driver.find_element_by_id('username').send_keys(l.MAIL)
driver.find_element_by_id('password').send_keys(l.PASSWORD)
driver.find_element_by_id('password').send_keys(Keys.RETURN)

## getting the search webpage
driver.get(f"https://www.linkedin.com/jobs/search/?geoId=101452733&keywords=data%20analyst&location=Australia&originalSubdomain=fr")
## wait while loading
time.sleep(3)
## creating lists for different job information 
job_id= []
job_title = []
company_name = []
city = []
region=[]
country=[]
date = []
job_link = []
jd = []
seniority = []
emp_type = []
industries = []
skills=[]



## get job list from every page 
for i in range(1,40):
    ## scroll down pages 
    driver.find_element_by_xpath(f'//button[@aria-label="Page {i}"]').click()
    ## job list
    jobs_lists = driver.find_element_by_class_name('jobs-search-results__list') #here we create a list with jobs
    jobs = jobs_lists.find_elements_by_class_name('jobs-search-results__list-item')#here we select each job to count
    # date 
    date1 = driver.find_elements(By.XPATH,f'/html/body/div[7]/div[3]/div[3]/div[2]/div/section[1]/div/div/ul/li/div/div/ul/li/time')
    for el in date1:
        date.append(el.get_attribute("datetime"))
    ## waite while loading
    time.sleep(2) 
    ## get information for every job in the list 
    for job in range (1, len(jobs)+1):
        driver.switch_to.window(driver.window_handles[0])
        ## job click
        driver.find_element_by_xpath(f'/html/body/div[7]/div[3]/div[3]/div[2]/div/section[1]/div/div/ul/li[{job}]/div/div/div/div/a').click()            
        time.sleep(2)       
        job_func1=[]
        industries1=[]
        skills2=[]

        # job title  /html/body/div[7]/div[3]/div[3]/div[2]/div/section[2]/div/div/div[1]/div/div[1]/div/div[2]/a/h2
        job_title1 = driver.find_element(By.XPATH,"/html/body/div[7]/div[3]/div[3]/div[2]/div/section[2]/div/div/div[1]/div/div[1]/div/div[2]/a/h2").get_attribute("innerText")
        job_title.append(job_title1)
        # Company name 
        company_name1= driver.find_element(By.CSS_SELECTOR,".jobs-unified-top-card__company-name").get_attribute("innerText")
        company_name.append(company_name1)
        # location: seperate into city, region and country 
        location1 = driver.find_element(By.CSS_SELECTOR,".jobs-unified-top-card__subtitle-primary-grouping > span:nth-child(2)").get_attribute("innerText").split(",")
        if len(location1)==3: 
            city.append(location1[0])
            region.append(location1[1])
            country.append(location1[2])
        elif len(location1)==2:
            city.append("n/a")
            region.append(location1[0])
            country.append(location1[1])
        else:
            city.append("n/a")
            region.append("n/a")
            country.append(location1[0])
        
        #job link
        job_link1 = driver.find_element(By.CSS_SELECTOR,'a').get_attribute('href')
        job_link.append(job_link1)
        #Employment type / seniority 
        time.sleep(2) 
        emp_type_path = "/html/body/div[7]/div[3]/div[3]/div[2]/div/section[2]/div/div/div[1]/div/div[1]/div/div[2]/div[2]/ul/li[1]/span"
        emp_type1 = driver.find_element(By.XPATH, emp_type_path).get_attribute("innerText")
        emp_type.append(emp_type1)
        
        # Industries

        industries_path = "/html/body/div[7]/div[3]/div[3]/div[2]/div/section[2]/div/div/div[1]/div/div[1]/div/div[2]/div[2]/ul/li[2]/span"
        industries_elements = driver.find_elements(By.XPATH,industries_path)
        for element in industries_elements:
            industries1.append(element.get_attribute("innerText"))
            industries_final = " ".join(industries1)
            industries.append(industries_final)
        
        
        #skills                            
        skills1= driver.find_elements(By.CSS_SELECTOR,".jobs-description__content")

        for skill in skills1:
            
            skills2.append(skill.text)
            skills_final=" ".join(skills2)
            skills.append( skills_final)





jobs = {
'Date': date,
'Company': company_name,
'Title': job_title,
'City': city,
'Region': region,
'Country':country,
'Level': seniority,
'Type': emp_type,
'Requirements': skills,
'Industry': industries,
'Link': job_link
}
data = pd.DataFrame.from_dict(jobs, orient='index')
data= data.transpose()
# remove comma 


#save dataframe to excel
data.to_excel('/home/aouataf/Documents/linkedinJobs/data/DataAnalystJobs.xlsx', index = False)  
print("data successfully stored ") 

