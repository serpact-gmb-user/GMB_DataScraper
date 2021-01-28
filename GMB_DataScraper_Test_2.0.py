import csv
import math
import os
import time
import re
import sys
from re import match
from urllib.request import Request, urlopen

import pandas as pd
import numpy as np
import logging
import keyring
import pywin32_system32
import traceback

from timeit import default_timer as timer
from datetime import timedelta
from tkinter import messagebox

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import httplib2
from bs4 import BeautifulSoup, SoupStrainer
import urllib.request
import re
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pynput.mouse import Button, Controller
import urllib3

# Add emailing functionality (dev-error log, business log, error-screenshot attachment).
username = "stoyan24"
cred_username = "GMBUsername"
cred_password = "GMBPassword"
# print(keyring.get_password(cred_username, username))
# print(keyring.get_password(cred_password, username))

# Start time.
start = timer()
# Credentials/variable declaration.
# username = 'stoyan.ch.stoyanov11@gmail.com'
# password = 'St-564289713'
path_myBusinessLink = 'https://business.google.com/insights/l/00989318428858229135?hl=bg'
GMB_Business_Accounts = 'GMB_Accounts.csv'
csv_file_name = 'WebPageScrape.csv'
new_csv_file_name = 'NewWebPageScrape.csv'
final_csv_file_name = 'FinalWebPageScrape.csv'
end_csv_file_name = 'GMB_End_Keyword_SearchTimes.csv'
values_to_remove = {"Заявка", "Потребители"}
# Instantiate global lists for keywords and times they appear.
gl_keywords_list = []
gl_times_list = []
# Instantiate emtpy lists to hold web element data.
list_elements = []
new_list_elements = []
# Regex pattern
regEx = "^[0-9]{1,}"

# OPTIONAL -- TESTING
# Add options to Chromedriver installation
# options = webdriver.ChromeOptions()
# options.headless = True
# OPTIONAL -- TESTING
# Path to Chromedriver engine.
# path = r'C:\\Users\\ststoyan\\source\\repos\\GITC.user32\\packages\\chromedriver.exe'
path = os.path.dirname(os.path.abspath(__file__)) + '/chromedriver.exe'
# Chromedriver.exe path. NB: Browser navigation made to headless with options set to True.
driver = webdriver.Chrome(executable_path=path)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler('Execution.log')
format_logger = logging.Formatter('%(name)s - %(levelname)s - %(message)s : %(asctime)s',
                                  datefmt='%d.%m.%Y_%H:%M'
                                          ':%S')
file_handler.setFormatter(format_logger)

logger.addHandler(file_handler)
#
# # Checking driver and browser versions.
# browser_version = driver.capabilities['browserVersion']
# driver_version = driver.capabilities['chrome']['chromedriverVersion'].split(' ')[0]
# logger.info(f"Obtaining Chrome Browser and Driver versions: {browser_version}, {driver_version}")
#
# #  if browser_version != driver_version:
# #     print("Browser and driver version incompatible. Please, download chromedriver version: {0}!".format(
# #          driver_version))
# #     print("Ending process!")
# #      logger.error("Chrome Driver and Browser versions incompatible. Ending process execution")
# #     driver.close()
#
driver.maximize_window()
driver.get(
    'https://accounts.google.com/o/oauth2/v2/auth/oauthchooseaccount?redirect_uri=https%3A%2F%2Fdevelopers.google.com%2Foauthplayground&prompt=consent&response_type=code&client_id=407408718192.apps.googleusercontent.com&scope=email&access_type=offline&flowName=GeneralOAuthFlow')
time.sleep(2)
driver.maximize_window()
logger.info("Accessing GMB Data Scraper business account login screen")

# Select the username input field.
user_element = driver.find_element(By.CSS_SELECTOR, 'input')
# Insert username credential.
user_element.send_keys(keyring.get_password(cred_username, username))
time.sleep(1)
logger.info("Entering username credential")
# Click on Next button.
button_element = driver.find_element(By.ID, 'identifierNext')
button_element.click()
time.sleep(2)
# Select the password input field.
password_element = driver.find_element(By.NAME, 'password')
time.sleep(1)
logger.info("Entering password credential")
try:
    # Enter password credentials.
    password_element.send_keys(keyring.get_password(cred_password, username))
    time.sleep(1)
    # Click on Next button.
    button_element = driver.find_element(By.ID, 'passwordNext')
    time.sleep(1)
    button_element.click()
    time.sleep(1)
    logger.info("Navigating into GMB Data Scraper business account")
except Exception:
    ex_type, ex_value, ex_traceback = sys.exc_info()
    date = time.strftime('%d_%m_%Y_%H_%M_%S')
    trace_back = traceback.extract_tb(ex_traceback)
    stack_trace = []
    for trace in trace_back:
        stack_trace.append(
            "File : %s , Line: %s , Func.Name: %s, Message: %s" % (trace[0], trace[1], trace[2], trace[3]))
        driver.save_screenshot("{0}_Error_{1}.png".format(date, ex_type.__name__))
        logger.info(f"Error! Invalid credentials entered. Error type: {ex_type.__name__}")

# Create a .csv reader and csv_dict variables, read the GMB Account links from .csv file.
csv_reader = csv.reader(open(GMB_Business_Accounts))
csv_dict = {}
# Test lists.
list_elements = []
new_list_elements = []

for row in csv_reader:
    key = row[0]
    if key in csv_dict:
        pass
    csv_dict[key] = row[1:]
    # Skipping .csv header row.
    if row[1] == 'GMB Links':
        continue
    print(row[1])
    # messagebox.showinfo("Reading .csv file with links", "Info")
    logger.info(f"Reading GMB Business account links from {GMB_Business_Accounts}")

    # Access each GMB link extracted from source .csv file.
    driver.get(path_myBusinessLink)
    # Searching for 'Show keywords result' on GMB My Business Account page.
    driver.get(row[1])
    driver.maximize_window()
    time.sleep(2)
    button_keywords = driver.find_element(By.XPATH,
                                          '//*[@id="yDmH0d"]/c-wiz/div[2]/div[1]/div/div/div[1]/div[2]/div[2]/div/div/div')
    button_keywords.click()
    WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.TAG_NAME, 'header')))
    pop_up_page = driver.find_element_by_css_selector('div[class="VfPpkd-Jh9lGc"]').tag_name
    mouse = Controller()
    mouse.position = (1555, 969)
    time.sleep(2)
    mouse.scroll(0, -500)
    mouse.position = (700, 860)
    time.sleep(2)
    mouse.click(Button.left, 1)
    time.sleep(1)
    mouse.release(Button.left)
    time.sleep(2)
    req = Request(row[1])
    resp = requests.get("https://business.google.com/local/business/12976422705466664939/promote/performance/queries")
    # soup = BeautifulSoup(html_page.content, 'html.parser')
    # soup = BeautifulSoup(html_page.content, 'lxml')
    # Figure out how to extract the data table.
# counter = 5
# while counter <= 5:
#     driver.execute_script("window.scrollTo(0, 768)")
#     # driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
#     counter += 1

"""First method works"""
# parser = 'html5lib'
# resp = urllib.request.urlopen('https://business.google.com/insights/l/00989318428858229135')
# soup = BeautifulSoup(resp, parser, from_encoding=resp.info().get_param('charset'))
#
# for link in soup.find_all('a', href=True):
#     print(link['href'])

"""Second method"""
# req = Request('https://business.google.com/insights/l/00989318428858229135')
# html_page = urlopen(req)
#
# soup = BeautifulSoup(html_page, 'lxml')
#
# links = []
# for link in soup.find_all('a'):
#     links.append(link.get('href'))
#     print(link)
