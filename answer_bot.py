import cv2
import pytesseract
import os
import requests
from bs4 import BeautifulSoup
import multiprocessing

# PATH
SCREENSHOT = "screenshot.png"
DOMAIN = "https://www.google.it/search?q="

# COLORS
class colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

# SCREEN CONSTANTS
LEFT_QUESTION = 34
RIGHT_QUESTION = 1046
QUESTION_TOP = 546
QUESTION_BOTTOM = 902
LEFT_OPTION = 106
RIGHT_OPTION = 970
OPTION_HEIGHT = 166
ROW_HEIGHT = 50
OPTION_POSITION = [890, 1082, 1274]

def get_number_of_results(data):
    image = data[0]
    position = data[1]
    row_count = data[2]
    question_text = data[3]
    # Crop image
    top = position + row_count * ROW_HEIGHT
    bottom = top + OPTION_HEIGHT
    option = image[top:bottom, LEFT_OPTION:RIGHT_OPTION]
    # Read option text
    option_text = pytesseract.image_to_string(option, lang='ita').replace('\n', ' ')
    # Create query
    query = DOMAIN + (question_text + ' ' + option_text).replace(' ', '+')
    # Perform request and read results
    r = requests.get(query)
    soup = BeautifulSoup(r.text, 'lxml')
    results = soup.find('div',{'id':'resultStats'}).text.split()[1].replace('.', '')
    return option_text, int(results)

def print_results(result_list, negative):
    total = sum(n for _, n in result_list)
    if negative:
        guess = min(result_list, key=lambda x:x[1])
    else:
        guess = max(result_list, key=lambda x:x[1])
    for result in result_list:
        if result == guess:
            print(colors.BOLD, end='')
        print(result[0], end=' ')
        if result == guess:
            if negative:
                print(colors.YELLOW, end='')
            else:
                print(colors.GREEN, end='')
        print("%.2f%%\n" % ((result[1] / total) * 100))
        if result == guess:
            print(colors.END, end='')
    print("-----------------------------------------------------------------------")

def manage_question():
    os.system("adb exec-out screencap -p > " + SCREENSHOT)
    # Import image and remove screenshot from directory
    image = cv2.imread(SCREENSHOT, cv2.IMREAD_GRAYSCALE)
    os.remove(SCREENSHOT)
    # Threshold images for OCR
    ret, question = cv2.threshold(image[QUESTION_TOP:QUESTION_BOTTOM,
        LEFT_QUESTION:RIGHT_QUESTION], 200, 255, cv2.THRESH_BINARY_INV)
    ret, options = cv2.threshold(image, 200, 255, cv2.THRESH_BINARY)
    # Read question text (determining number of rows)
    question_text = pytesseract.image_to_string(question, lang='ita')
    negative = "NON" in question_text
    row_count = question_text.count('\n')
    question_text = question_text.replace('\n', ' ')
    print("\n" + colors.BOLD + question_text + colors.END + "\n")
    # Get number of results of each option in parallel
    pool = multiprocessing.Pool(processes=3)
    data = []
    for i in range(0, 3):
        data.append((options, OPTION_POSITION[i], row_count, question_text))
    result_list = pool.map(get_number_of_results, data)
    # Print results
    print_results(result_list, negative)

if __name__ == "__main__":
    while True:
        key = input("\nPress " + colors.BOLD + colors.GREEN + "ENTER" + colors.END + " to take " +
                "a screenshot or " + colors.BOLD + colors.RED + "q" + colors.END + " to quit: ")
        if not key:
            print()
            manage_question()
        elif key == 'q':
            break
