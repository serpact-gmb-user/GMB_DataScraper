import csv
import math
import os
import time

import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
# chrome_options.add_argument('--window-size=1920,1080')
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--start-maximized')
# chrome_options.add_argument('--disable-setuid-sandbox')
# chrome_options.add_argument('--disable-extensions')

username = "stoyan.ch.stoyanov11@gmail.com"

# def do_login(username, password):
path = os.path.dirname(os.path.abspath(__file__)) + '/chromedriver.exe'
driver = webdriver.Chrome(executable_path=path, options=options)
driver.maximize_window()
url_address = 'https://accounts.google.com/o/oauth2/v2/auth/oauthchooseaccount?redirect_uri=https%3A%2F%2Fdevelopers.google.com%2Foauthplayground&prompt=consent&response_type=code&client_id=407408718192.apps.googleusercontent.com&scope=email&access_type=offline&flowName=GeneralOAuthFlow'
driver.get(url_address)
driver.maximize_window()
# email_address = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='identifierId']")))
user_element = driver.find_element(By.NAME, "identifier")
user_element.send_keys(username)
time.sleep(2)
print(user_element)
time.sleep(2)
button_element = driver.find_element(By.ID, 'identifierNext')
button_element.click()
time.sleep(2)
password_element = driver.find_element(By.NAME, 'password')
time.sleep(2)
# pw = WebDriverWait(driver, 5).until(
# EC.element_to_be_clickable((By.XPATH, "//input[@name='password']"))
# )
password_element.send_keys(password)
time.sleep(1)
# pw.send_keys(password)
button_element = driver.find_element(By.ID, 'passwordNext')
time.sleep(1)
button_element.click()
print(driver.title)
driver.close()

# print(do_login('stoyan.ch.stoyanov11@gmail.com', 'St-564289713'))
