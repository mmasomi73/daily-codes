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
        download_xpath = "/html/body/div[2]/main/div[3]/div/div[1]/div[2]/div[2]/div[2]/div/div[1]/div[3]/div/div/button"
        # WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.XPATH, download_xpath)))
        time.sleep(10)

        # scroll down
        driver.execute_script("window.scrollTo(0, 200);")
        
        # # click downlaod button
        driver.find_element(By.XPATH, download_xpath).click()
        time.sleep(2)
        download_ul = driver.find_element(By.XPATH, "/html/body/div[2]/main/div[2]/div/div[1]/div[2]/div[2]/div[2]/div/div[1]/div[3]/div/div[2]/div/ul")
        
        # get last li
        last_li = download_ul.find_elements(By.TAG_NAME, "li")[-1]
        # get download link
        last_li.click()
        time.sleep(5)

        # got to opened window
        driver.switch_to.window(driver.window_handles[1])
        
        # get window url
        download_links.append(driver.current_url)
        print(driver.current_url)

        # close window
        driver.close()
        # switch to main window
        driver.switch_to.window(driver.window_handles[0])

# write download links to file
with codecs.open("download_links.txt", "w", "utf-8") as f:
    for link in download_links:
        f.write(link + "\n")
