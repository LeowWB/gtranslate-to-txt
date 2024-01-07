# changes to make: if first part of entry is english, then un-capitalize if only the first letter is capitalized. then u can more easily find dupes.
# if entering pinyin AND english, ask for pinyin first

import time
import csv

CSV_PATH = 'Saved translations - Saved translations.csv'
OUTPUT_PATH = 'output.csv'

num_lines = 0

def process_line(line):
    if line[0] == 'English':
        english_bit = line[2]
        chinese_bit = line[3]
        en_to_zh = True
    else:
        english_bit = line[3]
        chinese_bit = line[2]
        en_to_zh = False

    english_bit = english_bit.replace(',','/').strip()
    chinese_bit = chinese_bit.replace(',','/').strip()

    return (english_bit, chinese_bit, en_to_zh)

def processed_line_to_output(processed_line):
    english_bit, chinese_bit, en_to_zh = processed_line
    pinyin = ''
    if en_to_zh:
        print(f'{english_bit} -> {chinese_bit}')
    else:
        print(f'{chinese_bit} -> {english_bit}')

    user_choice = input("[1] Add\t[2] Add Reversed\t[3] Don't Add\t[4] Change English\t[5] Add Pinyin\n")

    if '3' in user_choice:
        output = ''
    else:
        if '4' in user_choice:
            english_bit = input('Enter new English translation: ')
        
        if '5' in user_choice:
            pinyin = ' ' + input('Enter new pinyin: ')
        
        if en_to_zh:
            first_bit = english_bit
            second_bit = chinese_bit
        else:
            first_bit = chinese_bit
            second_bit = english_bit

        output = ''

        if '1' in user_choice:
            output += f'{first_bit},{second_bit}{pinyin}\n'
        
        if '2' in user_choice:
            output += f'{second_bit},{first_bit}{pinyin}\n'

    print(f'Result:\n{output}\n')
    return output

outputs = ''
processed_lines = []

with open(CSV_PATH, 'r', encoding='utf-8') as csv_file:
    num_lines = len(csv_file.readlines())
    csv_file.seek(0)
    reader = csv.reader(csv_file)

    for i, line in enumerate(reader):
        processed_lines.append(process_line(line))

        if i % 10 == 0:
            print(f'progress: {i}/{num_lines} ({i/num_lines*100:.2f}%)')

for i, processed_line in enumerate(processed_lines):
    print(f'({i}/{num_lines})',end='')
    outputs += processed_line_to_output(processed_line)

with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
    f.write(outputs)

print('DONE')
exit()
