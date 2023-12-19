import os, socket

flag = "TH{" + str(os.environ.get("FLAG")) + "}"

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("0.0.0.0", 1337))
server_socket.listen()

while True:
    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address}")

    message = "Welcome Adventurer"
    client_socket.send(message.encode('utf-8'))

    data = client_socket.recv(1024)

client_socket.close()