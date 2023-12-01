FROM ubuntu:latest

# Install steghide, python3, and uuid-runtime
RUN apt-get update && \
    apt-get install -y steghide python3 uuid-runtime && \
    rm -rf /var/lib/apt/lists/*

# Copy your image and script to the container
COPY wood.jpg /app/wood.jpg
COPY generate_flag.sh /app/generate_flag.sh

# Set working directory
WORKDIR /app

# Make the script executable
RUN chmod +x generate_flag.sh

# Expose the port used by the web server
EXPOSE 80

# Entry point command
CMD ["./generate_flag.sh"]
