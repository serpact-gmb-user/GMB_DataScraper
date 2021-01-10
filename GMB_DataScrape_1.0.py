import csv
import math
import os
import time
import re
import sys
from re import match
import pandas as pd
import numpy as np
import logging
import keyring
import pywin32_system32
import traceback

from timeit import default_timer as timer
from datetime import timedelta
from tkinter import messagebox

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


# Main function declaration.
def main():
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

    # Checking driver and browser versions.
    browser_version = driver.capabilities['browserVersion']
    driver_version = driver.capabilities['chrome']['chromedriverVersion'].split(' ')[0]
    logger.info(f"Obtaining Chrome Browser and Driver versions: {browser_version}, {driver_version}")

    #  if browser_version != driver_version:
    #     print("Browser and driver version incompatible. Please, download chromedriver version: {0}!".format(
    #          driver_version))
    #     print("Ending process!")
    #      logger.error("Chrome Driver and Browser versions incompatible. Ending process execution")
    #     driver.close()

    driver.maximize_window()
    driver.get(
        'https://accounts.google.com/o/oauth2/v2/auth/oauthchooseaccount?redirect_uri=https%3A%2F%2Fdevelopers.google.com%2Foauthplayground&prompt=consent&response_type=code&client_id=407408718192.apps.googleusercontent.com&scope=email&access_type=offline&flowName=GeneralOAuthFlow')
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
    time.sleep(1)
    # Select the password input field.
    password_element = driver.find_element(By.NAME, 'password')
    time.sleep(2)
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
        logger.showerror(f"Error! Invalid credentials entered. Error type: {ex_type.__name__}")

    # Try-except block -- handling all generic exceptions.
    try:
        # Create a .csv reader and csv_dict variables, read the GMB Account links from .csv file.
        csv_reader = csv.reader(open(GMB_Business_Accounts))
        csv_dict = {}
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
            # driver.get(path_myBusinessLink)
            driver.get(row[1])
            time.sleep(1)
            # Searching for 'Show keywords result' on GMB My Business Account page.
            button_keywords = driver.find_element(By.XPATH,
                                                  '//*[@id="yDmH0d"]/c-wiz/div[2]/div[1]/div/div/div[1]/div[2]/div[2]/div/div/div')
            button_keywords.click()
            # Waiting for button to be selectable to appear on screen and be clicked.
            time.sleep(2)

            '''From here on tomorrow - 10.01.2021'''
            # Search/click for 'See more keywords' by xpath element. TEST from this sectin on tomorrow -- see how to capture the Вижте още button.
            button_showKeywords = driver.find_element(By.CSS_SELECTOR, '#cHwEyf > div.FHHqqd > div > div > div.hJKKpe > div > div.J7elmb.bc99Ed.mL6HXe.RN8axf > c-wiz > c-wiz > div > div > details > div.ceU0Yb > div.guqnIf > div').text
            print(button_showKeywords)
            button_showKeywords.click()
            time.sleep(2)
            messagebox.showinfo("Navigate down the web page!")
            # Search click (test).

            # Extract keywords data table.
            keywords_data_table = driver.find_element(By.XPATH,
                                                      '//*[@id="cHwEyf"]/div[2]/div/div/div/div/div/div/c-wiz/c-wiz/div').text
            driver.get(keywords_data_table)
            print(keywords_data_table)
            time.sleep(1)
            messagebox.showinfo("Waiting for data table with keywords to appear!")

            new_list_elements = np.atleast_2d(list_elements)
            forward = driver.find_element_by_xpath(
                '//*[@id="search-keywords"]/div/span/div[2]/div[1]/div/div[2]/span/span/span').click()
            time.sleep(1)

        # Save extracted web element data to .csv file.
        np.savetxt(csv_file_name, new_list_elements, delimiter=",", fmt='%s')
        logger.info(f"Save extracted web data into temporary .csv file in root directory: {csv_file_name}")
        reader = csv.reader(open(csv_file_name))

        # Filter the data in initial .csv file before parsing process.
        for row in reader:
            new_row = []
            for m in row:
                if m not in values_to_remove:
                    num_matching_value = re.split("\s", m, 1)
                    if re.findall(regEx, num_matching_value[0]):
                        del num_matching_value[0]
                        new_row.append(num_matching_value[0])

            # Append data into .csv file row by row.
            csv.writer(open(new_csv_file_name, 'a')).writerow(new_row)

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

        # Clean the folder of residual .csv files.
        os.remove(csv_file_name)
        os.remove(new_csv_file_name)
        os.remove(final_csv_file_name)
        logger.info(
            f"Cleaning work .csv files from root folder: {csv_file_name}, {new_csv_file_name}, {final_csv_file_name}")

        # Remove .csv reader.
        del csv_reader

    except Exception:
        ex_type, ex_value, ex_traceback = sys.exc_info()
        date = time.strftime('%d_%m_%Y_%H_%M_%S')
        trace_back = traceback.extract_tb(ex_traceback)
        stack_trace = []
        for trace in trace_back:
            stack_trace.append(
                "File : %s , Line: %s , Func.Name: %s, Message: %s" % (trace[0], trace[1], trace[2], trace[3]))
        driver.save_screenshot("{0}_Error_{1}.png".format(date, ex_type.__name__))
        logger.showerror(f"Error! Generic system exception. Error type: {ex_type.__name__}")

    # Closing web browser session(s).
    end = timer()
    # Calculating elapsed process run-time.
    elapsed_time = timedelta(seconds=end - start)
    logger.info(f"Ending process. Execution time: {elapsed_time}")


# driver.close()


# Execute GMB Data Scraper.
if __name__ == "__main__":
    main()
