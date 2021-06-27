import os
from pdf2image import convert_from_path
import numpy as nm
import re
import pytesseract
import cv2
from PIL import ImageGrab

# For colored outputs
import colorama
from colorama import Fore, Back, Style
colorama.init()

# Function to clear terminal


def clear():
    os.system('cls')


# environment setup
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'

print(Fore.LIGHTBLUE_EX + "Converting PDF...")
# convert PDF to images
images = convert_from_path('D:\All Projects\PDFHunter\sample2.pdf',
                           poppler_path=r"D:\Downloads\Release-21.03.0\poppler-21.03.0\Library\bin")
print(Fore.GREEN+u'\u2713'+" Done")
buffer = ""
print(Fore.LIGHTBLUE_EX+"Indexing images...")

for image in images:
    #     Save pages as images in the pdf
    tesstr = pytesseract.image_to_string(cv2.cvtColor(
        nm.array(image), cv2.COLOR_BGR2GRAY), lang='eng')
    buffer += tesstr.lower()
print(Fore.GREEN+"\u2713 Done")

query_to_search = ""
while(query_to_search != "quit()"):
    print(Fore.GREEN+"\n")
    query_to_search = input(
        "Enter search string or quit() to exit...\n")
    if(query_to_search == "quit()"):
        break
    search_index = [m.start() for m in re.finditer(query_to_search, buffer)]
    ptr = 0
    max_size = len(search_index)
    while ptr < max_size or ptr >= 0:
        # next_delim=buffer[index:]
        if(max_size == 0):
            print(Fore.RED+"No results found!")
            break
        index = search_index[ptr]
        to_print = buffer[index:index+400]
        print(Fore.WHITE+to_print+"\n\n")
        print(Fore.CYAN+"Result %d of %d\n" % (ptr, max_size))
        print(Fore.GREEN+"\n")
        next_cmd = input(
            "next() to go to next result. prev() to go to next result. new() to initiate new search")
        if(next_cmd == "next()"):
            clear()
            ptr = (ptr+1) % max_size
        elif(next_cmd == 'prev()'):
            clear()
            ptr = ptr-1 if ptr > 0 else 0
        elif(next_cmd == 'new()'):
            clear()
            break
