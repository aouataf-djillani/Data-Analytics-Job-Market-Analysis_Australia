from os import lseek
from selenium import webdriver
import time
import pandas as pd
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
url="https://au.linkedin.com/jobs/data-analyst-jobs?position=1&pageNum=0"
#url="https://www.linkedin.com/jobs/search?keywords=Computational%20Linguist&location=Australia&locationId=&geoId=101452733&f_TPR=r604800&position=1&pageNum=0"
options = Options()
#options.add_argument("--headless")
options.add_argument("window-size=1400,1500")
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("excludeSwitches",["enable-automation"])
driver = webdriver.Chrome(options=options)
driver.get(url)
time.sleep(2)
screen_height = driver.execute_script("return window.screen.height;")
no_of_jobs = int(driver.find_element(By.CSS_SELECTOR,'h1>span').get_attribute('innerText')[:-1].replace(",",""))
i = 2
while i <= 50:
    driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
    #driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    i = i + 1
    time.sleep(1)
    scroll_height = driver.execute_script("return document.body.scrollHeight;")  
    try:
        driver.find_element(By.XPATH,"/html/body/div/div/main/section/button").click()
        time.sleep(1)
    except:
        pass
        time.sleep(1)
job_lists = driver.find_element(By.CLASS_NAME,"jobs-search__results-list")
jobs = job_lists.find_elements(By.TAG_NAME,"li")
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
job_func = []
industries = []
skills=[]
for job in jobs:
    # job id 
    job_id1 = job.find_element(By.CSS_SELECTOR,'div').get_attribute('data-row')
    job_id.append(job_id1)
    
    # job title 
    job_title1 = job.find_element(By.CSS_SELECTOR,"h3").get_attribute("innerText")
    job_title.append(job_title1)
    # Company name 
    company_name1= job.find_element(By.CSS_SELECTOR,"h4").get_attribute("innerText")
    company_name.append(company_name1)
    # location: seperate into city, region and country 
    location1 = job.find_element(By.CLASS_NAME,"job-search-card__location").get_attribute("innerText").split(",")
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
    # date 
    date1 = job.find_element(By.CSS_SELECTOR,'div>div>time').get_attribute("datetime")
    date.append(date1)
    #job link
    job_link1 = job.find_element(By.CSS_SELECTOR,'a').get_attribute('href')
    job_link.append(job_link1)


# clicking job to view further job details
for item in range(len(jobs)):
    job_func1=[]
    industries1=[]
    skills2=[]
    time.sleep(5)
    job_click_path = f'//li/div/a[@href]'
    job_click =job.find_element(By.XPATH,job_click_path).click()
    last_height = driver.execute_script('return document.body.scrollHeight')
    #seniority 
    seniority_path = "//ul/li[1]/span"
    seniority1 = job.find_element(By.XPATH,seniority_path).get_attribute("innerText")
    seniority.append(seniority1)
    
    #Employment type
    time.sleep(5) 
    emp_type_path = "/html/body/div[1]/div/section/div[2]/div/section[1]/div/ul/li/span"
    emp_type1 = job.find_element(By.XPATH, emp_type_path).get_attribute("innerText")
    emp_type.append(emp_type1)
    #Job function 
    job_func_path = "//ul/li[3]/span"
    job_func_elements = job.find_elements(By.XPATH,job_func_path)
    for element in job_func_elements:
        job_func1.append(element.get_attribute("innerText"))
        job_func_final = " ".join(job_func1)
        job_func.append(job_func_final)
        # Industries

        industries_path = "/html/body/div[1]/div/section/div[2]/div/section[1]/div/ul/li[4]/span"
        industries_elements = job.find_elements(By.XPATH,industries_path)
    for element in industries_elements:
        industries1.append(element.get_attribute("innerText"))
        industries_final = " ".join(industries1)
        industries.append(industries_final)
    # scroll for more 
    time.sleep(1)
    scroll_height = driver.execute_script("return document.body.scrollHeight;")  
    try:
        job.find_element(By.XPATH,"/html/body/div[1]/div/section/div[2]/div/section[1]/div/div/section/button[1]").click()
        time.sleep(1)
    except:
        pass
        time.sleep(1)
    #skills 
    skills1= job.find_elements(By.XPATH,"/html/body/div[1]/div/section/div[2]/div/section[1]/div/div/section/div/ul[2]")

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
'Function': job_func,
'Requirements': skills,
'Industry': industries,
'Link': job_link
}
data = pd.DataFrame.from_dict(jobs, orient='index')
data= data.transpose()
# cleaning skills column
data['Requirements'] = data['Requirements'].str.replace('\n',' ')
# cleaning Funtion column
data['Function'] = data['Function'].str.replace(',',' ')
data['Function'] = data['Function'].str.replace('and',' ')
data['Industry'] = data['Industry'].str.replace('and',' ')


data.to_excel('DataAnalystJobs2.xlsx', index = False)  
print("data successfully stored ")





    




