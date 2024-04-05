from flask import Flask, request
import os, hashlib

app = Flask(__name__)

flag = f"TH{{{os.environ.get('FLAG')}}}" # build flag

# MD5 hash function
def md5(input_string):
    md5_hash = hashlib.md5()
    md5_hash.update(input_string.encode('utf-8'))
    return md5_hash.hexdigest()

# Index page only accessible with correct credentials
@app.route('/')
def index():
    try:
        # Get Request Header from request
        user_agent = request.headers.get('User-Agent')
        # Get User Credentials from request
        username = request.form['username'] 
        password = request.form['password']
        
        if md5(md5(user_agent)) == "785298abfffd12e08104201367ae7650": # Check for correct user agent
            if md5(md5(username)) == "bfa4f131774102936c04f9daa7813886": # Check for correct username
                if md5(md5(password)) == "538426b414495d52f3f8b33d9b6e4ffa": # Check for correct password
                    return f"You shall pass!\nGet your Flag here: {flag}" # return flag if all checks passed successfully
                else:
                    return "Wrong password!"
            else:
                return "Unknown user!"
        else:
            return "Can only connect from same device-type!" # Indicator for wrong User-Agent
    except:
        return "No credentials provided!"

if __name__ == '__main__':
    app.run(host='0.0.0.0')
