# app.py
from flask import Flask, request, send_file, render_template
import os
from utils import sign_file, verify_signature

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
SIGNED_FOLDER = 'signed'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(SIGNED_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    signature = sign_file(file_path)
    with open(os.path.join(SIGNED_FOLDER, file.filename + ".sig"), "wb") as f:
        f.write(signature)

    return "File đã được ký và lưu thành công!"

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(UPLOAD_FOLDER, filename), as_attachment=True)

@app.route('/verify', methods=['POST'])
def verify():
    file = request.files['file']
    sig = request.files['signature']

    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)

    sig_path = os.path.join(SIGNED_FOLDER, file.filename + ".sig")
    sig.save(sig_path)

    with open(sig_path, 'rb') as f:
        signature = f.read()

    if verify_signature(path, signature):
        return "✅ Chữ ký hợp lệ!"
    else:
        return "❌ Chữ ký KHÔNG hợp lệ!"

if __name__ == '__main__':
    app.run(debug=True)
