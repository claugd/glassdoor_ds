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
    
    #Buttons to click. Jobs from the first search page 
    job_buttons = driver.find_elements_by_class_name("react-job-listing") 
    if verbose: 
        print ("Len of Job Buttons", len(job_buttons))
   
    # This first click makes glassdoor window to show up
    job_buttons[0].click() 
    
    time.sleep(2)
    try : 
         ## Close initial pop up window   
         driver.find_element_by_class_name('SVGInline-svg.modal_closeIcon-svg').click()
    except NoSuchElementException:
         pass
     
    #next_page_pointer points to the page to scrap, each page 30 jobs
    next_page_pointer = 2
    
    while len(jobs) < num_jobs:  #If true, should be still looking for new jobs.
        
     
        #Let the page load. Change this number based on your internet speed.
        time.sleep(slp_time)
            
        #Going through each job in this page
        scrap_glassdoor_page(driver, jobs, job_buttons,num_jobs,verbose)
        
      
        try:
                    
            #proceed to "next page" search results 
            #compares with 5 because the xpath button number changes 
            #when button[5] is clicked, it assume position of button[4] after reload 
            if next_page_pointer < 5 :
                next_page_pointer += 1
            if verbose: 
                print("page num",next_page_pointer)
                
            driver.find_element_by_xpath('//*[@id="MainCol"]/div[2]/div/div[1]/button['+str(next_page_pointer)+']').click()
            time.sleep(2)
                                 
            job_buttons = driver.find_elements_by_class_name("react-job-listing") 
            
        except NoSuchElementException:
            print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_jobs, len(jobs)))
            break

    return pd.DataFrame(jobs)  #This line converts the dictionary object into a pandas DataFrame.


def scrap_glassdoor_page(driver, jobs, job_buttons,num_jobs,verbose):
    
    page_position = 0
    
    for job_button in job_buttons:  
        
        page_position += 1
        
        if len(jobs) >= num_jobs :
            return
        
        if verbose:
            print("Progress: {}".format("" + str(len(jobs)) + "/" + str(len(job_buttons))))        
        
             
        job = scrap_glassdoor_job(driver,job_button, page_position,verbose)       
    
                   
        jobs.append(job)
        
    return 


def scrap_glassdoor_job(driver,job_button,page_position,verbose) : 
    
    job_button.click()
    time.sleep(5)
                
    srt_page_position = str(page_position)
              
    job_title = try_catch_find_by_xpath(driver,'//*[@id="MainCol"]/div[1]/ul/li['+srt_page_position+']/div[2]/a/span')
    
    company_name = try_catch_find_by_xpath(driver,'//*[@id="MainCol"]/div[1]/ul/li['+srt_page_position+']/div[2]/div[1]/a/span')
    if verbose:
        print("Company Name: {}".format(company_name))

    location = try_catch_find_by_xpath(driver,'//*[@id="MainCol"]/div[1]/ul/li['+srt_page_position+']/div[2]/div[2]/span')
    if verbose:
        print("Location: {}".format(location))
    
          
    job_description = try_catch_find_by_xpath(driver,'.//div[@class="jobDescriptionContent desc"]')
   
    salary_estimate = try_catch_find_by_xpath(driver,'//*[@id="MainCol"]/div[1]/ul/li['+srt_page_position+']/div[2]/div[3]/div[1]/span')
    if verbose:
        print("Salary: {}".format(salary_estimate))         
        
    rating = try_catch_find_by_xpath(driver,'//*[@id="MainCol"]/div[1]/ul/li['+srt_page_position+']/div[1]/span')
           
    size = try_catch_find_by_xpath(driver,'//*[@id="EmpBasicInfo"]/div[1]/div/div[1]/span[2]')
       
    founded = try_catch_find_by_xpath(driver,'//*[@id="EmpBasicInfo"]/div[1]/div/div[2]/span[2]')
    
    type_of_ownership = try_catch_find_by_xpath(driver,'//*[@id="EmpBasicInfo"]/div[1]/div/div[3]/span[2]')
    
    industry = try_catch_find_by_xpath(driver,'//*[@id="EmpBasicInfo"]/div[1]/div/div[4]/span[2]')
        
    sector = try_catch_find_by_xpath(driver, '//*[@id="EmpBasicInfo"]/div[1]/div/div[4]/span[2]')
  
    revenue = try_catch_find_by_xpath(driver,'//*[@id="EmpBasicInfo"]/div[1]/div/div[6]/span[2]')
  
    job = {"Job Title" : job_title,
    "Salary Estimate" : salary_estimate,
    "Job Description" : job_description,
    "Rating" : rating,
    "Company Name" : company_name,
    "Location" : location,
    "Size" : size,
    "Founded" : founded,
    "Type of ownership" : type_of_ownership,
    "Industry" : industry,
    "Sector" : sector,
    "Revenue" : revenue}
    
    return job

def try_catch_find_by_xpath(driver, str_xpath):
    try: 
        element = driver.find_element_by_xpath(str_xpath).text 
    except NoSuchElementException:
        element = -1
    return element
    