import pandas as pd 
import numpy as np 
import re 

def clean(file):

    data= pd.read_excel(file, delimiter=",")
    
    # cleaning skills column
    patterns=[
                    '\n',
                    ';',
                    ',',
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
                    
    data['Requirements'] = data['Requirements'].replace( [e for e in patterns] , ' ', regex=True)
    # remove irrelevent data from industry column 
    data['Industry'] = data['Industry'].str.replace("^(.+?)·",'',regex=True)
    # delete salary information from type: $15.50/hr - $17/hr 
    data['Type']=data['Type'].str.replace("\$.+?·", "",regex=True)

    # move job level information from type to level column : [Full-time . associate] ==> [full-time] [associate]
    #level column 
    data[['Type', 'Level']] = data['Type'].str.split('·', 1, expand=True)
    # Remove commas 
    data= data.replace(',', ' ', regex= True)


    #save to excel

    output="/home/aouataf/Documents/linkedinJobs/DataAnalystJobs_clean.xlsx"
    data.to_excel(output)
    return f"data saved to {output}"

dataFile='/home/aouataf/Documents/linkedinJobs/DataAnalystJobs.xlsx'
print(clean(dataFile))