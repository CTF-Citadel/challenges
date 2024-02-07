# Encased

> [!NOTE]
>
> To start off the `Reverse Engineering` category I had to make an easy challenge. <br/>
> For this purpose I created this challenge which is rather easy and can be solved with simple linux utility.

## Challenge Development

For this challenge I created a simple python script. <br/>
```py
import os, random, py_compile, string

flag = f'TH{{{os.getenv("FLAG")}}}'

# Created list for flag
listed_flag = list(flag)

rndm_num = random.randint(1, 100000000000)

# shuffle flag
random.seed(rndm_num)
random.shuffle(listed_flag)

# Function to write functions to output file
def write_functions(funcName, seed):
    file.write(f'def {funcName}(shuffled_list):\n\n')
    file.write(f'    random.seed({seed})\n\n')
    file.write(f'    indices = list(range(len(shuffled_list)))\n')
    file.write(f'    random.shuffle(indices)\n\n')
    file.write(f'    reversed_list = [None] * len(shuffled_list)\n')
    file.write(f'    for i, j in zip(indices, range(len(shuffled_list))):\n')
    file.write(f'        reversed_list[i] = shuffled_list[j]\n\n')
    file.write(f'    reversed_string = "".join(reversed_list)\n\n')
    file.write(f'    return reversed_string\n\n')

# Open output file to add content
with open('yeet.py', 'w') as file:
    file.write('import random\n\n')
    file.write(f'shuffled_input = {listed_flag}\n\n')

    # Generate fake functions
    for _ in range(1, 30):
        write_functions("".join(random.choice((str.upper, str.lower))(char) for char in "iknowsomeonewhodoesnotshower"), random.randint(1, 100000000000))

    # Actual function to solve challenge
    trueFuncName = "".join(random.choice((str.upper, str.lower))(char) for char in "iknowsomeonewh0doesnotshower")

    write_functions(trueFuncName, rndm_num)

    # Generate fake functions
    for _ in range(1, 30):
        write_functions("".join(random.choice((str.upper, str.lower))(char) for char in "iknowsomeonewhodoesnotshower"), random.randint(1, 100000000000))

    # hardcode password as main challenge
    file.write('password = input("Enter password: ")\n')
    file.write(f'if password == "{"".join(random.choice(string.ascii_letters + string.digits) for _ in range(20))}":\n')
    file.write(f'    print({trueFuncName}(shuffled_input))\n')
    file.write('else:\n')
    file.write('    print("Wrong Password!")\n\n')

    # Generate fake functions
    for _ in range(1, 30):
        write_functions("".join(random.choice((str.upper, str.lower))(char) for char in "iknowsomeonewhodoesnotshower"), random.randint(1, 100))

# Compile .py file to .pyc file
py_compile.compile("yeet.py")
```

To have dynamic flags I used read the environment variable `FLAG` which is imported during deployment. <br/>
I than created the function `write_functions(funcName, seed)` which basically creates a new function with certain paramters. <br/>
```py
def IKnowsOMeONeWhoDoeSnOtshOwer(shuffled_list):

    random.seed(84661192857)

    indices = list(range(len(shuffled_list)))
    random.shuffle(indices)

    reversed_list = [None] * len(shuffled_list)
    for i, j in zip(indices, range(len(shuffled_list))):
        reversed_list[i] = shuffled_list[j]

    reversed_string = "".join(reversed_list)

    return reversed_string
```

As you can see the created function may look like this. Here it is important to note that only 1 function has the correct seed to get the correct flag. <br/>
In the rest of the file we leverage the function `write_functions(funcName, seed)` to create a lot of fake functions but only 1 real useful function. <br/>
I than proceed to place an `input()` inside the script to ask the user for a password which is being generated randomly but can be read from the `.pyc` file with `strings`. <br/>

I used a simple docker-compose file to host a webservice. <br/>
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

This webservice is used to provide the files for the challenge. <br/>
```Dockerfile
FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

ARG FLAG
ENV FLAG=${FLAG}

RUN python3 /app/file_writer.py

CMD ["python", "service.py"]
```

In the dockerfile I setup a python environment and load the flag to generate the encrypted flag. <br/>
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
@app.route('/yeet')
def download_output():
    return send_from_directory('./__pycache__', 'yeet.cpython-38.pyc', as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
```

To host the webservice I use Flask and use the inbuild Flask function `send_from_directory` which is able to load files from the container. <br/>