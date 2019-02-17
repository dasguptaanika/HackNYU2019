from selenium import webdriver
import io
import cv2
from PIL import Image
import time
from main_nlp import main_nlp

from bs4 import BeautifulSoup

import re

#Remove unicode
unicode_regex = re.compile(r"\\u\w\w\w\w")

#Wherever the image is (better to be in the same directoryas the current program)
PATH = 

image = cv2.imread(PATH + "img.jpg",0)
image = cv2.GaussianBlur(image,(1,1),2)
retval2,image = cv2.threshold(image,125,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

name = "img2.jpg"

#Writes new file - probably can specify path if necessary
cv2.imwrite(name, image)

browser = webdriver.Chrome()

browser.get("https://secret-harbor.herokuapp.com/test")

fileinput = browser.find_element_by_name("file")

#PATH OF THE PROCESSED FILE
fileinput.send_keys(PATH + name)


browser.find_element_by_xpath("//input[@type='submit' and @value='Submit']").click()

time.sleep(10)

soup_level1=BeautifulSoup(browser.page_source, 'lxml')
raw_text = str(soup_level1).split("\n")[2:-2]

browser.close()

with open("test.txt", "w") as f:
    running_str = ""
    for line in raw_text:
        if(":" in line):
            tmp = line[line.index(":") + 1:-2]
            tmp = unicode_regex.sub("", tmp)
            
            tmp = tmp[2:-1]

            if(tmp != ""):
                running_str += tmp + "\n"

    f.write(running_str.strip())

print("\nFinished image processing")

main_nlp()





