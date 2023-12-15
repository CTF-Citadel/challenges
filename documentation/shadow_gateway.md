# Shadow Gateway

> [!NOTE]
>
> When brainstorming I got the idea of a simple `Command-Injection`. <br/>
> Only command injection would be a bit little so I also wanted to add maybe some privilege escalation and also hash cracking.

## Challenge Development

> [!NOTE]
> 
> For a better user experience every CTF challenge needs some kind of storyline. <br/>
> In this challenge I tried to build the storyline around some kind of hackergroup which obtained data.

Starting off I created the system archtiecture with `docker-compose.yml`. <br/>
```yml
version: '3.9'

services:
  web:
    image: nginx:latest
    ports:
      - '80:80'
    volumes:
      - ./web_files:/var/www/html
      - ./nginx.conf:/etc/nginx/conf.d/default.conf
    links:
      - php-fpm
    command: ["/bin/sh", "-c", "nginx -g 'daemon off;'"]
  php-fpm:
    build:
      context: .  
      dockerfile: Dockerfile_php  
    volumes:
      - ./instructions.txt:/home/h4ckt1v1st/instructions.txt
      - ./web_files:/var/www/html
    ports:
      - '22:22'
    environment:
      - flag=${flag}
```

In this `yaml` file I created 2 different containers 1 for `PHP` and `Nginx`. <br/>
The challenge itself is running only on the `PHP` container but the nginx container is elevated to host the actual website for the `PHP` code. <br/>
The `FLAG` is being loaded via environment variable. <br/> 

In the Dockerfile for the PHP container I specfiy the details for the actual challenge. <br/>
```Dockerfile
# Initializing docker image 
FROM php:8-fpm

# Set permissions for anyone to read `/etc/shadow`
RUN chmod 644 /etc/shadow

# Create Repo for web interface
RUN mkdir /opt/filestash

# Copy fake documents for storyline
COPY confidental_document.txt /opt/filestash/confidental_document.txt

# Copy entrypoint script for flag initialization
COPY entrypoint.sh /usr/local/bin/entrypoint.sh

# make executable
RUN chmod +x /usr/local/bin/entrypoint.sh

# Create random documents for storyline
RUN touch /opt/filestash/hacking_guide.md \
----------------------------------------------------
    touch /opt/filestash/BlackHatHandbook.pdf 

# Edit permissions
RUN chmod -R +r /opt/filestash

# Add user with password 
RUN if ! id -u h4ckt1v1st > /dev/null 2>&1; then \
        useradd -m -s /bin/bash h4ckt1v1st \
        && echo 'h4ckt1v1st:lekkerding' | chpasswd; \
    fi

# Install Binary for Privilege Escalation
RUN apt-get update && apt-get install -y openssh-server sudo && apt-get install -y vim

# Set elevated permissions for Binary
RUN echo "h4ckt1v1st ALL=(root) NOPASSWD: /usr/bin/vim" >> /etc/sudoers

RUN mkdir /var/run/sshd

# Edit ssh perms for root ssh login
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# Execute entrypoint script
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

# Start container and enable php
CMD ["/bin/bash", "-c", "/usr/sbin/sshd && php-fpm"]
```

This docker-script creates fake documents for the storyline. <br/>
Furthermore it creates the user, downloads the binary and sets permissions for those. <br/>
Using the entrypoitn script I set the flag in the container. <br/>
```sh
#!/bin/bash

mkdir /root/ && touch /root/goldnugget.txt

echo $flag > /root/goldnugget.txt

/usr/sbin/sshd
php-fpm
```

This entrypoint script loads the flag into `/root/goldnugget.txt` which is the final task of this challenge. <br/>

The nginx server is setup to redirect any requests to the `PHP` container. <br/>
```conf
server {
    index index.php;
    server_name shadowGateway;

    error_log /var/log/nginx/error.log;
    access_log /var/log/nginx/access.log;
    root /var/www/html;

    error_page 403 /403.html;
    location /403.html {
        internal;
        allow all;
    }

    location / {
    index index.php;

    if ($http_x_forwarded_for !~* "^192\.168\.1\..+") {
        return 403;
    }
    }

    location ~ \.php$ {
        try_files $uri =404;
        fastcgi_split_path_info ^(.+\.php)(/.+)$;
        fastcgi_pass php-fpm:9000;
        fastcgi_index index.php;
        include fastcgi_params;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        fastcgi_param PATH_INFO $fastcgi_path_info;
    }
}
```

In the `nginx.conf` we can see that the nginx basically acts as a proxy. <br/>
In the `index.php` the only important part is the php code in the file. <br/>
```php
<?php
if ($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST["crypto_code"])) {
    $userInput = $_POST["crypto_code"];

    $searchResults = shell_exec("ls /opt/filestash/ | grep " $userInput);
}
?>
```

This is the critical vulnerability which just executes `ls /opt/filestash/ | grep $userInput` in the shell. <br/>
The purpose of this code is that it allwos arbitrary code execution because it doesn't sanitize the input and directly passes it to the shell. <br/>

The next vulnerability is the elevated permission on `/etc/shadow` which is being created in the Dockerfile. <br/>

The next vulnerability is the elevated permission on the `/usr/bin/vim` binary. 

This summarizes every vulnerabiltiy being initiated in the deployment process.









