from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

# Index page to provide files
@app.route('/')
def index():
    return render_template('index.html')

# endpoint to download encrypted flag
@app.route('/download_output')
def download_output():
    return send_from_directory('.', 'output', as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
