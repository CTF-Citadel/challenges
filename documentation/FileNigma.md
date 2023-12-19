# FileNigma CTF Challenge Documentation

## Overview

Welcome to the "FileNigma"! In this Capture The Flag (CTF) challenge, participants are tasked with uncovering the location of a hidden flag within a cluster of files. The challenge is categorized as a simple MISC (Miscellaneous) challenge, and the objective is to connect to a provided IP and port, retrieve 100 files, and use the `grep` command to find the flag. The flag follows the format: `TH{UUID}`.

## Challenge Environment

### Docker Configuration

The challenge is hosted within a Docker container, ensuring a consistent environment for all participants. The Docker configuration consists of:

#### **DOCKERFILE**

```Dockerfile
FROM httpd:latest

WORKDIR /usr/local/apache2/htdocs

ARG FLAG=default_value

ENV FLAG=${FLAG}

COPY * /

RUN apt-get update && apt-get install -y python3

RUN rm /usr/local/apache2/htdocs/index.html

RUN python3 /func.py

CMD ["httpd", "-D", "FOREGROUND"]
```


#### **docker-compose.yml**

```yaml
Copy code
version: '3'

services:
  webserver:
    environment:
      - FLAG=${FLAG}
    build:
      context: .
      dockerfile: DOCKERFILE
      args:
        FLAG: ${FLAG}
    ports:
      - "80:80"
```

A web server is started on the port 80 and the func.py is executed so the files get provided when accessing the ip



## Python Script

The purpose of the script is to create 100 random text files containing 10000 random characters and hidding the flag into one of them, heres the script:

#### **func.py**

```python
import os
import random
import string
import uuid

flag = os.environ.get('FLAG', 'default_value')

# Function to generate a string with 10,000 different letters, numbers, and signs with random paragraphs
def generate_large_random_string():
    # ... (content generation logic)

# Directory to store the files inside the Docker container
directory = '/usr/local/apache2/htdocs'

# Create 100 files
for i in range(1, 101):
    filename = os.path.join(directory, f'file_{i}.txt')

    # For one file, use the specified format
    if i == 1:
        content = generate_large_random_string()
    else:
        content = generate_large_random_string()

    with open(filename, 'w') as file:
        file.write(content)

# Choose a random file
chosen_file = os.path.join(directory, random.choice([f for f in os.listdir(directory) if f.endswith('.txt')]))

# Generate the content for the chosen file
content = 'TH{' + flag + '}' + generate_large_random_string()

# Write the content to a random location in the file
with open(chosen_file, 'r') as file:
    file_content = file.read()

    # Choose a random position to insert the content
    insert_position = random.randint(0, len(file_content))

    # Insert the content at the chosen position
    updated_content = file_content[:insert_position] + content + file_content[insert_position:]

# Write the updated content back to the file
with open(chosen_file, 'w') as file:
    file.write(updated_content)
```
