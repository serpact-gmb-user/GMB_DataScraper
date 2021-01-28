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
button_keywords = driver.find_element(By.XPATH,
                                      '//*[@id="yDmH0d"]/c-wiz/div[2]/div[1]/div/div/div[1]/div[2]/div[2]/div/div/div')
time.sleep(2)
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
# lmbda expression for find/replace a comma with emtpy space, avoid a new line.
df_column_search_queries['Search query'] = [x.replace(',', '') for x in df_column_search_queries['Search query']]
# Assign Volume data column a name - 'Volume'.
df_column_volume = pd.DataFrame(df_volume.values, columns=['Volume'])
# Concatenate the dataframes into a single one.
current_date = time.strftime("%d-%m-%Y %H:%M:%S")
date = {"Date": [current_date]}
df_date = pd.DataFrame(date)
print(df_date)
df_search_queries_volume = pd.concat([df_column_search_queries, df_column_volume], axis=1)
# Scroll down to Вижте още button to expand the search query results.
P.scroll(-10000)
time.sleep(2)
messagebox.showinfo("Search query and Volume data combined into a single dataframe.")
# Save the Google My Business Search query and Volume values inside a .csv file.
np.savetxt(end_csv_file_name, np.c_[df_search_queries_volume], fmt='%s', delimiter=',',
           header=str('Search query, Volume'), comments='')

# Save the result data into a Result.csv file with Group, Project, Date columns added.
with open(end_csv_file_name, 'r') as final_empty:
    with open(csv_file_name, 'w') as output_data:
        writer = csv.writer(output_data, lineterminator='\n')
        reader = csv.reader(final_empty)

        data_output = []
        row = next(reader)
        row.append('Date')
        row.append('Group')
        row.append('Project')
        data_output.append(row)

        for row in reader:
            data_output.append(row)
        writer.writerows(data_output)

logger.info(f"Save extracted web data into temporary .csv file in root directory: {end_csv_file_name}")
messagebox.showinfo("Wait to see the results!")
driver.quit()
# reader = csv.reader(open(csv_file_name))

# Filter the data in initial .csv file before parsing process.
"""for row in reader:
    new_row = []
    for i in row:
        if i not in values_to_remove:
            num_matching_value = re.split("\s", i, 1)
            if re.findall(regEx, num_matching_value[0]):
                del num_matching_value[0]
                # new_row.append(num_matching_value[0])

    # Append data into .csv file row by row.
    csv.writer(open(new_csv_file_name, 'a')).writerow(new_row)
    messagebox.showinfo("Second Wait!")

# Force close reader sessions of initial .csv file.
del reader

# Create an emtpy .csv file to store the filtered data.
with open(final_csv_file_name, 'w') as my_empty_csv:
    pass

# Populate new .csv file with filtered data, NO headers included.
with open(new_csv_file_name) as input_file, open(final_csv_file_name, 'w', newline='') as output_file:
    writer = csv.writer(output_file)
    logger.info(
        f"Create {new_csv_file_name} and pass it as input file; create {final_csv_file_name} and pass it as output file")
    for row in csv.reader(input_file):
        if any(field.strip() for field in row):
            writer.writerow(row)

# Read result .csv file, split first column data into two columns.
with open(final_csv_file_name) as file_to_read:
    lines = file_to_read.readlines()
    logger.info(f"Read contents of {final_csv_file_name} file before final filtering of data")

for line in range(len(lines)):
    # Stripping lines of whitespace characters/tabs; splitting string into a list of elements.
    output = lines[line].replace("\n", "")
    list_output = re.split("\s", output)

    # Add two additional columns to final_csv_file_name -- Keyword, Search times,
    # Date (dd-MM-yyyy), Project name (GMB Data Scraper), Location, Location Group, URL Weblink
    # Obtain keyword values and appearance time from split list, append values to global lists.
    keywords = " ".join(list_output[:-1])
    logger.info(f"Current keyword element after filtering: {keywords}")
    times = list_output[-1]
    logger.info(f"Current search time count after filtering: {times}")
    gl_keywords_list.append(keywords)
    gl_times_list.append(times)

# Saving values to EndCSVFileName.csv file
np.savetxt(end_csv_file_name, np.c_[gl_keywords_list, gl_times_list], fmt='%s', delimiter=",")
logger.info(f"Insert all filtered and parsed data into {end_csv_file_name}")

with open(end_csv_file_name, 'r', newline="") as file_to_read:
    r = csv.reader(file_to_read)
    data = [line for line in r]

with open(end_csv_file_name, 'w', newline="") as file_to_write:
    w = csv.writer(file_to_write)
    w.writerow(['Keywords', 'Search times', 'Location', 'Location group', 'URL Address'])
    w.writerows(data)
"""
# Clean the folder of residual .csv files.
# os.remove(csv_file_name)
# os.remove(new_csv_file_name)
# os.remove(final_csv_file_name)
logger.info(
    f"Cleaning work .csv files from root folder: {csv_file_name}, {new_csv_file_name}, {final_csv_file_name}")
