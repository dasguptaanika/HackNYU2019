from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from PIL import Image

# .....
# ..... some exta code unimportant for this issue....
# ....


# here it is
ptr = open("tafAlternos.txt", "r")  # text file I need to convert
lineas = ptr.readlines()
ptr.close()
i = 750
numeroLinea = 0

while numeroLinea < len(lineas):
    if numeroLinea - len(lineas) < 60: # I'm gonna write every 60 lines because I need it like that
        i=750
        for linea in lineas[numeroLinea:numeroLinea+60]:      
            canvas.drawString(15, i, linea.strip())
            numeroLinea += 1
            i -= 12
        canvas.showPage()
    else:
        i = 750
        for linea in lineas[numeroLinea:]:
           canvas.drawString(15, i, linea.strip())
           numeroLinea += 1
           i -= 12
        canvas.showPage()
