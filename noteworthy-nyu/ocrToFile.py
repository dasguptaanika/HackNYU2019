from main_nlp import main_nlp

import io
import cv2
from PIL import Image
import pytesseract

def toFile(input):
    output = r"input.txt"
    image = cv2.imread(input,0)
    image = cv2.GaussianBlur(image,(1,1),2)
    retval2,image = cv2.threshold(image,125,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    target = pytesseract.image_to_string(Image.fromarray(image))
    file = open(output,"w") 
    #file.write(str(target.encode("utf-8")))
    file.write(target)
    file.close()

    print("Finished Image processing")

    main_nlp()


toFile(r"img.jpg")
