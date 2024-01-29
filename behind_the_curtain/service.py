import os
from flask import Flask, render_template, request

app = Flask(__name__)

flag = f'TH{{{os.getenv("FLAG")}}}'

# Index Page
@app.route('/')
def index():
    return render_template('index.html', flag=flag)

# News Page
@app.route('/news')
def news():
    return render_template('news.html')

# Contact Page
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        return render_template('index.html', flag=flag)
    else:
        return render_template('contact.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')

