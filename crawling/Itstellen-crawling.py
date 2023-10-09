import requests
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome() # to open a browser automatically to run a webpage

# uncomment if using Phantomjs
#driver = webdriver.PhantomJS()

url = "https://www.itstellen.at/jobs"
driver.get(url)

# Wait for the page to load
# WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'm-jobsList')))

# Loop through each page until there are no more job links
#page_number = 1
page_number = 110
idx = 1
while True:
    print(f"Scraping page {page_number}")

    # Find all the job links on the current page
    job_links = driver.find_elements(By.XPATH,'//a[@data-event-name="link-job-detail"]')


    # If there are no more job links, break out of the loop
    if len(job_links) == 0:
        break

    # Loop through each job link and write the job content to a file
    for job_link in job_links:
        # Get the URL of the job
        job_url = job_link.get_attribute('href')

        # Navigate to the job page
        driver.get(job_url)

        # Wait for the job content to load
        try:
            job_content = driver.find_element(By.CLASS_NAME, 'm-jobContent__jobDetail').text
        except NoSuchElementException:
            job_content = driver.find_element(By.CLASS_NAME, 'content').text

        # Write the job content to a file

        #with open(f'C:/Users/karam/PycharmProjects/skillExtraction/itstellen/itstellen_{idx}.txt', 'a', encoding='utf-8') as file:
        with open(f'C:/Users/karam/PycharmProjects/skillExtraction/metajob/jobPost_{idx}.txt', 'a', encoding='utf-8') as file:
            file.write(job_content + '\n\n')
        idx += 1
        # Go back to the main page
        driver.back()

    # Go to the next page
    page_number += 1
    driver.get(f"https://www.itstellen.at/jobs?keywords=&locations=&page={page_number}")

# Close the webdriver
driver.quit()
