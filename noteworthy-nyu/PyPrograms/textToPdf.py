#Import Modules
from textwrap import TextWrapper
from tkinter import Tk, Button, Text
from reportlab.pdfgen.canvas import Canvas

#File to save to
canvas = Canvas("/tmp/notes.pdf")

#Open and process files
file = open("/tmp/notes.txt","r")
text = file.read()
textlines = text.split("\n")
wrapper = TextWrapper()
text_wrapped_lines = list()
for line in textlines:
    text_wrapped_lines += wrapper.wrap(line)
 
# Write the text to the pdf canvas
count = 0
text_object = canvas.beginText(60, 770)
 
for line in text_wrapped_lines:
    text_object.textLine(line)
    count += 1

    #If it goes over the page
    if count == 48:
       canvas.drawText(text_object)
       canvas.showPage()
       text_object = canvas.beginText(60, 770)
       count = 0
 
canvas.drawText(text_object)
 
# Save the pdf file
canvas.showPage()
canvas.save()