#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 28 18:52:23 2022

@author: claudia
"""
path = './chromedriver'

import glassdoor_scraper as gs

df = gs.get_jobs("data scientist", 1000, True, path, 7)

df.to_csv('glassdoor_jobs.csv', index = False)


