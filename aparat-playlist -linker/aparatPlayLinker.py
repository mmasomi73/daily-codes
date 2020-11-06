import requests
from bs4 import BeautifulSoup

url = "https://www.aparat.com/playlist/408021"
response = requests.get(url)

html_string = response.content

soup = BeautifulSoup(html_string, 'html.parser')

lis = soup.find_all('li', {"class": "playlist-item"})
for li in lis:
    for a in li.find_all('a', {"class": "light-80"}):
        print("https://www.aparat.com"+a['href'])
