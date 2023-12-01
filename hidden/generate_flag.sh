#!/bin/bash

# Generate a random UUID
flag_uuid=$(uuidgen)

# Create the flag with the desired format
flag="TH{$flag_uuid}"

# Create the text file with the generated flag
echo "$flag" > goldnugget.txt

# Specify the passphrase for steghide
passphrase="Password"

# Hide the text file in the image using steghide with the specified passphrase
steghide embed -cf wood.jpg -ef goldnugget.txt --passphrase "$passphrase"
# The "--passphrase" option is used to provide the passphrase directly to steghide.


# Install nginx
apt-get update
apt-get install -y nginx

# Set permissions for the files
chmod 644 /app/wood.jpg /app/goldnugget.txt

# Configure nginx to serve only wood.jpg and block access to goldnugget.txt
echo "server {
  listen 80;
  server_name localhost;
  location / {
    root /app;
    index wood.jpg;
    try_files \$uri \$uri/ =404;
  }
  location = /goldnugget.txt {
    deny all;
  }
}" > /etc/nginx/sites-available/default

# Start nginx
nginx -g 'daemon off;'
