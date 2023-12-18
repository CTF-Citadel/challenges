# My very own Encryption

> [!NOTE]
>
> This challenge came to my mind when I thought of a simple entrypoint challenge to Crypto. <br/>
> For this challenge I recreated a simple caesar cipher in a different way. 

## Challenge Development

> [!NOTE]
> 
> For a better user experience every CTF challenge needs some kind of storyline. <br/>
> In this challenge I tried to declare the code as a first graders project. 

For this challenge I created a simple python script. <br/>
```py
import os, base64, random

flag = "TH{" + str(os.environ.get("FLAG")) + "}"  # build flag  with env var

def encrypt(flag):
    encoded_flag = bytes(flag, 'utf-8').hex()

    shifted_pairs = [encoded_flag[i:i + 2] for i in range(0, len(encoded_flag), 2)]

    for i in range(999999):
        rndm = random.randint(1, 25)
        shifted_pairs = shifted_pairs[-rndm:] + shifted_pairs[:-rndm]

    encrypted_flag = ''.join(shifted_pairs)

    return base64.b64encode(bytes.fromhex(encrypted_flag))

with open('output', 'wb') as file: 
    file.write(encrypt(flag))
```

To have dynamic flags I used a function to read the environment variable `FLAG` which is imported during deployment. <br/>
I than created the function `encrypt(flag)` which basically converts the flag to `hex`. <br/>
Afterwards the `hex` string is being converted to an array of 2 characters each. <br/>
It is than being shifted to the left `999999`, the bitshift is a "random" number between 1 and 25. <br/>
To finish the encryption I fuse those pairs together again and convert it to a `base64` encoded string and print it to a file called `output`. <br/>

I use a simple docker-compose file to host a webservice. <br/>
```yml
version: '3.9'

services:
  web:
    build: .
    ports:
      - "80:5000"
```

This webservice is used to provide the files for the challenge. <br/>
```Dockerfile
FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

ARG FLAG
ENV FLAG=${FLAG}

RUN python3 /app/encryption.py

CMD ["python", "service.py"]
```

In the dockerfile I setup a python environment and load the flag to generate the encrypted flag. <br/>
```py
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
```

To host the webservice I use Flask and use the inbuild Flask function `send_from_directory` which is able to load files from the container. <br/>