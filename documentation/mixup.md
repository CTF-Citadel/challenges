# My very own Encryption

> [!NOTE]
>
> This should be a medium challenge which entails a substitution cipher.

## Challenge Development

For this challenge I created a simple python script. <br/>
```py
import random, os

def switch_characters(input_str):
    # dictionary to store letter mapping
    char_map = {}

    # generate random order for letters A-J
    letters = [chr(i) for i in range(65, 75)]
    random.shuffle(letters)

    # map numbers 0-9 to letters A-J (for UUID)
    for i in range(10):
        char_map[str(i)] = letters[i]

    output_str = ''
    for char in input_str:
        if char.isalpha() or char.isdigit():
            if char.isdigit():
                output_str += char_map[char]
            elif char.isalpha() and char.lower() not in char_map:
                new_char = char
                while new_char == char or new_char.lower() in char_map.values():
                    new_char = chr(random.randint(65, 90)) if char.isupper() else chr(random.randint(97, 122))
                char_map[char.lower()] = new_char.lower() if char.islower() else new_char.upper()
                output_str += char_map[char.lower()] if char.islower() else char_map[char.lower()].upper()
            else:
                output_str += char_map.get(char.lower(), char) if char.isalpha() else char
        elif char == '{':
            output_str += 'T'
        elif char == '}':
            output_str += 'X'
        elif char == '-':
            output_str += 'Q'
        else:
            output_str += char

    return output_str

input = f"""emergency situation!
apparently an agent of ours was hacked, he testified that he was in the process of transmitting an important piece of evidence.
according to another witness the flag th{{{os.environ['FLAG']}}} was leaked.

the numbers present in the flag follow this mapping:
zero corresponds to 0, one is mapped to 1 and two may be correlated with 2
three is 3, four is hidden as 4, five is connected to 5
six looks like 6, seven may be 7, eight should be 8 and nine is associated with 9
the left curved curly brace is {{, the right curved curly brace is }} and the hyphen is connected to -"""

with open('output', 'w') as file: 
    file.write(switch_characters(input))
```

The script above simple takes our input which contains the imported flag and maps every character in the provided input to another random character. <br/>
This is an implementation of a simple substitution cipher. Essentially I used the `random` builtin library from python to generate a random number between `97` and `122` which in ASCII are lowercase letters. <br/>
I also check if the letters were already mapped to another, this way every letter gets mapped to only 1 other letter. <br/>
The numbers are mapped to uppercase letters together with special chars of the flag like `{`, `}`, `-`. Using this I was able to completely hide the flag syntax within the output. <br/>
After the input was encrypted with the substitution cipher it will be written to a file. <br/>

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
ARG FLAG
ENV FLAG=${FLAG}
WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

RUN chmod +x initiate.sh

CMD ["./initiate.sh"]
```

The dockerfile sets up a simple python environment and imports the flag as envvar. <br/>
The `./initiate.sh` will execute the substitution cipher script once and than host the webservice to provide the output of the subsitution cipher. <br/>
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

if __name__ == '__main__':
    app.run(host='0.0.0.0')
```

The `Flask` service above provides only the output of the encryption script and not the script itself as this is supposed to be a black-box challenge. <br/>
The inbuild Flask function `send_from_directory` is able to load files from the container and therefore provide the generated file. <br/>