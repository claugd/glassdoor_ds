# Data Science Salary Estimator: Project Overview 
* Created a tool that estimates data science salaries (MAE ~ $ 11K) to help data scientists negotiate their income when they get a job.
* Scraped over 1000 job descriptions from glassdoor using python and selenium
* Engineered features from the text of each job description to quantify the value companies put on python, excel, aws, and spark. 

## Code and Resources Used 
**Python Version:** 3.7  
**Packages:** pandas, numpy, sklearn, matplotlib, seaborn, selenium, flask, json, pickle  
**Scraper Github:** https://github.com/arapfaik/scraping-glassdoor-selenium  
**Scraper Article:** https://towardsdatascience.com/selenium-tutorial-scraping-glassdoor-com-in-10-minutes-3d0915c6d905  

## Web Scraping
Used the web scraper github repo (above) as a rerefence to scrape 1000 job postings from glassdoor.com. 
The scrapper script was dated from 2019, so I adjusted it to work accoding to the most recent changes in Glassdoor website structure.
Besides, I applied some concepts of clean code to make the code more clean and readable.

With each job, we got the following:
*	Job title
*	Salary Estimate
*	Job Description
*	Rating
*	Company 
*	Location
*	Company Headquarters 
*	Company Size
*	Company Founded Date
*	Type of Ownership 
*	Industry
*	Sector
*	Revenue

## Data Cleaning
After scraping the data, I needed to clean it up so that it was usable for our model. I made the following changes and created the following variables:

*	Parsed numeric data out of salary, creating the columns representing:inferior limit salary, superior limit salary and avarage salary
*	Made columns for employer provided salary and hourly wages 
*	Removed rows without salary 
*	Made a new column for company state 
*	Transformed founded date into age of company 
*	Made columns for if different skills were listed in the job description:
    * Python  
    * R  
    * Excel  
    * AWS  
    * Spark 
*	Column for Job Categories and Job Seniority 
*	Column for description length 

## EDA
I looked at the distributions of the data and the value counts for the various categorical variables. Below are a few highlights from the pivot tables. 


## Model Building 
Under construction... 
Nice have you here! 
Welcome back soon!
