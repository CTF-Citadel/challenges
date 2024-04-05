# Lost Access

> [!NOTE]
>
> This Web-Challenge involves finding a correct way to access an endpoint via bruteforcing a users' password.

## Challenge Development

For this challenge I created a simple `Flask` service. <br/>
```py
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
```

Essentially this challenge consists of multiple stages, each stage indicates some authentication mechanism you need to bypass. <br/>
For security reasons, the values for `username`, `password` and `User-Agent` were hashed two times using `MD5`. <br/>
Each stage returns some kind of error indicating on what a user would need to fix next. <br/>
First you have to find the correct `Syntax` to provide the credentials which in this case is simple `html-forms`. <br/>
```py
import requests

forms = {
    'username': 'CCIE',
    'password': 'Test'
}

res = requests.get(URL, data=forms)
```

The python implementation above would send credentials in the correct format. <br/>
After passing the correct syntax for the credentials, the correct `User-Agent` needs to be passed along in the `Request-Headers`. <br/>
The correct Header can be aquired through the challenge-description and a bit of research on the internet. <br/>
The next stage is about passing along the correct `username` which can just be read from the challenge-description. <br/>
The last stage involves bruteforcing the correct `password`. The password can be found somewhere in the default `rockyou.txt` in the first 2000 passwords. <br/>

To make the challenge dynamic the `Flag` is being passed along during build in the `docker-compose.yml` file. <br/>
```yml
version: '3.9'

services:
  flask:
    build:
      context: .
      dockerfile: Dockerfile
      args:
        - FLAG=$FLAG
    ports:
      - "80:5000"
```

To build the container and setup a python environment a Dockerfile is being used. <br/>
```docker
FROM python:3.8-slim

ARG FLAG
ENV FLAG=${FLAG}

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

CMD ["python", "service.py"]
```