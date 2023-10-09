import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.common.by import By
# uncomment if using Firefox web browser
import time
from time import sleep

options = webdriver.ChromeOptions()
options.add_argument(r"--user-data-dir=c:\\crawler_google-chrome")
driver = webdriver.Chrome(options=options)


# uncomment if using Phantomjs
#driver = webdriver.PhantomJS()

url = 'https://www.metajob.at/it'
driver.get(url)

# set initial page count
pages = 1
idx = 1

for i in range(10):
    sleep(20)  # grab the Next button if it exists
    btn_next = driver.find_element(By.CLASS_NAME, 'scrollBttRight')
    btn_next.send_keys(Keys.RETURN)

with open('heritageURLs.txt', 'w') as f:
    while True:
    # try:
        # sleep here to allow time for page load
        sleep(20)           # grab the Next button if it exists
        btn_next = driver.find_element(By.CLASS_NAME,'scrollBttRight')
        # find all item-title a href and write to file
        # links = driver.find_elements(By.CLASS_NAME,'rTitle')
        links = driver.find_elements(By.CLASS_NAME,'resultUrl')
        print ("Page: {} -- {} urls to write...".format(pages, len(links)))
        for link in links:
            f.write(link.get_attribute("href")+'\n')
            text = requests.get(link.get_attribute("href"))
            with open(f'C:/Users/karam/PycharmProjects/skillExtraction/metajob/newCrawling/jobpost_{idx}.txt', 'w',encoding='utf-8') as ft:
                ft.write(text.text)
            idx+=1
        # Exit if no more Next button is found, ie. last page
        if btn_next is None:
            print ("crawling completed.")
            exit(-1)
        # otherwise click the Next button and repeat crawling the urls
        pages += 1
        btn_next.send_keys(Keys.RETURN)
    # you should specify the exception here
    # except:
    #     print ("Error found, crawling stopped")
    #     exit(-1)
