#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 28 18:52:23 2022

@author: claudia
"""
path = './chromedriver'

import pandas as pd
import glassdoor_scraper as gs

df = gs.get_jobs("data scientist", 45, False, path, 7)

print(df)


