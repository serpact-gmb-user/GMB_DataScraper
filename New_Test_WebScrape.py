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

import keyring
import numpy as np
import pandas as pd
import pyautogui as P
import pyperclip
from google.cloud import bigquery
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# Add emailing functionality (dev-error log, business log, error-screenshot attachment).

# Start execution time.
start_time = datetime.datetime.now()
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
    if row[1] == 'GMB Accounts':
        continue
    logger.info(f"Current web link {row[1]}")
    logger.info(f"Reading GMB Business account links from {GMB_Business_Accounts}")

    # Iterate over GMB Accounts from GMB_Accounts_Data .csv file.
    driver.get(row[1])
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
        # Increment counter by 1.
        iter_counter += 1

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
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'VfPpkd-vQzf8d')))
    button_keywords.click()
    # Check for 'Ефективност' web element.
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, 'header')))
    time.sleep(4)
    # Select all data from current screen.
    P.click(button='left', x=400, y=500, clicks=1)
    time.sleep(2)
    P.scroll(-2000)
    time.sleep(3)
    # Click on Show more result queries button.
    P.click(button='left', x=690, y=866, clicks=1)
    time.sleep(3)

    while True:
        time.sleep(1)
        # Scroll down the web page.
        P.scroll(-10000)
        time.sleep(1)
        # Dynamic list to append web element data from Search query and Volume.
        var = copy_clipboard()
        dynamic_web_list = []
        dynamic_web_list.clear()
        dynamic_web_list.append(var)
        # List to hold trimmed from carriage returns and newline web elements.
        list_trim_carriage_return = []
        for el in dynamic_web_list:
            list_trim_carriage_return = [re.sub(r'\r\n', '|', el) for el in dynamic_web_list]

        split_on_pipe_list = [l.split('|') for l in '|'.join(list_trim_carriage_return).split('|')]
        # Remove 'Разширения на търсенията'.
        split_on_pipe_list.pop(0)
        # Extract index only dynamically at each iteration.
        index = split_on_pipe_list[1::3]
        time.sleep(1)
        # Click on Show more results button from web interface.
        P.click(button='left', x=900, y=940, clicks=1)
        time.sleep(1)
        # Instantiate list for storing index values.
        list_ext_web_index = []
        list_ext_web_index.clear()
        # Append each index to the empty list.
        list_ext_web_index.append(index[-1])
        # If statement - check if web index exists in np array of indices, break if statement NOT true.
        if list_ext_web_index not in np_arr_page_indexes:
            break

    # Instantiate empty list.
    trim_carriage_return = []
    for el in dynamic_web_list:
        trim_carriage_return = [re.sub(r'\r\n', '|', el) for el in dynamic_web_list]

    split_on_pipe_list = [l.split('|') for l in '|'.join(trim_carriage_return).split('|')]
    # Remove 'Разширения на търсенията'.
    split_on_pipe_list.pop(0)
    split_on_pipe_list.pop(0)
    # Extract 'Search query' and 'Volume' data (before DataFrame insertion).
    index = split_on_pipe_list[0::3]
    # Convert index to an integer.
    index = [int(i) for i in index[-1]]
    messagebox.showinfo("Pause!")
    search_query = split_on_pipe_list[1::3]
    volume = split_on_pipe_list[2::3]
    # Assign Search query results a column name - 'Search query'.
    df_column_search_queries = pd.DataFrame(search_query, columns=['Search_query'])
    # lambda expression for find/replace a comma with emtpy space, avoid a new line.
    df_column_search_queries['Search_query'] = [x.replace(',', '') for x in df_column_search_queries['Search_query']]
    # Assign Volume data column a name - 'Volume'.
    df_column_volume = pd.DataFrame(volume, columns=['Volume'])
    # Actions to remove empty spaces and comparison operators from origin dataframe.
    df_column_volume["Volume"] = df_column_volume["Volume"].str.replace(" ", "")
    df_column_volume["Volume"] = df_column_volume["Volume"].str.replace("<", "")
    df_column_volume["Volume"] = df_column_volume["Volume"].str.replace(">", "")
    df_column_volume["Volume"] = df_column_volume["Volume"].str.strip()
    # Generate date time in custom format dd-MM-yyyy HH:mm:ss.
    current_date = [time.strftime("%d-%m-%Y %H:%M:%S")]
    date = time.strftime("%d-%m-%Y %H:%M:%S")
    shop_name = driver.find_element(By.XPATH, '//*[@id="gb"]/div[4]/div[2]/div/c-wiz/div/div[1]/div[1]/div[1]')
    df_date = pd.DataFrame(current_date, columns=['Date'])
    # Concatenate the Search query, Volume and Date dataframes into a single df.
    df_search_queries_volume = pd.concat([df_column_search_queries, df_column_volume, df_date], axis=1)
    # Insert Date and Group data inside end dataframe structure.
    df_search_queries_volume['Date'] = df_search_queries_volume['Search_query'].apply(lambda x: date)
    df_search_queries_volume['Project_ID'] = df_search_queries_volume['Search_query'].apply(lambda y: store_name)
    df_search_queries_volume['Group_ID'] = df_search_queries_volume['Search_query'].apply(lambda y: group)

    # API Configuration.
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.dirname(os.path.abspath(__file__)) + "\service_account.json"
    client = bigquery.Client()
    table_id = "test_dataset.GMB_DataTable"

    # Splitting data size into 1 equal chunks of data, load the data straight from DataFrame into BigQuery (gbq-API).
    for data in np.array_split(df_search_queries_volume, 1):
        job_config = bigquery.LoadJobConfig(schema=[
            bigquery.SchemaField("Search_query", bigquery.enums.SqlTypeNames.STRING),
            bigquery.SchemaField("Volume", bigquery.enums.SqlTypeNames.STRING),
            bigquery.SchemaField("Date", bigquery.enums.SqlTypeNames.STRING),
            bigquery.SchemaField("Project_ID", bigquery.enums.SqlTypeNames.STRING),
            bigquery.SchemaField("Group_ID", bigquery.enums.SqlTypeNames.STRING)
        ])

        # Append the data at each iteration.
        job_config.write_disposition = bigquery.WriteDisposition.WRITE_APPEND
        job = client.load_table_from_dataframe(data, table_id, job_config=job_config)
        job.result()
        # End timestamp.
        end_time = datetime.datetime.now()
        print(end_time)
        logger.info(f'Process duration: {end_time - start_time}')

# Closing active web browser.
driver.quit()
