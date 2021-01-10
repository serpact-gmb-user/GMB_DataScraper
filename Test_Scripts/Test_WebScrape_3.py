import csv
import math
import os
import time

import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

username = 'stoyan.ch.stoyanov11@gmail.com'
password = 'St-564289713'

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
options.add_argument('--headless')
options.add_argument('--disable-gpu')

path = os.path.dirname(os.path.abspath(__file__)) + '/chromedriver.exe'
driver = webdriver.Chrome(executable_path=path, options=options)
driver.maximize_window()
url_address = 'https://accounts.google.com/o/oauth2/v2/auth/identifier?redirect_uri=https%3A%2F%2Fdevelopers.google.com%2Foauthplayground&prompt=consent&response_type=code&client_id=407408718192.apps.googleusercontent.com&scope=email&access_type=offline&flowName=GeneralOAuthFlow'
driver.get(url_address)
print(url_address)
print(url_address.title())
time.sleep(2)
text_box_username = driver.find_element(By.TAG_NAME, 'input')
text_box_username.send_keys("Hello!")
time.sleep(2)
button_one = driver.find_element(By.TAG_NAME, 'button').click()
time.sleep(2)
text_box_password = driver.find_element(By.TAG_NAME, 'input')
text_box_password.send_keys(password)
time.sleep(2)
button_two = driver.find_element(By.TAG_NAME, 'button').click()
time.sleep(2)

