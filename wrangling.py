import pandas as pd 
import numpy as np 
import re 

def clean(file):

    data= pd.read_excel(file, delimiter=",")
    
    # Remove Commas, semi-colons and line breaks
    patterns=[
                    '\n',
                    ';',
                    ',',
                    ]

    data= data.replace( [e for e in patterns] , ' ', regex=True)
    # remove irrelevent data from industry column 
    data['Industry'] = data['Industry'].str.replace("^(.+?)·",'',regex=True)
    # delete salary information from type: $15.50/hr - $17/hr 
    data['Type']=data['Type'].str.replace("\$.+?·", "",regex=True)

    # move job level information from type to level column : [Full-time . associate] ==> [full-time] [associate]
    #level column 
    data[['Type', 'Level']] = data['Type'].str.split('·', 1, expand=True)
    

    #save to excel

    output="/home/aouataf/Documents/linkedinJobs/DataAnalystJobs_clean.xlsx"
    data.to_excel(output)
    return f"data saved to {output}"

dataFile='/home/aouataf/Documents/linkedinJobs/DataAnalystJobs.xlsx'
print(clean(dataFile))