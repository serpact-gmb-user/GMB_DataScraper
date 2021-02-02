import smtplib, ssl

import self as self
import yagmail
import csv
import datetime
import logging
import os
import re
import sys
import time
import traceback
import logging
import logging.handlers
from tkinter import messagebox
import json
import keyring
import numpy as np
import pandas as pd
import pyautogui as P
import pyperclip
import yagmail
from google.cloud import bigquery
from pandas_gbq import timestamp
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import argparse
from datetime import datetime
from datetime import timedelta
import json
import logging
import os
import re

from babel import Locale
from babel.core import UnknownLocaleError
from googleapiclient import discovery
from googleapiclient.errors import HttpError
from googleapiclient.http import build_http
from oauth2client import client, file, tools

### GENERIC EMAIL SENDING SOLUTION WITH SSL.
""" port = 465
smtp_server = "smtp.gmail.com"
sender_email = "stoyan.ch.stoyanov11@gmail.com"
receiver_email = "stoyan.ch.stoyanov11@gmail.com"
password = input("Type in your password here:")
message = Add docstring here
Subject: Test_Email


This message is a test email message from PyCharm IDE 2020."""

# Create a secure SSL context.
"""context = ssl.create_default_context()

with smtplib.SMTP_SSL(smtp_server, port, context=context) as email_server:
    email_server.login(sender_email, password)
    email_server.sendmail(sender_email, receiver_email, message)
"""
"""### SENDING EMAILS VIA YAGMAIL MODULE (SPECIFIC FOR GMAIL)
receiver = "stoyan.ch.stoyanov11@gmail.com"
body = "Hello, there, this is a test email!"
filename = "Execution.log"
password = input("Please, input a password here:")

try:
    yag = yagmail.SMTP("stoyan.ch.stoyanov11@gmail.com", password=password)
    yag.send(to=receiver, subject="Mail sent with attachment", contents=body, attachments=filename)
except Exception as e:
    print(f"Error: {e}")
"""

# Add emailing functionality (dev-error log, business log, error-screenshot attachment).

# Start execution time.
# start_time = datetime.datetime.now()
# Windows credentials vault.
username = "stoyan24"
cred_username = "GMBUsername"
cred_password = "GMBPassword"
# Variable declaration.
GMB_Business_Accounts = 'GMB_Account_Data.csv'
# Iteration flag - 1 set to indicate first iteration for insert log-in credentials.
group = ""
iter_counter = 1
gl_keywords_list = []
gl_times_list = []
# Instantiate emtpy lists to hold web element data.
list_elements = []
new_list_elements = []
# Search query, Volume raw data list.
dynamic_web_list = []
# Numpy array holding page index comparison values.
np_arr_page_indexes = np.array(["100", "200", "300", "400", "500", "600", "700", "800", "900", "1000",
                                "1100", "1200", "1300", "1400", "1500", "1600", "1700", "1800",
                                "1900", "2000", "2100", "2200", "2300", "2400", "2500", "2600", "2700", "2800",
                                "2900", "3000", "3100", "3200", "3300", "3400", "3500", "3600", "3700", "3800", "3900",
                                "4000"])
# Regex for identifying proper URL addresses.
url_regex = re.compile(r'^(?:http|ftp)s?://'
                       r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
                       r'localhost|'
                       r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
                       r'(?::\d+)?'
                       r'(?:/?|[/?]\S+)$', re.IGNORECASE)

# Email configuration detail (Email body for success, failure, filename).
receiver = "stoyan.ch.stoyanov11@gmail.com"  ### TO ADD ADDITIONAL EMAIL(s) OR A .CSV FILE FOR BULK DISPATCH.
email_subject_success = f"GMB_DataScraping - successful execution. {time.strftime('%d-%m-%Y %H:%M:%S')}"
email_subject_error = f"GMB_DataScraping - unsuccessful execution. {time.strftime('%d-%m-%Y %H:%M:%S')}"
email_body_success = "Dear business owner, \n\n the Search queries and Volume data have been successfully extracted " \
                     "from your store. \n\n Kind regards, \n\n GMB_DataScraping Team"
email_body_fail = "Dear business owner, \n\n the process for extracting Search query and Volume data has encountered \
                    an error. Process was terminated. \n\n Kind regards, \n\n GMB_DataScraping Team"
filename = "Execution.log"

# Chromedriver .exe absolute path location.
path = os.path.dirname(os.path.abspath(__file__)) + '/chromedriver.exe'
# Chromedriver.exe path. NB: Browser navigation made to headless with options set to True.
driver = webdriver.Chrome(executable_path=path)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Checking driver and browser versions.
browser_version = driver.capabilities['browserVersion']
driver_version = driver.capabilities['chrome']['chromedriverVersion'].split(' ')[0]
logger.info(f"Obtaining Chrome Browser and Driver versions: {browser_version}, {driver_version}")

file_handler = logging.FileHandler('Execution.log')
format_logger = logging.Formatter('%(name)s - %(levelname)s - %(message)s : %(asctime)s',
                                  datefmt='%d.%m.%Y_%H:%M'
                                          ':%S')
file_handler.setFormatter(format_logger)


# Copy all data into Clipboard.
def copy_clipboard():
    P.hotkey('ctrl', 'a')
    time.sleep(0.1)
    P.hotkey('ctrl', 'c')
    time.sleep(0.1)
    return pyperclip.paste()


logger.addHandler(file_handler)
# Create a .csv reader and csv_dict variables, read the GMB Account links from .csv file.
csv_reader = csv.reader(open(GMB_Business_Accounts))
csv_dict = {}
for row in csv_reader:
    key = row[0]
    if key in csv_dict:
        pass
    csv_dict[key] = row[1:]
    # Skipping .csv GMB Accounts header row.
    logger.info(f"Reading GMB Business account links from {GMB_Business_Accounts} file.")
    if row[1] == 'GMB Accounts':
        continue
    try:
        if re.match(url_regex, row[1]) is None:
            assert f"The current email address:{row[1]} is invalid! URL logged in Execution.log. Proceed with next URL."
            # Proceed with next email address.
            continue
        else:
            logger.info(f"Current web link: {row[1]}")
            print(re.match(url_regex, row[1]) is not None)
    except AssertionError as a:
        ex_type, ex_value, ex_traceback = sys.exc_info()
        date = time.strftime('%Y-%m-%d %H:%M:%S')
        trace_back = traceback.extract_tb(ex_traceback)
        stack_trace = []
        for trace in trace_back:
            stack_trace.append(
                "File : %s , Line: %s , Func.Name: %s, Message: %s" % (trace[0], trace[1], trace[2], trace[3]))
            driver.save_screenshot("{0}_Invalid_URL_{1}.png".format(date, ex_type.__name__))
            logger.info(stack_trace)
            logger.info(f"Assertion error! Invalid email address: {row[1]}\n Exception type: {ex_type.__name__}")

        password = "St-564289713"
        # password = input("Please, provide your email login password here:")
        try:
            # Sending email due to error encountered to recipient list.
            yag = yagmail.SMTP(receiver, password=password)
            yag.send(to=receiver, subject=email_subject_error, contents=email_body_fail, attachments=filename)
        except Exception as e:
            print(f"Error encountered during email dispatch: {e}\n {ex_type.__name__}")

    # Iterate over GMB Accounts from GMB_Accounts_Data .csv file.
    driver.get('https://business.google.com/insights/l/16717946256408587345')
    time.sleep(3)
    driver.maximize_window()
    time.sleep(2)

    if iter_counter == 1:
        # Select the username input field.
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input')))
        user_element = driver.find_element(By.CSS_SELECTOR, 'input')
        # Insert username credential.
        user_element.send_keys(keyring.get_password(cred_username, username))
        # time.sleep(1)
        logger.info("Entering username credential")
        # Click on Next button.
        button_element = driver.find_element(By.ID, 'identifierNext')
        button_element.click()
        # time.sleep(2)
        # Select the password input field.
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, 'password')))
        time.sleep(3)
        password_element = driver.find_element(By.NAME, 'password')
        time.sleep(3)
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
            date = time.strftime('%Y-%m-%d %H:%M:%S')
            trace_back = traceback.extract_tb(ex_traceback)
            stack_trace = []
            for trace in trace_back:
                stack_trace.append(
                    "File : %s , Line: %s , Func.Name: %s, Message: %s" % (trace[0], trace[1], trace[2], trace[3]))
                driver.save_screenshot("{0}_Error_{1}.png".format(date, ex_type.__name__))
                logger.info(f"Error! Invalid credentials entered. Error type: {ex_type.__name__}")
                password = "St-564289713"
                # password = input("Please, provide your email login password here:")
                try:
                    # Sending email due to error encountered to recipient list.
                    yag = yagmail.SMTP(receiver, password=password)
                    yag.send(to=receiver, subject=email_subject_error, contents=email_body_fail, attachments=filename)
                except Exception as e:
                    print(f"Error encountered during email dispatch: {e}\n {ex_type.__name__}")

        # Increment counter by 1.
        iter_counter += 1
        # Click on the 'Покажи още резултати' button
        actions = ActionChains(driver)
        WebDriverWait(driver, 4).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div[2]/div[1]/div/div/div[1]/div[2]/div[2]/div/div/div')))
        # Extract retail store name.
        store_name = driver.find_element(By.XPATH,
                                         '//*[@id="gb"]/div[4]/div[2]/div/c-wiz/div/div[1]/div[1]/div[1]').text
        logger.info(f"Capture store name: {store_name}")
        # Navigate to search query and volume module window.
        button_keywords = driver.find_element(By.XPATH,
                                              '//*[@id="yDmH0d"]/c-wiz/div[2]/div[1]/div/div/div[1]/div[2]/div[2]/div/div/div')
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'VfPpkd-vQzf8d')))
        button_keywords.click()
