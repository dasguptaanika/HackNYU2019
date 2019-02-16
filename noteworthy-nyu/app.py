import os
from PyPrograms import ocrToFile, main, textToPdf
from flask import Flask, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/tmp'
ALLOWED_EXTENSIONS = set(['png', 'jpg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
  # this has changed from the original example because the original did not work for me
    return filename[-3:].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            print(app.config['UPLOAD_FOLDER'])
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            url_for('uploaded_file', filename=filename)
            ocrToFile.toFile(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            main.main()
            return('Notes can be found at https://noteworthy-nyu.herokuapp.com/tmp/notes.pdf')
    return 'Image not found'

@app.route('/tmp/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                              filename)

if __name__ == '__main__':
  app.debug = True
  app.run()
