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
from datetime import timedelta, datetime
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
from selenium.webdriver.common.action_chains import ActionChains
import urllib3
import pyautogui as P
from openpyxl import Workbook
import pyperclip
import string
import datetime

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
csv_file_name = 'Group_Project_Date.csv'
new_csv_file_name = 'NewWebPageScrape.csv'
final_csv_file_name = 'FinalWebPageScrape.csv'
end_csv_file_name = 'Result.csv'
result_file = 'GMBDataScrapeFinal.csv'
values_to_remove = {"Разбивка на търсенията"}
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
# Initiate process from here.
start_time = datetime.datetime.now()
driver.maximize_window()
driver.get("https://business.google.com/insights/l/16717946256408587345")
# driver.get("https://business.google.com/local/business/12976422705466664939/promote/performance/queries")
# driver.get("https://accounts.google.com/o/oauth2/v2/auth/oauthchooseaccount?redirect_uri=https%3A%2F%2Fdevelopers.google.com%2Foauthplayground&prompt=consent&response_type=code&client_id=407408718192.apps.googleusercontent.com&scope=email&access_type=offline&flowName=GeneralOAuthFlow")
time.sleep(2)
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
    date = time.strftime('%d-%m-%Y_%H:%M:%S')
    trace_back = traceback.extract_tb(ex_traceback)
    stack_trace = []
    for trace in trace_back:
        stack_trace.append(
            "File : %s , Line: %s , Func.Name: %s, Message: %s" % (trace[0], trace[1], trace[2], trace[3]))
        driver.save_screenshot("{0}_Error_{1}.png".format(date, ex_type.__name__))
        logger.info(f"Error! Invalid credentials entered. Error type: {ex_type.__name__}")

# Click on the 'Покажи още резултати' button
actions = ActionChains(driver)
WebDriverWait(driver, 4).until(EC.presence_of_element_located((By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div[2]/div[1]/div/div/div[1]/div[2]/div[2]/div/div/div')))
# Extract retail store name.
store_name = driver.find_element(By.XPATH, '//*[@id="gb"]/div[4]/div[2]/div/c-wiz/div/div[1]/div[1]/div[1]').text
logger.info(f"Capture store name: {store_name}")
# Navigate to search query and volume module window.
button_keywords = driver.find_element(By.XPATH,
                                      '//*[@id="yDmH0d"]/c-wiz/div[2]/div[1]/div/div/div[1]/div[2]/div[2]/div/div/div')
WebDriverWait(driver, 4).until(EC.presence_of_element_located((By.CLASS_NAME, 'VfPpkd-vQzf8d')))
button_keywords.click()
WebDriverWait(driver, 4).until(EC.presence_of_element_located((By.TAG_NAME, 'header')))
time.sleep(2)
# Select all data.
P.scroll(-1000)
time.sleep(2)
P.click(button='left', x=690, y=866, clicks=1)
time.sleep(2)
# Select all data.
P.hotkey("ctrl", "a")
time.sleep(2)
# Copy all data into Clipboard.
P.hotkey("ctrl", "c")
# Convert data from Clipboard into a pandas dataframe.
df = pd.read_clipboard(sep='delimiter')
# df = pd.read_clipboard(sep='delimiter', error_bad_lines=False)
df_converted = pd.DataFrame(df.values, columns=['Index'])
# Extract only Search query results.
df_search_queries = df_converted.iloc[1::3]
# Extract only Volume of search queries.
df_volume = df_converted.iloc[2::3]
# Assign Search query results a column name - 'Search query'.
df_column_search_queries = pd.DataFrame(df_search_queries.values, columns=['Search query'])
# lambda expression for find/replace a comma with emtpy space, avoid a new line.
df_column_search_queries['Search query'] = [x.replace(',', '') for x in df_column_search_queries['Search query']]
# Assign Volume data column a name - 'Volume'.
df_column_volume = pd.DataFrame(df_volume.values, columns=['Volume'])
# Concatenate the dataframes into a single one.
current_date = [time.strftime("%d-%m-%Y %H:%M:%S")]
date = time.strftime("%d-%m-%Y %H:%M:%S")
shop_name = driver.find_element(By.XPATH, '//*[@id="gb"]/div[4]/div[2]/div/c-wiz/div/div[1]/div[1]/div[1]')
df_date = pd.DataFrame(current_date, columns=['Date'])
messagebox.showinfo("Print element at each iteration!")
# print(df_date)
df_search_queries_volume = pd.concat([df_column_search_queries, df_column_volume, df_date], axis=1)
# Scroll down to Вижте още button to expand the search query results.
P.scroll(-10000)
time.sleep(2)
messagebox.showinfo("Search query and Volume data combined into a single dataframe.")
# Save the Google My Business Search query and Volume values inside a .csv file.
np.savetxt(end_csv_file_name, np.c_[df_search_queries_volume], fmt='%s', delimiter=',',
           header=str('Search query, Volume, Date'), comments='')

# Insert Date and Group data inside end .csv file.
df_search_queries_volume['Date'] = df_search_queries_volume['Search query'].apply(lambda x: date)
df_search_queries_volume['Group'] = df_search_queries_volume['Search query'].apply(lambda y: store_name)

# Save output to GMBDataScrapeFinal.csv file.
np.savetxt(result_file, np.c_[df_search_queries_volume], fmt='%s', delimiter=',',
           header=str('Search query, Volume, Date, Project, Group'), comments='')
logger.info(f'Result file generated: {result_file}')
messagebox.showinfo("Result file generated!")
        # writer.writerows(data_output)
# df_date = pd.DataFrame(date, columns=['Date']).fillna('')
# df_date.to_csv(end_csv_file_name, mode='a', header=False)
messagebox.showinfo("Wait to see the results!")
logger.info(f"Save extracted web data into temporary .csv file in root directory: {end_csv_file_name}")
driver.quit()
end_time = datetime.datetime.now()
print(f'Process duration: {end_time - start_time}')

# Clean the folder of residual .csv files.
# os.remove(csv_file_name)
# os.remove(new_csv_file_name)
# os.remove(final_csv_file_name)
logger.info(
    f"Cleaning work .csv files from root folder: {csv_file_name}, {new_csv_file_name}, {final_csv_file_name}")
