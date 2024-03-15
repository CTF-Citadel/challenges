# Cheap RSA

> [!NOTE]
>
> Almost every CTF has some kind of RSA challenge, for this reason I also wanted to add 1 to our CTF. 

## Challenge Development

For the flag creationi created a python script which is the main focus of the challenge. <br/>
```py
from Crypto.Util.number import getPrime, isPrime, bytes_to_long
import os

flag = f'TH{{{os.getenv("FLAG")}}}'
FLAG = bytes_to_long(flag.encode())

p = getPrime(300)

while (not isPrime(p + 50)):
    p = getPrime(300)

q = p + 50

n = p * q
e = 2**16 + 1
ct = pow(FLAG, e, n)

with open('output', 'w') as file: 
    file.write(f'n: {n}\n')
    file.write(f'e: {e}\n')
    file.write(f'ct: {ct}')
```

I leveraged the python library `pycrypto` for RSA encryption/decryption. <br/>
As per best practice I read the flag from envvar and convert it to an integer using `bytes_to_long(flag.encode())`. <br/>
I then proceed to search for a pair of prime numbers. The vulnerability in here lies in the calculation of the second prime number `q`. <br/>
Because we only have 1 unknown prime number, we can basically reverse for `p` and therefore calculate `d` for decryption. <br/>
After the the value `n` is calculated I build the ciphertext by using `pow(FLAG, e, n)`, afterwards the values are written to a output-file. <br/>

I use a simple docker-compose file to host a webservice which provides the files. <br/>
```yml
version: '3.9'

services:
  web:
    image: 10.0.0.2:5000/cheap_rsa
    build:
      context: .
      dockerfile: Dockerfile
      args:
        - FLAG=${FLAG}
    ports:
      - "80:5000"
```

This webservice is used to provide the files for the challenge. <br/>
```Dockerfile
FROM python:3.8-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

RUN chmod +x initiate.sh

CMD ["./initiate.sh"]
```

In the dockerfile I setup a python environment and start the bash-script `initiate.sh`. <br/>
```py
from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__)

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

To host the webservice I use `Flask` and its built-in function `send_from_directory` which is able to load files from the container. 