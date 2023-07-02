from flask import Flask, flash, request, redirect, url_for, render_template
import urllib.request
import os
from werkzeug.utils import secure_filename
import cv2

app = Flask(__name__)
 
UPLOAD_FOLDER = 'static/uploads/'
 
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
 

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/demonstration')
def demonstration():
    return render_template('demonstration.html')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/demonstration', methods=['POST'])
def upload_image():

    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']

    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)

    if not(file and allowed_file(file.filename)):
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)

    input_image_path = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], input_image_path))
    flash('Input image uploaded')

    input_image = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], input_image_path))
    output_image = process_image(input_image)
    output_image_path = f"{input_image_path.split('.')[0]}_output.jpg"
    cv2.imwrite(os.path.join(app.config['UPLOAD_FOLDER'], output_image_path), output_image)
    flash('Output image computed')

    return render_template('demonstration.html', input_image_path=input_image_path, output_image_path=output_image_path)

def process_image(image):
    image = cv2.resize(image, (512, 512))
    return image
 
@app.route('/display/')
def display_image():
    filename = request.args.get('filename', None)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)

@app.route('/help')
def help():
    return render_template('help.html')

@app.route('/api')
def api():
    return render_template('api.html')


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)