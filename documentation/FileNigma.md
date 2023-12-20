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

# Function to generate10,000 different letters
def generate_large_random_string():
    content = ''

    while len(content) < 10000:
        num_chars_in_paragraph = random.randint(100, 500)  # Adjust the range as needed
        content += ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(num_chars_in_paragraph))
        
       
        if len(content) < 10000 and random.choice([True, False]):
            content += '\n\n'
    
    return content

directory = '/usr/local/apache2/htdocs'

# File creation
for i in range(1, 101):
    filename = os.path.join(directory, f'file_{i}.txt')

    if i == 1:
        content = generate_large_random_string()
    else:
        content = generate_large_random_string()

    with open(filename, 'w') as file:
        file.write(content)

chosen_file = os.path.join(directory, random.choice([f for f in os.listdir(directory) if f.endswith('.txt')]))

content = 'TH{' + flag + '}' + generate_large_random_string()

# Write the content to a random location in the file
with open(chosen_file, 'r') as file:
    file_content = file.read()

    # Choose a random position to insert the content
    insert_position = random.randint(0, len(file_content))

    updated_content = file_content[:insert_position] + content + file_content[insert_position:]

# Write the updated content back to the file
with open(chosen_file, 'w') as file:
    file.write(updated_content)
```

### Script Components

#### **Flag Retrieval**

```python
flag = os.environ.get('FLAG', 'default_value')
```
Retrieves the value of the environment variable FLAG. If the variable is not set, it defaults to 'default_value'.

#### **Randomized String Generation**

```python
def generate_large_random_string():
    content = ''

    while len(content) < 10000:
        num_chars_in_paragraph = random.randint(100, 500)  
        content += ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(num_chars_in_paragraph))
                if len(content) < 10000 and random.choice([True, False]):
            content += '\n\n'
    
    return content
```

- Function to generate a string with 10,000 different letters, numbers, and signs with random paragraphs.

- A while loop is employed to ensure that the generated string reaches a length of 10,000 characters.

  - Within the loop:

  - Randomly determines the number of characters in a paragraph (between 100 and 500).
  - Appends randomly chosen letters, numbers, and signs to the content.
  - Adds a paragraph break after a random amount of characters.

 
#### **File Creation Loop**

```python
for i in range(1, 101):
    filename = os.path.join(directory, f'file_{i}.txt')

    if i == 1:
        content = generate_large_random_string()
    else:
        content = generate_large_random_string()
    with open(filename, 'w') as file:
        file.write(content)
```

- Uses the generate_large_random_string function to create content for each file.
  
- The content for the first file is created with the flag format, while subsequent files have random content.


#### **Write Content into a Random File Position**

```python
  with open(filename, 'w') as file:
    file.write(content)

chosen_file = os.path.join(directory, random.choice([f for f in os.listdir(directory) if f.endswith('.txt')]))

content = 'TH{' + flag + '}' + generate_large_random_string()

with open(chosen_file, 'r') as file:
    file_content = file.read()
    insert_position = random.randint(0, len(file_content))
    updated_content = file_content[:insert_position] + content + file_content[insert_position:]

with open(chosen_file, 'w') as file:
    file.write(updated_content)
```

- Chooses a random file for the flag format to be written 
```python
chosen_file = os.path.join(directory, random.choice([f for f in os.listdir(directory) if f.endswith('.txt')]))
```

-  And writes the flag to a random position in the file so its not at the start of a file.
```python
with open(chosen_file, 'r') as file:
    file_content = file.read()
    insert_position = random.randint(0, len(file_content))
    updated_content = file_content[:insert_position] + content + file_content[insert_position:]
```

