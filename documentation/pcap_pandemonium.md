# Pcap Pandemonium

## Overview

This is a networking (and a tiny little bit forensic) challenge. The ctf participant has to find a hidden flag inside a `.pcapng` file. It is solvable with `strings` and a `grep` or you do it with your favorite pcap analysis tool.

## Creation of the pcap file

For this I needed some http traffic and a login form where I can submit some credentials. I chose `http://testphp.vulnweb.com/login.php` for this task.
Next, I need to get the UUID into the file. To automate this task, I use a file called `converter.sh`

```sh
#!/bin/bash

# Input file
input_file="./input.pcapng"

# Output file
output_file="/var/www/html/capture.pcapng"

echo "Flag: $FLAG"

# Generate a UUID with the format "TH{xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx}"
new_password="TH{${FLAG}}"

# Replace the password in the pcapng file and remove the trailing "test"
awk -v new_pass="$new_password" 'BEGIN {FS=OFS="="} $1=="uname" && $2=="test&pass" {print $1, $2, new_pass; next} {print}' $input_file > $output_file

echo "Password changed successfully to $new_password. Modified file: $output_file"

# Start Apache in the foreground
/usr/sbin/apache2ctl -D FOREGROUND
```

This returns a file called `capture.pcapng`. Now I just need to server the file to the user.

## Simple web service

I am using apache2 to serve the file via `/capture.pcapng`. 
This Dockerfile executes the converter.sh and starts the apache web server:

```Dockerfile
# Use a base image with necessary tools
FROM ubuntu:latest

# Update package lists and install required packages
RUN apt-get update && \
    apt-get install -y \
    tcpdump \
    apache2 \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy the input.pcapng file to the container
COPY input.pcapng /app/input.pcapng

# Copy the script and set it as executable
COPY converter.sh /app/script.sh
RUN chmod +x /app/script.sh

# Set the working directory
WORKDIR /app

# Start Apache and expose port 80
EXPOSE 80

# Define an environment variable for the new password
ENV FLAG=""

CMD ["/bin/bash", "/app/script.sh"]
```

To start the challenge and make it dynamically deployable, I use a compose file:

```yaml
version: '3'
services:
  web_service:
    build:
      context: .
      dockerfile: Dockerfile
    environment:
      - FLAG=${FLAG}
    ports:
      - "80:80"
```

Now the participant/user can access the url `URL/capture.pcapng` to download the file.
If you want to know how to solve the challenge, please go to the writeup.
