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
        
       
      
        #Going through each job in this page
        #jl for Job Listing. These are the buttons we're going to click.
        scrap_glassdoor_page(driver, jobs, job_buttons,num_jobs)
        
        #proceed to "next page" results 
        try:
            page += 1
        
            driver.find_element_by_xpath('//*[@id="MainCol"]/div[2]/div/div[1]/button['+str(page)+']').click()
            time.sleep(2)
            job_buttons = driver.find_elements_by_class_name("react-job-listing") 
            
        except NoSuchElementException:
            print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_jobs, len(jobs)))
            break

    return pd.DataFrame(jobs)  #This line converts the dictionary object into a pandas DataFrame.


def scrap_glassdoor_page(driver, jobs, job_buttons,num_jobs):
    
    page_position = 0
    
    for job_button in job_buttons:  
        
        if len(jobs) >= num_jobs :
            return
        
        print("Progress: {}".format("" + str(len(jobs)) + "/" + str(len(job_buttons))))        
        
        job_button.click()
        
        time.sleep(2)

               
        try:
              
                  print("collected success", len(jobs))
                 
                  page_position += 1
                  srt_page_position = str(page_position)
                  
                  company_name = driver.find_element_by_xpath('//*[@id="MainCol"]/div[1]/ul/li['+srt_page_position+']/div[2]/div[1]/a/span').text
                  print("Company Name: {}".format(company_name))
            
                  location = driver.find_element_by_xpath('//*[@id="MainCol"]/div[1]/ul/li['+srt_page_position+']/div[2]/div[2]/span').text
                  print("Location: {}".format(location))
                               
                  job_title = driver.find_element_by_xpath('//*[@id="MainCol"]/div[1]/ul/li['+srt_page_position+']/div[2]/a/span').text
                  
                                    
                  job_description = driver.find_element_by_xpath('.//div[@class="jobDescriptionContent desc"]').text
    
        except:
                  time.sleep(5)

        try:
                salary_estimate = driver.find_element_by_xpath('//*[@id="MainCol"]/div[1]/ul/li['+srt_page_position+']/div[2]/div[3]/div[1]/span').text
                   
        except NoSuchElementException:
                  salary_estimate = -1 #You need to set a "not found value. It's important."
            
        print("Salary: {}".format(salary_estimate))         
            
        try:
                              
                  rating = driver.find_element_by_xpath('//*[@id="MainCol"]/div[1]/ul/li['+srt_page_position+']/div[1]/span').text
        except NoSuchElementException:
                  rating = -1 #You need to set a "not found value. It's important."
        
                      
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
        "Job Description" : job_description,
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
