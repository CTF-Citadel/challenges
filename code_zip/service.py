from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

# Index page to provide files
@app.route('/')
def index():
    return render_template('index.html')

# endpoint to download code.zip
@app.route('/download/code.zip')
def download_output():
    return send_from_directory('.', 'code.zip', as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1337)
