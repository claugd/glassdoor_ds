#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 11:12:51 2022

@author: claudia
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split
import statsmodels.api as sm


df = pd.read_csv("eda_output.csv")

# choose relevant columns
df.columns

df_model = df[["mean_salary","Rating","Type of ownership","Size","Industry","Sector",
                 "Revenue","per_hour","job_state","job_categories", "spark_skill",
                 "excel_skill", "aws_skill","python_skill","job_seniority","description_lenght"]]


# get dummy data
df_dummy = pd.get_dummies(df_model)

# train test split
X = df_dummy.drop("mean_salary",axis=1)
y = df_dummy.mean_salary.values

X_train,X_test,y_train,y_test = train_test_split(X,y,test_size = 0.2, random_state=42)

# multiple linear regression
X_sm = X = sm.add_constant(X)
#model = sm.OLS(y,X_sm)


model.fit().summary()

# lasso regression
# random forest
# tune models GridsearchCV
# test ensembles


 