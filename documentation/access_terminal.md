# Access Terminal

> This is a pretty basic binary exploitation challenge that utilizes
> a method known as return address overwriting, variations of which
> can be found in many CTF competitions

## Overview

```
I found this self written authentication service that protects my friend' server terminal.

He told me he wrote it in C and copied most of the code from ChatGPT but ensured me that it is absolutely bullet-proof, or is it?
```

### What do we want to achieve

As hintend in the Overview text of this challenge, we clearly need to find and exploit some kind of vulnerability in the "self-written authentication" service.

## Creation

This challenge only needs a few basic things to get up and running.

### Preparing a properly vulnerable C program

The C program doesnt need to do much, other than having a function that *does* do much.

It basically just needs to read and print our flag somehow (in this case from and env-var called `$FLAG`) and be **out of scope** and **never called**.

```c
#include <stdio.h>
#include <stdlib.h>

void accessTerminal()
{
  const char *flag = getenv("FLAG");

  puts("Welcome to my terminal!");
  if (flag == NULL) {
    printf("No Flag defined \n");
    fflush(stdout);
    return 1;
  }
  else {
    printf("The Flag is: %s \n",flag);
    fflush(stdout);
  }
  return;
}

int main()
{
  start();
  puts("Not so easy!");
  fflush(stdout);
  return 0;
}

void start()
{
  char input [16];
  printf("%p\n",start);
  fflush(stdout);
  puts("Tell me the access word:");
  fflush(stdout);
  scanf("%s",input);
  return;
}
```

The `accessTerminal()` function can be reached in this case, by exploiting the vulnerable `scanf()` function to overwrite the return address.

This can easily be observed when viewing the raw binary in f.E. Ghidra or other Disassemblers.

```c
// ...
void start()
{
  // ...
  scanf("%s",input);
  return;
}
```

### Writing the Server-Side Socket

Since the actual binary is deployed in a docker container, so we can generate dynamic flags on the fly, we need a helper socket that relays user standard input to
our actual program.

One of the most basic ways to do this can be seen below.

```py
from socket import socket, AF_INET, SOCK_STREAM
from subprocess import Popen, PIPE
from os import getenv

FLAG = getenv("FLAG")


def start_listener():
    server = socket(AF_INET, SOCK_STREAM)
    server.bind(("0.0.0.0", 1337))
    server.listen(5)
    while True:
        client, addr = server.accept()
        print(f"Accepted connection from {addr}")

        try:
            handle_connect(client)
        except Exception as e:
            print(f"Error handling client: {e}")
        finally:
            client.close()


def handle_connect(peer: socket):
    program = Popen(["./server"], stdin=PIPE, stdout=PIPE, env={"FLAG": FLAG})

    output = program.stdout.readline()
    peer.sendall(output)
    output = program.stdout.readline()
    peer.sendall(output)

    while True:
        data = peer.recv(1024)
        if not data:
            break
        new_output, _ = program.communicate(input=data)
        peer.sendall(new_output)

    program.stdin.close()
    program.stdout.close()
    program.wait()


if __name__ == "__main__":
    start_listener()
```

To put it simply, this program simply starts a socket on port 1337, then waits for clients to connect to it.

Once a client connects, we can execute the binary and present the user with the first data it spits out to us.

```py
# ...
def handle_connect(peer: socket):
    program = Popen(["./server"], stdin=PIPE, stdout=PIPE, env={"FLAG": FLAG})

    output = program.stdout.readline()
    peer.sendall(output)
    output = program.stdout.readline()
    peer.sendall(output)
# ...
```

In this case it is exactly two lines, so we do it twice.

After that we can process whatever the user inputs and send it to the attached subprocess.

This is repeated until the user eventually inputs the correct overflow bytes to get to the return address of the function that reads and prints the flag.

On occasions where the underlying program segfaults or crashes, the socket is closed.

```py
# ...
while True:
        data = peer.recv(1024)
        if not data:
            break
        new_output, _ = program.communicate(input=data)
        peer.sendall(new_output)

    program.stdin.close()
    program.stdout.close()
    program.wait()
# ...
```

### Writing a `Dockerfile` and `docker-compose.yaml`

The Dockerfile is pretty simple since it only needs to execute our simple python script and house our binary.

```docker
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
```

The interesting bit may be the compilation of the C binary. Which is done in a way that stack-smashing detection and variable base addresse are turned of.

This makes exploitation a lot easier and should only be done in cases of f.E. CTF competitions.

```bash
# ...
RUN gcc -fno-stack-protector -no-pie server.c -o server
# ...
```

The compose file is simple and should need no further explanation

```yaml
version: "3"

services:
  socket-app:
    build: .
    environment:
      FLAG: ${FLAG}
    ports:
      - "8080:1337"
    restart: always
```
