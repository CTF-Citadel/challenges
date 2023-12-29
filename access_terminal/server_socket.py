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
