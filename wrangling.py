import pandas as pd 
import numpy as np 
import re 
data= pd.read_excel('/home/aouataf/Documents/linkedinJobs/DataAnalystJobs.xlsx', delimiter=",")

# cleaning skills column
patterns=[
                 '\n',
                 '^.*?Expect', 
                 '^.*?Qualifications', 
                 '^.*?Required', 
                 '^.*?expected', 
                 '^.*?Responsibilities', 
                 '^.*?Requirements', 
                 '^.*?QualificationsRequired1', 
                 '^.*?great', 
                 '^.*?Looking For', 
                 '^.*?ll Need', 
                 ]

data['Requirements'] = data['Requirements'].replace( [e for e in patterns] , '', regex=True)
# remove irrelevent data from industry column 
data['Industry'] = data['Industry'].str.replace("^(.+?)·",'',regex=True)

# move level information from jobtype to level column : [Full-time . associate] ==> [full-time] [associate]
#level column
data["Level"]= data['Type'].str.findall("·(.*)$").astype(str)
#jobtype column 
data['Type']= data['Type'].str.findall("^(.+?)·").astype(str)



#save to excel
data.to_excel("/home/aouataf/Documents/linkedinJobs/DataAnalystJobs_clean.xlsx")

