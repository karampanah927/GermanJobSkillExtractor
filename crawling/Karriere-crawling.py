import time
from time import sleep
from pathlib import  Path

#from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from charset_normalizer import detect

from tqdm import tqdm

#create chromeoptions instance
options = webdriver.ChromeOptions()
options.add_argument(r"--user-data-dir=c:\\crawler_google-chrome")
driver = webdriver.Chrome(options=options)

urls = list(Path('C:/Users/karam/PycharmProjects/skillExtraction/karriere/karriereoutput_classes.txt').open("rt").readlines())

do_sleep = True
for url in tqdm(urls):
    url = url.strip()
    if not url: continue
    job_id = url.split('/')[-1]
    out_file = Path(f'C:/Users/karam/PycharmProjects/skillExtraction/karriere/out/{job_id}.txt')
    if out_file.exists(): continue

    if do_sleep:
        time.sleep(5)
    driver.get(url)

    try:
        iframe = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'm-jobContent__iFrame')))
        driver.switch_to.frame(iframe)
        content = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.content')))
        # result = detect(content.text)
        with out_file.open("wt", encoding="utf8") as f:
            f.write(content.text)
        do_sleep = True
    except :
        print("ERROR")
        do_sleep = False

sleep(100)
exit(0)

# Read HTML content from file
with open('D:\\UNI\\Data engineering\\JobSkillsMatching\\jobs\\karriere\\posts.txt', "r", encoding="utf-8") as f:
    html_content = f.read()

# Parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Extract the clean version of the content
clean_content = soup.get_text()

# Write the clean content to another file
with open('D:\\UNI\\Data engineering\\JobSkillsMatching\\jobs\\karriere\\jobposts.txt', "w", encoding="utf-8") as ft:
    ft.write(clean_content)