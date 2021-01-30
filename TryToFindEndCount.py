import datetime
import logging
import os
import sys
import time
import traceback
import numpy as np
from timeit import default_timer as timer
from tkinter import messagebox
import keyring
import pandas as pd
import pyautogui as P
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import pyperclip
import re

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
WebDriverWait(driver, 4).until(EC.presence_of_element_located(
    (By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div[2]/div[1]/div/div/div[1]/div[2]/div[2]/div/div/div')))
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


# Copy all data into Clipboard.
def copy_clipboard():
    P.hotkey('ctrl', 'a')
    time.sleep(0.1)
    P.hotkey('ctrl', 'c')
    time.sleep(0.1)
    return pyperclip.paste()


counter = 0
dyn_list = []
while counter <= 7:
    time.sleep(0.5)
    # Scroll down the web page.
    P.scroll(-10000)
    time.sleep(0.5)
    # P.doubleClick(P.position())
    # Dynamic list to append.
    var = copy_clipboard()
    dyn_list = []
    dyn_list.clear()
    dyn_list.append(var)
    # Extract only Search query results.
    # df_search_queries = df_converted.iloc[1::3]
    # Extract only Volume of search queries.
    # df_volume = df_converted.iloc[2::3]
    # Assign Search query results a column name - 'Search query'.
    # df_column_search_queries = pd.DataFrame(df_search_queries.values, columns=['Search query'])
    # Increment index
    # df_column_search_queries.index = df_column_search_queries.index + 1
    # time.sleep(1)
    # print(str(len(df_column_search_queries.index)))
    # print(df_column_search_queries.to_string())
    # messagebox.showinfo("Extract individual page!")
    time.sleep(1)
    # Adjust the logic for clicking on the Show more results button.
    P.click(button='left', x=900, y=940, clicks=1)
    time.sleep(1)

    counter += 1

file_list_trimmed = []
for el in dyn_list:
    file_list_trimmed = [re.sub(r'\r\n', '|', el) for el in dyn_list]

list_one = [l.split('|') for l in '|'.join(file_list_trimmed).split('|')]
list_one.pop(0)
list_one.pop(0)
print(list_one)
search = list_one[1::3]
volume = list_one[2::3]
print(search)
print(volume)
# print(f"List data: \n {list_query}")
# df_converted = pd.DataFrame(dyn_list, columns=['Index'])
# Extract only Search query results.
# df_search_queries = df_converted.iloc[1::3]
# Extract only Volume of search queries.
# df_volume = df_converted.iloc[2::3]
# Assign Search query results a column name - 'Search query'.
# df_column_search_queries = pd.DataFrame(df_search_queries.values, columns=['Search_query'])
# lambda expression for find/replace a comma with emtpy space, avoid a new line.
# df_column_search_queries['Search_query'] = [x.replace(',', '') for x in df_column_search_queries['Search_query']]
# Assign Volume data column a name - 'Volume'.
# df_column_volume = pd.DataFrame(df_volume.values, columns=['Volume'])
# Concatenate the dataframes into a single one.
# df_search_queries_volume = pd.concat([df_column_search_queries, df_column_volume], axis=1)
# print(df_search_queries_volume.values)
# P.doubleClick(P.position())
# Dynamic list to append.
# dyn_list = []
# var = copy_clipboard()
# dyn_list.append(var)
# print(dyn_list)
# Convert data from Clipboard into a pandas dataframe.
# df = pd.read_clipboard(sep='delimiter')
# df = pd.read_clipboard(sep='delimiter', error_bad_lines=False)
# df_converted = pd.DataFrame(df.values, columns=['Index'])
# Extract only Search query results.
# df_search_queries = df_converted.iloc[1::3]
# Extract only Volume of search queries.
# df_volume = df_converted.iloc[2::3]
# Assign Search query results a column name - 'Search query'.
# df_column_search_queries = pd.DataFrame(df_search_queries.values, columns=['Search query'])
# Increment index
# df_column_search_queries.index = df_column_search_queries.index + 1
# driver.quit()

# Think on how to start incrementation from one and make the logic for clicking on Button to view more results
