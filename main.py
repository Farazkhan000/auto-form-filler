from flask import Flask, render_template, request
import os
from cv_parser import parse_pdf

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No file uploaded"
    
    file = request.files['file']
    if file.filename == '':
        return "No file selected"
    
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    # Parse PDF
    name, email, phone = parse_pdf(file_path)

    return render_template('result.html', name=name, email=email, phone=phone)

if __name__ == '__main__':
    app.run(debug=True)
