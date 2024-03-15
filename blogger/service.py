from flask import Flask, render_template, request, redirect, url_for
import base64, json, os, uuid

app = Flask(__name__)

users = []

flag = f"TH{{{str(os.environ.get('FLAG'))}}}" # build flag

# Index page with login and signup links
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')