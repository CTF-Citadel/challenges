# Challenge Overview: Steganographic Flag Hunt

## Objective
Participants must decipher a flag concealed within an image using steghide, a tool for hiding and extracting data in various file types. The challenge incorporates scripting to generate a random flag, embed it within an image, and configure an Nginx web server to selectively serve the concealed image while restricting access to certain files.

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
- Maps port 8080 on the host to port 80 on the container.

## 1. `generate_flag.sh` Shell Script

**Purpose:**
This script is designed to generate a random UUID, create a flag in a specified format, hide the flag within an image using steghide, and configure an nginx server to serve the image while restricting access to certain files.

**Key Steps:**


2. **Create the Flag:**

   ```bash
   flag="TH{$flag}"

This line constructs the flag with a desired format and assigns it to the variable flag.

3. **Create a Text File with the Generated Flag:**

   ```bash
   echo "$flag" > goldnugget.txt

This line creates a text file named goldnugget.txt and writes the generated flag into it.

Hide the Text File in the Image using Steghide:

bash
steghide embed -cf wood.jpg -ef goldnugget.txt --passphrase "$passphrase"
This line uses steghide to embed the text file (goldnugget.txt) within the image (wood.jpg) using a specified passphrase.

Install Nginx:

bash
Copy code
apt-get update
apt-get install -y nginx
Update the package list and install the Nginx web server.

Set Permissions for Files:

bash
Copy code
chmod 644 /app/wood.jpg /app/goldnugget.txt
This line sets permissions for the image and text file to read and write.

Configure Nginx to Serve Only Wood.jpg and Block Access:

bash
Copy code
echo "server {
  # Nginx configuration
}" > /etc/nginx/sites-available/default
The script generates an Nginx configuration to serve only the image (wood.jpg) and block access to specific files (goldnugget.txt, generate_flag.sh).

Start Nginx:

bash
Copy code
nginx -g 'daemon off;'
Start the Nginx server in the foreground.

csharp
Copy code

Copy this Markdown content into a file with a `.md` extension for proper for
