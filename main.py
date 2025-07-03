from flask import Flask, render_template, request
import PyPDF2
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']

    if file.filename == '':
        return 'No selected file'

    if file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ''
        for page in pdf_reader.pages:
            text += page.extract_text()

        return render_template('result.html', extracted_text=text)

if __name__ == '__main__':
    # Only for local development
    app.run(debug=True)
    #changed
