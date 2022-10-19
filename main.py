from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os
import time
import csv

TIMER_MULTIPLIER = 1
DRIVER_PATH = 'chromedriver/chromedriver.exe'
CSV_PATH = 'Saved translations - Saved translations.csv'
OUTPUT_PATH = 'output.csv'

# set up driver
driver = webdriver.Chrome(DRIVER_PATH) 
page_url = 'https://translate.google.com' 
driver.get(page_url) 
driver.maximize_window() 
driver.implicitly_wait(20*TIMER_MULTIPLIER) 
time.sleep(1*TIMER_MULTIPLIER)

# choose chinese. i can't use "Detect Language" because some words are interpreted as japanese.
choose_lang_button = driver.find_element(by=By.XPATH, value='/html/body/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[1]/c-wiz/div[1]/c-wiz/div[2]/button')
choose_lang_button.click()
time.sleep(1*TIMER_MULTIPLIER)
chinese_button = driver.find_element(by=By.XPATH, value='//*[@id="yDmH0d"]/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[1]/c-wiz/div[2]/c-wiz/div[1]/div/div[3]/div/div[3]/div[20]/div[2]')
chinese_button.click()
time.sleep(1*TIMER_MULTIPLIER)

# gets the pinyin of a chinese phrase from google translate
def get_pinyin(driver, chinese_phrase):
    textarea = driver.find_element(by=By.XPATH, value='/html/body/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[2]/div[3]/c-wiz[1]/span/span/div/textarea')
    textarea.clear()
    time.sleep(2*TIMER_MULTIPLIER)
    textarea.send_keys(chinese_phrase)
    driver.implicitly_wait(20*TIMER_MULTIPLIER) 
    time.sleep(2*TIMER_MULTIPLIER) 
    pinyin_label = driver.find_element(by=By.XPATH, value='/html/body/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[2]/div[3]/c-wiz[1]/div[2]/div[1]')
    pinyin = pinyin_label.get_attribute('innerHTML')
    return pinyin

def process_line(driver, line):
    if line[0] == 'English':
        english_bit = line[2]
        chinese_bit = line[3]
        en_to_zh = True
    else:
        english_bit = line[3]
        chinese_bit = line[2]
        en_to_zh = False

    pinyin = get_pinyin(driver, chinese_bit)
    
    return (english_bit, chinese_bit, pinyin, en_to_zh)

def processed_line_to_output(processed_line):
    english_bit, chinese_bit, pinyin, en_to_zh = processed_line
    if en_to_zh:
        print(f'{english_bit} -> {chinese_bit} {pinyin}')
    else:
        print(f'{chinese_bit} {pinyin} -> {english_bit}')

    user_choice = input("[1] Add\t[2] Add Reversed\t[3] Don't Add\t[4] Change English\t[5] Change Pinyin\n")

    if '3' in user_choice:
        output = ''
    else:
        if '4' in user_choice:
            english_bit = input('Enter new English translation: ')
        
        if '5' in user_choice:
            pinyin = input('Enter new pinyin: ')
        
        if en_to_zh:
            first_bit = english_bit
            second_bit = chinese_bit
        else:
            first_bit = chinese_bit
            second_bit = english_bit

        output = ''

        if '1' in user_choice:
            output += f'{first_bit},{second_bit} {pinyin}\n'
        
        if '2' in user_choice:
            output += f'{second_bit},{first_bit} {pinyin}\n'

    print(f'Result:\n{output}\n')
    return output

outputs = ''
processed_lines = []

with open(CSV_PATH, 'r', encoding='utf-8') as csv_file:
    reader = csv.reader(csv_file)

    for i, line in enumerate(reader):
        processed_lines.append(process_line(driver, line))

        if i % 10 == 0:
            print(f'progress: {i}')

for processed_line in processed_lines:
    outputs += processed_line_to_output(processed_line)

with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
    f.write(outputs)

print('DONE')
exit()
