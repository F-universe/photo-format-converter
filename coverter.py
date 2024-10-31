from flask import Flask, render_template, request, redirect, url_for, send_file
from werkzeug.utils import secure_filename
from PIL import Image
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    format = request.form.get('format')
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        output_file = convert_image(filepath, format)
        return send_file(output_file, as_attachment=True)

    return redirect(request.url)

def convert_image(input_path, output_format):
    image = Image.open(input_path)
    output_filename = input_path.rsplit('.', 1)[0] + '.' + output_format
    image.save(output_filename, format=output_format.upper())
    return output_filename

if __name__ == '__main__':
    app.run(debug=True)
