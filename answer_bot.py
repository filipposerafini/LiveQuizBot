import cv2
import pytesseract
import os
import requests
import urllib
from bs4 import BeautifulSoup
import argparse

directory = "/home/filippo/Downloads/"
domain = "https://www.google.it/search?q="
headers_get = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1' }
row_height = 50
left = 34
left_answer = 106
right = 1046
right_answer = 970
question_top = 546
question_bottom = 902
answer_height = 166
first_answer_top = 890
second_answer_top = 1082
third_answer_top = 1274
answer_bottom = 1540

while True:
    for filename in os.listdir(directory):
        if (filename.startswith("screenshot") and filename.endswith(".png")):
            print("New screenshot found: " + filename)
            img = cv2.imread(directory + filename, cv2.IMREAD_GRAYSCALE)
            # os.remove(directory + filename)

            ret, question = cv2.threshold(img[question_top:question_bottom, left:right], 200, 255, cv2.THRESH_BINARY_INV)
            ret, answers = cv2.threshold(img, 200, 255, cv2.THRESH_BINARY)

            question_text = pytesseract.image_to_string(question, lang='ita').replace('?', ' ')
            row_count = question_text.count('\n')
            question_text = question_text.replace('\n', ' ')
            print(question_text)

            top = first_answer_top + row_count * row_height
            bottom = top + answer_height
            first_answer = answers[top:bottom, left_answer:right_answer]
            first_answer_text = pytesseract.image_to_string(first_answer, lang='ita').replace('\n', ' ')
            print(first_answer_text)

            top = second_answer_top + row_count * row_height
            bottom = top + answer_height
            second_answer = answers[top:bottom, left_answer:right_answer]
            second_answer_text = pytesseract.image_to_string(second_answer, lang='ita').replace('\n', ' ')
            print(second_answer_text)

            top = third_answer_top + row_count * row_height
            bottom = top + answer_height
            third_answer = answers[top:bottom, left_answer:right_answer]
            third_answer_text = pytesseract.image_to_string(third_answer, lang='ita').replace('\n', ' ')
            print(third_answer_text)

            first_query = (question_text + first_answer_text).replace(' ', '+')
            second_query = (question_text + second_answer_text).replace(' ', '+')
            third_query = (question_text + third_answer_text).replace(' ', '+')

            r = requests.get(domain + first_query, headers=headers_get)
            soup = BeautifulSoup(r.text, 'lxml')
            first_count = soup.find('div',{'id':'resultStats'}).text.split()[1]
            r = requests.get(domain + second_query, headers=headers_get)
            soup = BeautifulSoup(r.text, 'lxml')
            second_count = soup.find('div',{'id':'resultStats'}).text.split()[1]
            r = requests.get(domain + third_query, headers=headers_get)
            soup = BeautifulSoup(r.text, 'lxml')
            third_count = soup.find('div',{'id':'resultStats'}).text.split()[1]

            print(first_count, second_count, third_count)

            cv2.imshow("qwer", first_answer)
            cv2.imshow("asdf", second_answer)
            cv2.imshow("qdfr", third_answer)
            cv2.waitKey(0)

            cv2.destroyAllWindows()

        else:
            continue
