#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 28 18:49:50 2022

@author: claudia
"""

from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
import time
import pandas as pd

def get_jobs(keyword, num_jobs, verbose, path, slp_time):
    
      
    #Initializing the webdriver
   
    options = webdriver.ChromeOptions()

    #Uncomment the line below if you'd like to scrape without a new Chrome window every time.
    #options.add_argument('headless')
       
    driver = webdriver.Chrome(executable_path =path, options=options)
    driver.set_window_size(1120, 1000)

    url = "https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword="+keyword+"&sc.keyword="+keyword+"&locT=&locId=&jobType="
    driver.get(url)
    jobs = []
    
    job_buttons = driver.find_elements_by_class_name("react-job-listing") 
    
    print ("Len of Job Buttons", len(job_buttons))
   
    # This first click is to cause the glassdoor window to show up
    job_buttons[0].click()  #You might 
    
    ## Close pop up window   
    time.sleep(2)
    try : 
         driver.find_element_by_class_name('SVGInline-svg.modal_closeIcon-svg').click() #clicking to the X.
    except NoSuchElementException:
         pass
     
    page = 2
    
    while len(jobs) < num_jobs:  #If true, should be still looking for new jobs.
        
     
        #Let the page load. Change this number based on your internet speed.
        #Or, wait until the webpage is loaded, instead of hardcoding it.
        time.sleep(slp_time)
        
        
        #time.sleep(1)
        
        #Going through each job in this page
        #jl for Job Listing. These are the buttons we're going to click.
        scrap_glassdoor_page(driver, jobs, job_buttons)
        
        #Clicking on the "next page" button
        try:
            page += 1
        
            driver.find_element_by_xpath('//*[@id="MainCol"]/div[2]/div/div[1]/button['+str(page)+']').click()
            job_buttons = driver.find_elements_by_class_name("react-job-listing") 
            
        except NoSuchElementException:
            print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_jobs, len(jobs)))
            break

    return pd.DataFrame(jobs)  #This line converts the dictionary object into a pandas DataFrame.

def scrap_glassdoor_page(driver, jobs, job_buttons):
    
    num_page = 0
    
    for job_button in job_buttons:  
        
        #if len(jobs) >= len(job_buttons):
        #    return
        
        print("Progress: {}".format("" + str(len(jobs)) + "/" + str(len(job_buttons))))        
        
        time.sleep(1)
        
        collected_successfully = False
        
        while not collected_successfully:
            
            try:
              
                  print("collected success", len(jobs))
                  
                  num_page += 1
                  page_position = str(num_page)
              
                  company_name = driver.find_element_by_xpath('//*[@id="MainCol"]/div[1]/ul/li['+page_position+']/div[2]/div[1]/a/span').text
                  print("Company Name: {}".format(company_name))
            
                  location = driver.find_element_by_xpath('//*[@id="MainCol"]/div[1]/ul/li['+page_position+']/div[2]/div[2]/span').text
                  print("Location: {}".format(location))
                  #job_title = driver.find_element_by_xpath('.//div[contains(@class, "title")]').text
                  
                  job_title = driver.find_element_by_xpath('//*[@id="MainCol"]/div[1]/ul/li['+page_position+']/div[2]/a/span').text
                  
                                     
                  #data_id = driver.find_element_by_class_name("react-job-listing").get_attribute('data-id')
                  #job_description = driver.find_element_by_xpath('//*[@id="JobDesc+'+data_id+']/div').text
                  #job_description = driver.find_element_by_xpath('.//div[@class="jobDescriptionContent desc"]').text
    
                  collected_successfully = True
            except:
                 time.sleep(5)

            try:
                
                  salary_estimate = driver.find_element_by_xpath('//*[@id="MainCol"]/div[1]/ul/li['+page_position+']/div[2]/div[3]/div[1]/span/text()').text
                    
                  #salary_estimate = driver.find_element_by_xpath('//*[@id="MainCol"]/div[1]/ul/li['+page_position+']/div[2]/div[3]/div[1]/span/').text
            except NoSuchElementException:
                  salary_estimate = -1 #You need to set a "not found value. It's important."
            
            print("Salary: {}".format(salary_estimate))         
            
            try:
                              
                  rating = driver.find_element_by_xpath('//*[@id="employerStats"]/div[1]/div[1]').text
            except NoSuchElementException:
                  rating = -1 #You need to set a "not found value. It's important."
        
              
            #Going to the Company tab...
            #clicking on this:
            #<div class="tab" data-tab-type="overview"><span>Company</span></div>
            try:
                  driver.find_element_by_xpath('//*[@id="MainCol"]/div[1]/ul/li['+page_position+']').click()
            except NoSuchElementException:
                 size = -1
                 founded = -1
                 type_of_ownership = -1
                 industry = -1
                 sector = -1
                 revenue = -1
                   
             
            try:
                  size = driver.find_element_by_xpath('//*[@id="EmpBasicInfo"]/div[1]/div/div[1]/span[2]').text
            except NoSuchElementException:
                  size = -1
        
            try:
                 founded = driver.find_element_by_xpath('//*[@id="EmpBasicInfo"]/div[1]/div/div[2]/span[2]').text
            except NoSuchElementException:
                      founded = -1
        
            try:
                      type_of_ownership = driver.find_element_by_xpath('//*[@id="EmpBasicInfo"]/div[1]/div/div[3]/span[2]').text
            except NoSuchElementException:
                      type_of_ownership = -1
        
            try:
                      industry = driver.find_element_by_xpath('//*[@id="EmpBasicInfo"]/div[1]/div/div[4]/span[2]').text
            except NoSuchElementException:
                      industry = -1
        
            try:
                      sector = driver.find_element_by_xpath('//*[@id="EmpBasicInfo"]/div[1]/div/div[4]/span[2]').text
            except NoSuchElementException:
                      sector = -1
        
            try:
                      revenue = driver.find_element_by_xpath('//*[@id="EmpBasicInfo"]/div[1]/div/div[6]/span[2]').text
            except NoSuchElementException:
                      revenue = -1
        
               
        jobs.append({"Job Title" : job_title,
        "Salary Estimate" : salary_estimate,
        #"Job Description" : job_description,
        "Rating" : rating,
        "Company Name" : company_name,
        "Location" : location,
        #"Headquarters" : headquarters,
        "Size" : size,
        "Founded" : founded,
        "Type of ownership" : type_of_ownership,
        "Industry" : industry,
        "Sector" : sector,
        "Revenue" : revenue})
        #add job to jobs
        
    return 