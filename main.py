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
    time.sleep(2)
    textarea.send_keys(chinese_phrase)
    driver.implicitly_wait(20) 
    time.sleep(2) 
    pinyin_label = driver.find_element(by=By.XPATH, value='/html/body/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[2]/div[3]/c-wiz[1]/div[2]/div[1]')
    pinyin = pinyin_label.get_attribute('innerHTML')
    return pinyin

def swap_translation_output_string(translation_output_string):
    split_string = translation_output_string.split(',')
    return f'{split_string[1]},{split_string[0]}'

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
        translation_string = f'{english_bit} -> {chinese_bit} {pinyin}'
        prelim_output_string = f'{english_bit},{chinese_bit} {pinyin}'
    else:
        translation_string = f'{chinese_bit} {pinyin} -> {english_bit}'
        prelim_output_string = f'{chinese_bit} {pinyin},{english_bit}'

    user_input_request_string = f'{translation_string}\n[1] Ok\t[2] Swap\t[3] Both\t[4] Change English\t[5] Change English and Swap\t[6] Skip\n'
    user_choice = int(input(user_input_request_string))

    if user_choice == 1:
        output = f'{prelim_output_string}\n'
    elif user_choice == 2:
        output = f'{swap_translation_output_string(prelim_output_string)}\n'
    elif user_choice == 3:
        output = f'{prelim_output_string}\n{swap_translation_output_string(prelim_output_string)}\n'
    elif user_choice == 4 or user_choice == 5:
        new_english = input('Enter new English translation:\n')
        output = f'{prelim_output_string.replace(english_bit, new_english)}'
        if user_choice == 5:
            output = swap_translation_output_string(output)
        output += '\n'
    else:
        output = ''

    print(f'Result: {output}\n')
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
