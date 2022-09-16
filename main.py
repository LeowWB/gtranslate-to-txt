from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os
import time
import csv

DRIVER_PATH = 'chromedriver/chromedriver.exe'
CSV_PATH = 'Saved translations - Saved translations.csv'
OUTPUT_PATH = 'output.csv'

# set up driver
driver = webdriver.Chrome(DRIVER_PATH) 
page_url = 'https://translate.google.com' 
driver.get(page_url) 
driver.maximize_window() 
driver.implicitly_wait(20) 
time.sleep(1)

# choose chinese. i can't use "Detect Language" because some words are interpreted as japanese.
choose_lang_button = driver.find_element(by=By.XPATH, value='/html/body/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[1]/c-wiz/div[1]/c-wiz/div[2]/button')
choose_lang_button.click()
time.sleep(1)
chinese_button = driver.find_element(by=By.XPATH, value='//*[@id="yDmH0d"]/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[1]/c-wiz/div[2]/c-wiz/div[1]/div/div[3]/div/div[3]/div[20]/div[2]')
chinese_button.click()
time.sleep(1)

# gets the pinyin of a chinese phrase from google translate
def get_pinyin(driver, chinese_phrase):
    textarea = driver.find_element(by=By.XPATH, value='/html/body/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[2]/div[3]/c-wiz[1]/span/span/div/textarea')
    textarea.clear()
    time.sleep(1)
    textarea.send_keys(chinese_phrase)
    driver.implicitly_wait(20) 
    time.sleep(1) 
    pinyin_label = driver.find_element(by=By.XPATH, value='/html/body/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[2]/div[3]/c-wiz[1]/div[2]/div[1]')
    pinyin = pinyin_label.get_attribute('innerHTML')
    return pinyin

# takes a line of the input csv and converts to lines of the output csv
def line_to_next_output_line(driver, line):
    if line[0] == 'English':
        english_bit = line[2]
        chinese_bit = line[3]
    else:
        english_bit = line[3]
        chinese_bit = line[2]
    pinyin = get_pinyin(driver, chinese_bit)
    return f'{english_bit},{chinese_bit} {pinyin}\n{chinese_bit},{english_bit} {pinyin}\n'


outputs = ''

with open(CSV_PATH, 'r', encoding='utf-8') as csv_file:
    reader = csv.reader(csv_file)

    for i, line in enumerate(reader):
        outputs += line_to_next_output_line(driver, line)

        if i % 10 == 0:
            print(f'progress: {i}')

with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
    f.write(outputs)
