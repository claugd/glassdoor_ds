#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 14:19:01 2022

@author: claudia
"""

import pandas as pd
from datetime import date

df = pd.read_csv("glassdoor_jobs.csv")

#salary parsing
df = df[df ['Salary Estimate']!= '-1']

#na is filled with empty string to avoid missing data problems
df['Salary Estimate'] = df ['Salary Estimate'].fillna("")

## Indicator of Salary Data source and time reference
df ['per_hour'] = df ['Salary Estimate'].apply(lambda x: 1 if 'per hour' in x.lower() else 0)
df ['employer_estimate'] = df ['Salary Estimate'].apply(lambda x: 1 if 'employer est.' in x.lower() else 0)
df ['glassdoor_estimate'] = df ['Salary Estimate'].apply(lambda x: 1 if 'glassdoor est.' in x.lower() else 0)


## Salaty Data Cleaning
salary = df['Salary Estimate'].apply(lambda x: x.split('(')[0])

cut_chars = df['Salary Estimate'].apply(lambda x: x.replace('K',"")
                                                      .replace('$',"")
                                                      .replace('(',"")
                                                      .replace(')',""))

cut_strings = cut_chars.apply(lambda x: x.lower().replace('per hour',"")
                                                             .replace('employer est.',"") 
                                                             .replace('glassdoor est.',""))


df ['min_salary'] = cut_strings.apply(lambda x: x if x=="" 
                                                  else x.split("-")[0])

df ['max_salary'] = cut_strings.apply(lambda x: x if len(x.split("-")) < 2  
                                                  else  (x.split("-")[1].replace(" ","")) )                                        


df ['min_salary'] = df["min_salary"].apply(lambda x : int(x) if x!="" else 0 )
df ['max_salary'] = df["max_salary"].apply(lambda x : int(x) if x!="" else 0 )

df['mean_salary'] = (df.min_salary + df.max_salary) / 2

## split city and state
df ['job_state'] = df['Location'].apply(lambda x: "" if pd.isna(x) else 
                                                  "" if (len(x.split(",")) < 2) else 
                                                  x.split(",")[1])

#Company age calculation
df['company_age'] = df['Founded'].apply(lambda x: -1 if x == '-1' or pd.isna(x) else
                                                   date.today().year - int(x)  if x.isnumeric() else -1)


## Parsing Job Description

df['python_skill'] = df['Job Description'].apply(lambda x: 1 if 'python' in x.lower() else 0)
df['spark_skill']        = df['Job Description'].apply(lambda x: 1 if 'spark' in x.lower() else 0)
df['aws_skill']          = df['Job Description'].apply(lambda x: 1 if 'aws' in x.lower() else 0)
df['excel_skill']        = df['Job Description'].apply(lambda x: 1 if 'excel' in x.lower() else 0)

# Fill NA with blank or -1
df['Job Title'] = df ['Job Title'].fillna("")
df['Rating'] = df ['Salary Estimate'].fillna(-1)
df['Location'] = df ['Location'].fillna("")

df.to_csv("data_cleaned.csv",index = False)


