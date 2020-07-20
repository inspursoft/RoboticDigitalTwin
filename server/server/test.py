from bottle import route, run, request
import os

count = 0
HTML= """
<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <title>file uploader</title>
    </head>
    <body>
        <form action="/upload" method="post" enctype="multipart/form-data">
            Category:      <input type="text" name="category" />
            Select a file: <input type="file" name="upload" />
            <input type="submit" value="Start upload" />
        </form>
    </body>
</html>
"""

@route('/', method='GET')
def index():
    return HTML

@route('/count', method='GET')
def hello():
    global count
    count = count + 1
    return "hello: %d" %(count)

@route('/upload', method='POST')
def do_upload():
    category   = request.forms.get('category')
    upload     = request.files.get('upload')
    name, ext = os.path.splitext(upload.filename)

    save_path = os.path.dirname(os.path.realpath(__file__))
    save_file = os.path.join(save_path, category+".png")
    upload.save(save_file) # appends upload.filename automatically
    return 'OK'

run(host="0.0.0.0", debug=True, reloader=True)
