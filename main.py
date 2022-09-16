from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os
import time

DRIVER_PATH = 'chromedriver/chromedriver.exe'

driver = webdriver.Chrome(DRIVER_PATH) 
page_url = 'https://translate.google.com' 
driver.get(page_url) 
driver.maximize_window() 
driver.implicitly_wait(20) 
time.sleep(2) 