import os
from flask import Flask, flash, request, redirect, url_for
from flask_cors import CORS
from werkzeug.utils import secure_filename
from main import run_workflow
import json

UPLOAD_FOLDER = '../uploads'
CONFIG_FOLDER = '../config'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','yaml','yml','json'}


app = Flask(__name__)
CORS(app,origins=["http://localhost:5173"])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['CONFIG_FOLDER'] = CONFIG_FOLDER


import secrets
foo = secrets.token_urlsafe(16)
app.secret_key = foo

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    #print(request.get_data())
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return 'No file part'#redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return 'No selected file'#redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # display file name and redirect to the uploaded file
            return {'status':'done'} #redirect('/')
            #return redirect(url_for('upload_file', name=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    <form action="/run" method="post">
     <input type=file name=file>
     <input type=button name=submit value="Run Flow">
    </form>
    <form action="/run" method="post" enctype=multipart/form-data>
     <input type="text" name="email"></input>
     <input type=file name=file></input>
     <input type="submit" value="Signup"></input>
    </form>
    '''

@app.route('/run', methods=['POST'])
def run():
    print("\033[5;38;5;11m|------------------------------------------------------|\033[0;0m")
    print("\033[5;38;5;11m|---------------------- NEW RUN -----------------------|\033[0;0m")
    print("\033[5;38;5;11m|------------------------------------------------------|\033[0;0m")
    print('hello')
    file = request.files['file']
    filename = secure_filename(file.filename)
    filename = 'template_1.yaml'
    print(f"{filename}")
    result = run_workflow(dto_path=os.path.join(app.config['CONFIG_FOLDER'], filename))
    result_json=json.dumps(result,indent=4)
    print(result_json)
    return '''
    <!doctype html>
    <title>Process</title>
    <h1>Here is your process</h1>
    <p>'''+ result_json+'''</p>
    '''

@app.route('/run_from_react', methods=['POST'])
def run_from_react():
    print("\033[5;38;5;11m|------------------------------------------------------|\033[0;0m")
    print("\033[5;38;5;11m|---------------------- NEW RUN -----------------------|\033[0;0m")
    print("\033[5;38;5;11m|------------------------------------------------------|\033[0;0m")
    print('hello')
    filename = 'template_1.yaml'
    print(f"{filename}")
    result = run_workflow(dto_path=os.path.join(app.config['CONFIG_FOLDER'], filename))
    return result

# @app.route('/signup', methods = ['POST'])
# def signup():
#     email = request.form['email']
#     print(f"The email address is '{email}'")
#     return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)