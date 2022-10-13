import time
import codecs
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

# captivate playlist url
url = "https://www.aparat.com/playlist/584204"
url_prefix = "https://www.aparat.com"
filenames = []

# create driver
driver = webdriver.Firefox()
driver.get(url)

page_links = []
download_links = []
# wait for the page to load
WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.XPATH, "/html/body/div[2]/main/div/div/div[2]/ul")))
# get all links
ul = driver.find_element(By.XPATH, "/html/body/div[2]/main/div/div/div[2]/ul")
lis = ul.find_elements(By.TAG_NAME, "li")
for li in lis:
    a = li.find_element(By.TAG_NAME, "a")
    page_links.append(a.get_attribute("href"))
    filenames.append(a.text)

for page_link in page_links:
    driver.get(page_link)
    
    # wait for the page to load
    download_xpath = "/html/body/div[2]/main/div[2]/div/div[1]/div[2]/div[2]/div[2]/div/div[1]/div[3]/div"
    WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.XPATH, download_xpath)))
    time.sleep(5)
    
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
    break

# remove all duplicates
links = list(set(download_links))

if  len(links) > 0:
    with codecs.open("links.txt", "w", "utf-8") as f:
        for link, filename in zip(links, filenames):
            f.write(link + ','+ filename + "\n")

# download files
directory = 'captivate/'
for link, filename in zip(links, filenames):
    print("downloading file: " + filename)
    r = requests.get(link)
    with open(directory + filename + ".mp4", "wb") as f:
        f.write(r.content)

