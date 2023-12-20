# Hidden

## Objective
Participants must decipher a flag concealed within an image using steghide, a tool for hiding and extracting data in various file types. The challenge incorporates scripting to generate a random flag, embed it within an image, and configure an Nginx web server to selectively serve the concealed image while restricting access to certain files.

## Image Creation
To create the image i used the Photoshop Ai and prompted it create an image with a old looking wood background and add Letters:

![image](https://github.com/CTF-Citadel/challenges/assets/115781703/130bd9c6-9eca-446e-8cba-a652e9798f5b)



## Challenge Components

### 1. Scripting (`generate_flag.sh`)
- Generates a random UUID to create a unique flag.
- Constructs the flag in a specific format.
- Creates a text file containing the generated flag.
- Uses steghide to embed the text file within an image.
- Installs Nginx, configures it to serve the image exclusively, and blocks access to specific files.

### 2. Docker Image (`Dockerfile`)
- Installs steghide, Python 3, and uuid-runtime within a Ubuntu base image.
- Copies the image and script into the Docker container.
- Sets the working directory, makes the script executable, and exposes port 80.

### 3. Docker Compose (`docker-compose.yml`)
- Defines a Docker service using the created Docker image.
- Maps port 80 on the host to port 80 on the container.


## 1. `generate_flag.sh` Shell Script

**Purpose:**
This script is designed to generate a random UUID, create a flag in a specified format, hide the flag within an image using steghide, and configure an nginx server to serve the image while restricting access to certain files.

**Key Steps:**

1. **Create a Text File with the Generated Flag:**

   ```sh
   echo "TH{$flag}" > goldnugget.txt
   ```
Creates a text file named goldnugget.txt and writes the generated flag passed by environment variable into it.


2. **Hide the Text File in the Image using Steghide:**

    ```sh
   steghide embed -cf wood.jpg -ef goldnugget.txt --passphrase "$passphrase"
    ```
This line uses steghide to embed the text file (goldnugget.txt) within the image (wood.jpg) using a specified passphrase.


3. **Install Nginx:**

    ```sh
   Copy code
   apt-get update
   apt-get install -y nginx
    ```
Update the package list and install the Nginx web server.


5. **Set Permissions for Files:**

    ```sh
   Copy code
   chmod 644 /app/wood.jpg /app/goldnugget.txt
    ```
This line sets permissions for the image and text file to read and write.


6. **Configure Nginx to Serve Only Wood.jpg and Block Access:**

  ```sh
  Copy code
  echo "server {
  # Nginx configuration
  }" > /etc/nginx/sites-available/default
  ```
The script generates an Nginx configuration to serve only the image (wood.jpg) and block access to specific files (goldnugget.txt, generate_flag.sh).
