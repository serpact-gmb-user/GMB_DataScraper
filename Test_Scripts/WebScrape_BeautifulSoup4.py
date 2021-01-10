from urllib.request import urlopen
from bs4 import BeautifulSoup

urlAddress = "https://www.benlcollins.com/apps-script/google-apps-script-beginner-guide/"

try:
    webPage = urlopen(urlAddress)

except:
    print("Error opening the URL address!")

obj_soup = BeautifulSoup(webPage, 'html.parser')

content = obj_soup.find('div', {"class": "entry-content"})
article = ''

for i in content.find_all('p'):
    article = article + ' ' + i.text
print(article)

with open('WebPageScrape.txt', 'w') as file:
    file.write(article)

