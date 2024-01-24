import os, socket, time
from sudoku import generate_sudoku, prepare_sudoku

# Build flag from env var
flag = "TH{" + str(os.environ.get("FLAG")) + "}"

# Initiate Socket 
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("0.0.0.0", 1337))
server_socket.listen()

while True:
    try:
        client_socket, client_address = server_socket.accept()

        client_socket.send('Welcome challenger! Are you fast enough to solve all my Sudokus?\n\n'.encode('utf-8'))

        # Initiate counter
        count = 1

        # Loop Sending sudokus
        while count < 50:
            client_socket.send(f'Sudoku {count}/50:\n'.encode('utf-8'))

            # Generate random Sudoku
            solved_sudoku = generate_sudoku()

            print(solved_sudoku)

            # Empty Sudoku spots
            random_sudoku = prepare_sudoku(solved_sudoku)

            print(random_sudoku)

            # Initiate empty vars
            message = ""
            output = {}

            client_socket.send(random_sudoku.encode('utf-8'))

            data = client_socket.recv(1024)
            decoded_data = client_socket.recv(1024).decode()

            # Loop through array to convert solved sudoku array to a dictionary
            for index, line in enumerate(random_sudoku):
                output[index] = line

            # Using eval to convert decoded string to an actual dictionary
            if eval(decoded_data) != output:
                client_socket.send('Wrong format or wrong sudoku solution!'.encode('utf-8'))
                client_socket.close()

            # Adding counter for loop
            count += 1

            time.sleep(1)

        # Send flag if client successfully solved 50 sudokus
        client_socket.send(flag.encode('utf-8'))
        client_socket.close()

    except:
        client_socket.close()