import os, socket, time
from sudoku import *

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

        # Set max time for client to respond to 5 sec
        client_socket.settimeout(10)

        # Initiate counter
        count = 1

        # Loop Sending sudokus
        while count < 50:
            client_socket.send(f'Sudoku {count}/50:\n'.encode('utf-8'))

            # Generate random Sudoku
            solved_sudoku = generate_sudoku()

            # Empty Sudoku spots
            random_sudoku = prepare_sudoku(solved_sudoku)

            client_socket.send(random_sudoku.encode('utf-8'))

            data = client_socket.recv(1024)
            decoded_data = data.decode('utf-8')

            if is_valid_input(decoded_data) == False:
                break

            # Format input to readable sudoku
            rows = random_sudoku.strip().split('\n')
            sudoku_grid = [[cell if cell != '.' else '.' for cell in row.split()] for row in rows]

            check = check_sudoku_mapping(eval(decoded_data), sudoku_grid)

            # Check if Client Sudoku is valid
            if not check[0]:
                client_socket.send('Wrong format or wrong sudoku solution!'.encode('utf-8'))
                client_socket.close()

            # Adding counter for loop
            count += 1

            time.sleep(1)

        # Send flag if client successfully solved 50 sudokus
        if count == 50:
            client_socket.send(flag.encode('utf-8'))
        else:
            client_socket.send('Wrong Sudoku!'.encode('utf-8')) 

        client_socket.close()

    except socket.timeout:
        client_socket.send('Timeout: No response received within 10 seconds'.encode('utf-8')) 
        client_socket.close() 

    except:
        client_socket.close()