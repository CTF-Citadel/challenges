# Zero to Hero

> [!NOTE]
>
> To start off the `Crypto` category I wanted to make a simple `cryptography` challenge. <br/>
> Instead of using simple MySQL I wanted to use a DB which has a slightly different SQL syntax.

## Challenge Development

> [!NOTE]
> 
> For a better user experience every CTF challenge needs some kind of storyline. <br/>
> In this challenge I tried to build the storyline around some kind of Banking Web Application which has a security flaw. 

Starting off I created the `docker-compose.yml` file which contains only 1 container. <br/>
```yml
version: '3.9'

services:
  web:
    build:
      context: .
      args:
        FLAG: ${FLAG}
    ports:
      - "80:5000"
```

Mapping the port `5000` which is used by `Flask` to the exposed port `80`, which can be used be the user. <br/>
The `Dockerfile` sets up the latest python container and installs its dependencies, the `flag` is also being imported in the `Dockerfile`. <br/>
```docker
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

The `Python Flask` service just provides the file `output` which contains the encoded `flag`. <br/>
```py
from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__)

flag = "TH{" + os.environ.get("FLAG") + "}" # build flag

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
```

The challenge itself is just `encryption.py` which is essentially made up of two parts. <br/>
The first part is that we load the `flag` from an envrionment variable and convert each character to binary. <br/>
The second part is the convertion, every `1` will be converted to a `0` and every `0` to a `1`. <br/>
The output will than be written to a file which is than being provided by the `Flask` service. <br/>
```py
import os

flag = f'TH{{{os.getenv("FLAG")}}}'

for char in flag:
    # convertion to ascii and aftrwards to binary
    binary_repr = bin(ord(char))[2:] 

    # Pad the binary representation with leading zeros to ensure each chunk is 8 bits long
    binary_repr_padded = binary_repr.zfill(8)

    # Split the binary representation into chunks of 8 bits
    inverted_binary_repr = binary_repr_padded.translate(str.maketrans('01', '10'))

    # Split single string into multiple
    binary_chunks = [inverted_binary_repr[i:i+8] for i in range(0, len(inverted_binary_repr), 8)]

    # Write binary to file
    with open('output', 'a') as file:
        for char in binary_chunks:
            file.write(f'{char}\n')

```



