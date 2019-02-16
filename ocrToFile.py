import cv2
from PIL import Image
import pytesseract
filename = input(r"Enter the full path of the image: ")
output = input(r"Enter the path of the file to write to: ")
image = cv2.imread(filename,0)
image = cv2.GaussianBlur(image,(1,1),2)
retval2,image = cv2.threshold(image,125,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
target = pytesseract.image_to_string(Image.fromarray(image))
file = open(output,"w") 
file.write(target) 
file.close() 
