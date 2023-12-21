# zipception

## Idea
> [!NOTE]
>I got this idea from last year's TopHack CTF, where there was a zipped folder within another zipped folder and so on. However, last year's challenge only had about 100 zipped folders nested within each other. Instead of using a script, everyone clicked through the folders until they reached the last one. For my challenge, I decided to increase the complexity by having 9999 nested folders. This way, the user would need to use a script, or it would take a very long time to navigate through the folders manually. Creating the script is not that difficult, and even if you don't know how, AI will help you with it, or you can do it manually. Therefore, the challenge is still easy.


## Overview
The challenge involves a Dockerfile that sets up a Flask web service in a Python environment, utilizing a script to generate nested zip files containing a flag, and a Docker Compose configuration to expose the service on port 80, allowing participants to download an encrypted flag from the web service.

```Dockerfile
FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

ARG FLAG
ENV FLAG=${FLAG}

RUN python3 /app/zip.py

CMD ["python", "service.py"]
```

The Dockerfile which is used to load the flag and install the requirements

```yml
version: '3.9'

services:
  web:
    build: .
    ports:
      - "80:5000"
```

The docker-compose.yml file to host the webservice for the files to be provided and to expose the port for the flask service

```python
from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

# Index page with login and signup links
@app.route('/')
def index():
    return render_template('index.html')

# endpoint to download encrypted flag
@app.route('/download_goldnugget_zip')
def download_output():
    return send_from_directory('.', 'goldnugget.zip', as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
```

The webservice is being hosted using Flask, which loads the files from the container using an inbuild function `send_from_directory`. 

```python
import os
import zipfile

def zip_file(input_file, output_zip):
    with zipfile.ZipFile(output_zip, 'w') as zipf:
        zipf.write(input_file, arcname=os.path.basename(input_file))

def generate_zip_files(input_text_file, output_zip, num_iterations, flag):
    # Create the goldnugget.txt file
    file_content = flag.encode("utf-8")
    with open(input_text_file, "wb") as file:
        file.write(file_content)

    for i in range(num_iterations):
        current_zip = f'zip{i}.zip'
        zip_file(input_text_file, current_zip)
        input_text_file = current_zip

    # Move the final zip file to the desired name
    os.rename(input_text_file, output_zip)

    # Remove intermediate zip files
    for i in range(num_iterations):
        current_zip = f'zip{i}.zip'
        if os.path.exists(current_zip):
            os.remove(current_zip)

def main():
    env_variable = os.getenv("FLAG")  # Updated to use "flag" as the environment variable

    # Set the flag for the file content
    flag = f"TH{{{env_variable}}}"

    input_text_file = 'goldnugget.txt'
    output_zip = 'goldnugget.zip'
    num_iterations = 9999

    generate_zip_files(input_text_file, output_zip, num_iterations, flag)

if __name__ == "__main__":
    main()
```

The script to create the goldnugget.txt file and zip it multiple times

```python
def zip_file(input_file, output_zip):
    with zipfile.ZipFile(output_zip, 'w') as zipf:
        zipf.write(input_file, arcname=os.path.basename(input_file))
```

- Creates a zip file containing the provided input file.
- Uses the zipfile module.


```python
def generate_zip_files(input_text_file, output_zip, num_iterations, flag):
    # Create the goldnugget.txt file
    file_content = flag.encode("utf-8")
    with open(input_text_file, "wb") as file:
        file.write(file_content)

    for i in range(num_iterations):
        current_zip = f'zip{i}.zip'
        zip_file(input_text_file, current_zip)
        input_text_file = current_zip
```

- Generates a series of nested zip files.
- Creates the initial 'goldnugget.txt' file with the specified flag content.
- Calls zip_file iteratively to create nested zip files.
- Renames the last zip file to the specified final output name.
- Removes intermediate zip files to maintain cleanliness.


```python
def main():
    env_variable = os.getenv("FLAG")  # Updated to use "flag" as the environment variable

    # Set the flag for the file content
    flag = f"TH{{{env_variable}}}"

    input_text_file = 'goldnugget.txt'
    output_zip = 'goldnugget.zip'
    num_iterations = 9999

    generate_zip_files(input_text_file, output_zip, num_iterations, flag)
```

- Retrieves the flag content from the "FLAG" environment variable.
- Sets default values for input and output filenames and the number of iterations.
- Calls generate_zip_files with specified parameters.
