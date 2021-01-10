import csv
import math
import os
import time
import re
from re import match
from tkinter import messagebox

import io
import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By


# Credentials/variable declaration.
username = 'stoyan.ch.stoyanov11@gmail.com'
password = 'St-564289713'
path_myBusinessLink = 'https://business.google.com/insights/l/00989318428858229135?hl=bg'
csv_file_name = 'WebPageScrape.csv'
new_csv_file_name = 'NewWebPageScrape.csv'
final_csv_file_name = 'FinalWebPageScrape.csv'
values_to_remove = {"Заявка", "Потребители"}
# Regex pattern
regEx = "^[0-9]{1,}"
regEx_2 = "(^([а-яА-Я])+\s+([а-яА-Я])+)"

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

driver.maximize_window()
driver.get(
    'https://accounts.google.com/o/oauth2/v2/auth/oauthchooseaccount?redirect_uri=https%3A%2F%2Fdevelopers.google.com%2Foauthplayground&prompt=consent&response_type=code&client_id=407408718192.apps.googleusercontent.com&scope=email&access_type=offline&flowName=GeneralOAuthFlow')
driver.maximize_window()

# Select the username input field.
user_element = driver.find_element(By.CSS_SELECTOR, 'input')
# Insert username credential.
user_element.send_keys(username)
time.sleep(1)
# Click on Next button.
button_element = driver.find_element(By.ID, 'identifierNext')
button_element.click()
time.sleep(1)
# Select the password input field.
password_element = driver.find_element(By.NAME, 'password')
time.sleep(2)
# Enter password credentials.
password_element.send_keys(password)
time.sleep(1)
# Click on Next button.
button_element = driver.find_element(By.ID, 'passwordNext')
time.sleep(1)
button_element.click()
time.sleep(1)
# Navigate into Google MyBusiness.
driver.get(path_myBusinessLink)
count_pages = driver.find_element_by_xpath('//*[@id="search-keywords"]/div/span/div[2]/div[1]/div/span').text
len_split_text = len(list(count_pages))
# Retrieving the count of total items in the table.
split_text = list(count_pages)[10:12]
split_text[10:12] = [''.join(map(str, split_text[10:12]))]
total_count_values = int(split_text[0] + split_text[1])
# Check for round up or down of the page counter.
if int(split_text[1]) <= 5:
    page_counter = math.floor(total_count_values / 10)
else:
    page_counter = (math.ceil(total_count_values / 10) - 1)

# print(page_counter)
# forward = driver.find_element_by_xpath('//*[@id="search-keywords"]/div/span/div[2]/div[1]/div/div[2]/span/span/span').click()

list_elements = []
new_list_elements = []

for page in range(page_counter):
    """ TESTING LOGIC"""
    web_elements = driver.find_elements_by_css_selector('#search-keywords > div > span > div.OVNxrb > div.tAY0Ie')
    for element in range(len(web_elements)):
        lines_to_remove = driver.find_elements_by_css_selector('#search-keywords > div > span > div.OVNxrb > div.tAY0Ie > table > tbody > tr.tR1K6d')[0].text
        lines_to_array = np.atleast_2d(lines_to_remove)
        print(lines_to_array[0])
        if web_elements[element] not in lines_to_array[0]:
            messagebox.showinfo("Pause prompts", "Info prompts")
            # if j not in lines_to_remove:
            web_elements[element].click()
            print(web_elements[element].text)
            list_elements.append(web_elements[element].text)
            new_list_elements = np.atleast_2d(list_elements)
            forward = driver.find_element_by_xpath(
                '//*[@id="search-keywords"]/div/span/div[2]/div[1]/div/div[2]/span/span/span').click()
            time.sleep(1)
    """TESTING LOGIC"""

# Save output to .csv file.
np.savetxt(csv_file_name, new_list_elements, delimiter=",", fmt='%s', encoding='utf-8')
reader = csv.reader(open(csv_file_name))

# Filter the data in initial .csv file.
for row in reader:
    new_row = []
    for m in row:
        if m not in values_to_remove:
            new_row.append(m)
            # num_matching_value = re.split("\s", m, 1)
            # filtered_values = list(filter(lambda results: match('^[0-9]{1,}$', results), matching_value[0]))
            # print(filtered_values[0])
            #if re.findall(regEx, num_matching_value[0]):
                # del num_matching_value[0]
                # x = str(num_matching_value).replace(regEx_2, "|")
                # print(x)
                # Add a regex to distinguish between text literal characters and integers
                # Test the logic using list to numpy array to dataframe conversion.
                # new_row.append(num_matcsssssshing_value[0])
                # new_row.append(num_matching_value[0])
                # print(matching_value[0])
                # col_1.append(matching_value)
            # col_2.append(matching_value[2])
            # new_row.append(matching_value)
            # Original code.
            # new_row.append(m)

    csv.writer(open(new_csv_file_name, 'a')).writerow(new_row)

# Create an emtpy .csv file to store the filtered data.
with open(final_csv_file_name, 'w') as my_empty_csv:
    pass

# Populate new .csv file with filtered data, NO headers included.
with open(new_csv_file_name) as input_file, open(final_csv_file_name, 'w', newline='') as output_file:
    writer = csv.writer(output_file)
    for row in csv.reader(input_file):
        if any(field.strip() for field in row):
            writer.writerow(row)

# Clean the folder of residual files.
os.remove(new_csv_file_name)
# os.remove(csv_file_name)
# Closing web browsing session.
driver.close()
