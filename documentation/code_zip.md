# Access Terminal

> This is a very easy git forensics challenge that requires the
> player to know the basics of git, analyze the repository and
> use the correct series of commands to browse the git history

## Overview

```
Jake was just hired by a company who fired their former system administrator. He was very reluctant about giving out passwords to all the servers, but left a few code samples behind. 

Unfortunately its just some random python program that doesnt really do anything. If only there was a way to recover the password.
```

## Creation

This challenge relies on a single script that generates commits based on sample folders

### Writing the generator script

First we need to create a new repository and set our git config to arbitary values.

```bash
# init new repository
mkdir code/
cd code/
git init

# set arbitary name
git config --global user.name "bob"
git config --global user.email "bob@security.org"
```

After that we can start adding samples, stopping at the sample where we want to add our custom flag.

```bash
# phase 1
cp -r ../samples/phase1/* .
git add .
git commit -m "initial commit"
git commit --amend --date="Sat Feb 8 14:12 2019 +0100" --no-edit

# phase 2
cp -r ../samples/phase2/* .
# change to correct flag
sed -i 's/PLACEHOLDER/'"$FLAG"'/' lib/security.py
git add .
git commit -m "add security.py"
git commit --amend --date="Sun Feb 9 08:16 2019 +0100" --no-edit
```

The usage of `sed` is an easy way to substitute the placeholder password with the generated uuid. 

After that we add some more phases where we basically just add random cover-up code.

```bash
# phase 3
cp -r ../samples/phase3/* .
git add .
git commit -m "update security.py"
git commit --amend --date="Mon Feb 10 23:14 2019 +0100" --no-edit

# phase 4
cp -r ../samples/phase4/* .
git add .
git commit -m "add geometry.py"
git commit --amend --date="Tue Feb 11 11:32 2019 +0100" --no-edit

# phase 5
cp -r ../samples/phase5/* .
git add .
git commit -m "add shapes.py"
git commit --amend --date="Thu Feb 13 15:47 2019 +0100" --no-edit
```

We make sure to always change the date too, just for some more randomization, I guess.

Finally we zip up the repo and start the Python flask service, that provides this file to the player.

```bash
# zip the code
cd ..
zip -r code.zip code/

# run the program
python service.py
```

### Writing the File-Provider

This code is a standard flask app, which servers the only purpose of providing the generated `code.zip` file for download.

```py
from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

# Index page to provide files
@app.route('/')
def index():
    return render_template('index.html')

# endpoint to download code.zip
@app.route('/download/code.zip')
def download_output():
    return send_from_directory('.', 'code.zip', as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1337)

```

### Writing a `Dockerfile` and `docker-compose.yaml`

Simple Dockerfile that builds from python slim, installs `git` and `zip`, and finally runs the script.

```docker
FROM python:3.11-slim

WORKDIR /app

RUN apt update && \
    apt install -y git zip

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY templates/ ./templates
COPY samples/ ./samples
COPY service.py \
entrypoint.sh \
./

RUN chmod +x entrypoint.sh

ARG FLAG
ENV FLAG=${FLAG}

EXPOSE 1337

CMD ["./entrypoint.sh"]
```

The compose file is simple and should need no further explanation

```yaml
version: '3'

services:
  web:
    build:
      context: .
      args:
        FLAG: ${FLAG}
    ports:
      - "80:1337"
    restart: always
```
