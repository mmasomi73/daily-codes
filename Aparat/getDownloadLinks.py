import time
import codecs
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions


# captivate playlist url
url = "https://www.aparat.com/playlist/584204"

# create driver
driver = webdriver.Firefox()
driver.get(url)
download_links = []

# open links.txt file and read line by line
with codecs.open("links.txt", "r", "utf-8") as f:
    lines = f.readlines()
    for line in lines:
        driver.get(line)
        # wait for the page to load
        WebDriverWait(driver, 100).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, 'single-playlist__title')))
        # get meta tag
        meta = driver.find_element(By.XPATH, "//meta[@property='og:video']")
        # get content attribute
        content = meta.get_attribute("content")
        print(content)
        download_links.append(content)

# write download links to file
with codecs.open("download_links.txt", "w", "utf-8") as f:
    for link in download_links:
        f.write(link + "\n")
