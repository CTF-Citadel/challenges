# Use a base image with necessary tools
FROM ubuntu:latest
ARG FLAG
ENV FLAG=${FLAG}
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

CMD ["/bin/bash", "/app/script.sh"]
