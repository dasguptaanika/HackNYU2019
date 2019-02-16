from app import app

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Anika'}
    return '''
<html>
    <head>
        <title>Home Page - Microblog</title>
    </head>
    <body>
        <h1 style="align: center; color: dark-blue">Noteworthy</h1>
    </body>
</html>'''

