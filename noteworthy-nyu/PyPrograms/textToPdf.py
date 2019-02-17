from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, Frame
styles = getSampleStyleSheet()
styleN = styles['BodyText']
story = []

c = Canvas('output.pdf')

buff = 0

row1 = ""
row2 = "                   "
row3 = "                                      "

def textToPdf(filename):

    with open(filename, "r") as f:
        data = f.read()

    data = data.split("\n")

    #add some flowables
    for x in data:
        if("         " in x):
            story.append(Paragraph("<font size='10'>{}{}</font>".format(x.strip(), "\n"),styleN, bulletText = row3 + "•"))
            story.append(Paragraph("<br></br>", styleN))
        elif("   " in x):
            story.append(Paragraph("<font size='11'>{}{}</font>".format(x.strip(), "\n"),styleN, bulletText = row2 + "•"))
            story.append(Paragraph("<br></br>", styleN))
        else:
            story.append(Paragraph("<font size='12'>{}{}</font>".format(x.strip(), "\n"),styleN, bulletText = row1 + "•"))
            story.append(Paragraph("<br></br>", styleN))
        if(buff >= 25):
            c.showPage()
            buff = 0
        else:
            buff += 1
        
    f = Frame(inch, inch, 6.5*inch, 9.5*inch, showBoundary=0)
    f.addFromList(story,c)
    c.save()

