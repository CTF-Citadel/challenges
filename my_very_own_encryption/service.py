from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__)

flag = "TH{" + os.environ.get("FLAG") + "}" # build flag

# Index page with login and signup links
@app.route('/')
def index():
    return render_template('index.html')

# endpoint to download encrypted flag
@app.route('/download_output')
def download_output():
    return send_from_directory('.', 'output', as_attachment=True)

# endpoint to download cipher
@app.route('/download_encryption_py')
def download_encryption_py():
    return send_from_directory('.', 'encrypter.py', as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
