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
from sklearn.linear_model import LinearRegression, Lasso
from sklearn.model_selection import cross_val_score

df = pd.read_csv("eda_output.csv")
df.isna().sum()
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
model = sm.OLS(y,X_sm)
model.fit().summary()

lm = LinearRegression()
lm.fit(X_train,y_train)

np.mean(cross_val_score(lm,X_train,y_train,scoring="neg_mean_absolute_error",cv=3))

# lasso regression
lm_l = Lasso()
lm_l.fit(X_train,y_train)
np.mean(cross_val_score(lm_l,X_train,y_train,scoring="neg_mean_absolute_error",cv=3))

alpha = []
error = []

for i in range (1,100):
    alpha.append(i/10)
    lml = Lasso(alpha = (i/10))
    error.append (np.mean(cross_val_score(lml,X_train,y_train,scoring="neg_mean_absolute_error",cv=3)))

plt.plot(alpha,error)
err = tuple (zip(alpha,error))
df_err = pd.DataFrame(err,columns = ['alpha',"error"])
df_err[df_err.error== max(df_err.error)]

# random forest
from sklearn.ensemble import RandomForestRegressor
rf = RandomForestRegressor()

np.mean(cross_val_score(rf,X_train,y_train,scoring = "neg_mean_absolute_error", cv = 3))

# tune models GridsearcCV
from sklearn.model_selection import GridSearchCV

parameters = {"n_estimators":range(10,300,10), "criterion":('mse','mae'),"max_features":('auto','sqrt','log2') }

gs = GridSearchCV(rf,parameters,scoring = "neg_mean_absolute_error", cv = 3)

gs.fit(X_train,y_train)

gs.best_score_
gs.best_estimator_

tpred_lm  = lm.predict (X_test)
tpred_lml = lm_l.predict (X_test)
tpred_rf = gs.best_estimator_.predict(X_test)

from sklearn.metrics import mean_absolute_error

mean_absolute_error(y_test, tpred_lm)
mean_absolute_error(y_test, tpred_lml)
mean_absolute_error(y_test, tpred_rf)

mean_absolute_error(y_test,(tpred_lm+tpred_rf/2))

#rf.get_rams().keys()
# test ensembles


 