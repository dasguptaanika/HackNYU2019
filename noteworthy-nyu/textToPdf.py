from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, Frame


def textToPdf(filename):

    styles = getSampleStyleSheet()
    styleN = styles['BodyText']
    styleH = styles['Heading1']
    story = []

    c = Canvas('output.pdf')

    buff = 0

    row1 = ""
    row2 = "                   "
    row3 = "                                      "   

    with open(filename, "r") as f:
        data = f.read()

    data = data.split("\n")

    #add some flowables
    tokens = ["~", "`", "@"]
    current_token = "~"

    i = 0
    while(i < len(data)):
        x = data[i]
        if(x != ""):
            if(str(x)[0] in tokens):
                current_token = x[0]
                x = x[1:]
                while(i < len(data) - 1 and data[i + 1] != ""):
                    if((data[i + 1][0] in tokens)):
                        break
                    else:
                        x += " " + data[i + 1]
                        i += 1

            if(current_token == "~"):
                story.append(Paragraph("<font size='12'>{}{}</font>".format(x.strip(), "\n"),styleN, bulletText = row1 + "•"))
                story.append(Paragraph("<br></br>", styleN))
            elif(current_token == "`"):
                story.append(Paragraph("<font size='11'>{}{}</font>".format(x.strip(), "\n"),styleN, bulletText = row2 + "•"))
                story.append(Paragraph("<br></br>", styleN))
            else:
                story.append(Paragraph("<font size='10'>{}{}</font>".format(x.strip(), "\n"),styleN, bulletText = row3 + "•"))
                story.append(Paragraph("<br></br>", styleN))
            if(buff >= 25):
                c.showPage()
                buff = 0
            else:
                buff += 1
        i += 1
        
    f = Frame(inch, inch, 6.5*inch, 9.5*inch, showBoundary=0)
    f.addFromList(story,c)
    c.save()


if __name__ == "__main__":
    textToPdf("inter.txt")

