#!/bin/bash

echo "TH{$flag}" > goldnugget.txt

passphrase="password123"

# Hide the text file in the image using steghide with the specified passphrase
steghide embed -cf wood.jpg -ef goldnugget.txt --passphrase "$passphrase"

apt-get update
apt-get install -y nginx

chmod 644 /app/wood.jpg /app/goldnugget.txt

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
  location = /generate_flag.sh {
    deny all;
  }
}" > /etc/nginx/sites-available/default

nginx -g 'daemon off;'
