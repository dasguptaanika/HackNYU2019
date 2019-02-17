import cv2
from PIL import Image
import pytesseract
def toFile(input):
    output = "/tmp/text.txt"
    image = cv2.imread("/tmp/text.txt",0)
    image = cv2.GaussianBlur(image,(1,1),2)
    retval2,image = cv2.threshold(image,125,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    target = pytesseract.image_to_string(Image.fromarray(image))
    file = open(output,"w") 
    file.write(target) 
    file.close()