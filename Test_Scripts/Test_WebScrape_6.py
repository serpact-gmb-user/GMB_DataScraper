from bs4 import BeautifulSoup
import requests

r = requests.get('https://business.google.com/insights/l/00989318428858229135?hl=bg').text
soup = BeautifulSoup(r, 'lxml')
print(soup.prettify().encode('cp1251', errors='ignore'))