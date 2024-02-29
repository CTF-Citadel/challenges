from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

# Index page to provide files
@app.route('/')
def index():
    return render_template('index.html')

# endpoint to download pdf
@app.route('/download_pdf')
def download_encryption_py():
    return send_from_directory('.', 'leaked_pdf_00.pdf', as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
