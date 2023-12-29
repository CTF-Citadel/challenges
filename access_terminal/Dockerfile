FROM python:3.11-slim-bookworm

WORKDIR /app

# install gcc
RUN apt update && \
apt install -y gcc

# copy necessary files
COPY server.c \
server_socket.py \
./

# build the binary
RUN gcc -fno-stack-protector -no-pie server.c -o server

# run the socket
EXPOSE 1337
CMD ["python", "server_socket.py"]
