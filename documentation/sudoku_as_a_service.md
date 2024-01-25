# Sudoku as a Service

> [!NOTE]
>
> When doing a Sudoku I got the idea of a service which provides random Sudokus. <br/>
> The goal of this challenge is to make a script to solve 50 random sudokus fast enough to obtain the flag.

## Challenge Development

> [!NOTE]
> 
> This challenge was made with python and its' built-in library socket to provide a service which can generate random sudokus. <br/>

Starting off I created the system archtiecture with `docker-compose.yml`. <br/>
```yml
version: '3.9'

services:
  python:
    build:
      context: .
      args:
        FLAG: ${FLAG}
    ports:
      - "1337:1337"
```

For this challenge 1 container is enough because we only have 2 python scripts. <br/>
1 python script for the purpose of socket connections and the other script to generate random sudokus and check solutions from the client. <br/>
The dockerfile below creates the container with python installed, loads the flag from an environment variable and instantly launches the socket service on port `1337`. <br/>
```docker
FROM python:3.8-slim

WORKDIR /app

COPY . /app

ARG FLAG
ENV FLAG=${FLAG}

CMD ["python", "service.py"]
```

### Most important functions

The function below checks if the client input is actually a valid sudoku. <br/>
```py
def is_valid_input(input_string):
    try:
        # Attempt to evaluate the input string
        result = eval(input_string)
        
        # Check if the result is a list
        if not isinstance(result, list):
            return False
        
        # Check if each element in the list is also a list
        for sublist in result:
            if not isinstance(sublist, list):
                return False
        
        # Check if each sublist has the same length
        sublist_length = len(result[0])
        for sublist in result:
            if len(sublist) != sublist_length:
                return False
        
        return True
        
    except Exception as e:
        # If any error occurs during evaluation or validation, return False
        return False
```

The functions below are made to sovle an empty sudoku which is needed by another function to check the uniquenes of a sudoku. <br/>
```py
def is_valid(board, row, col, num):
    # Check if the number can be placed in the given row and column
    for i in range(9):
        if board[row][i] == num or board[i][col] == num or board[3 * (row // 3) + i // 3][3 * (col // 3) + i % 3] == num:
            return False
    return True

def solve_sudoku(board):
    # Find empty location
    empty = find_empty_location(board)
    
    if not empty:
        return True  # Puzzle solved
    
    row, col = empty
    
    # Try placing a number from 1 to 9
    for num in range(1, 10):
        if is_valid(board, row, col, num):
            # Place the number if it's valid
            board[row][col] = num

            # Recursively try to solve the rest of the puzzle
            if solve_sudoku(board):
                return True

            # If placing the number didn't lead to a solution, backtrack
            board[row][col] = 0

    # No number can be placed at this location, backtrack
    return False

def find_empty_location(board):
    # Find the first empty location (zero) in the board
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)
    return None  # If no empty location is found, puzzle is solved
```

The functions below are made for the sole purpose of generating unique sudokus. <br/>
Those functions were altered from code I found [online](https://stackoverflow.com/questions/45471152/how-to-create-a-sudoku-puzzle-in-python) to create random sudokus each time. <br/>
```py
def generate_sudoku():
    while True:
        base  = 3
        side  = base*base

        # pattern for a baseline valid solution
        def pattern(r, c): return (base * (r % base) + r // base + c) % side

        # randomize rows, columns and numbers (of valid base pattern)
        def shuffle(s): return sample(s, len(s)) 
        rBase = range(base) 
        rows  = [g * base + r for g in shuffle(rBase) for r in shuffle(rBase)]
        cols  = [g * base + c for g in shuffle(rBase) for c in shuffle(rBase)]
        nums  = shuffle(range(1, base * base + 1))

        # produce board using randomized baseline pattern
        board = [[nums[pattern(r, c)] for c in cols] for r in rows]

        # Check if the generated Sudoku has a unique solution
        if check_uniqueness(board):
            return board

def prepare_sudoku(board):
    base = 3
    side = base * base

    squares = side * side
    empties = squares * 3 // 4
    for p in sample(range(squares), empties):
        board[p // side][p % side] = 0

    numSize = len(str(side))
    sudoku_str = ""
    for line in board:
        sudoku_str += " ".join(f"{n or '.':{numSize}}" for n in line) + "\n"

    return sudoku_str

def check_uniqueness(sudoku):
    # Copy the original sudoku to avoid modifying it
    sudoku_copy = [row[:] for row in sudoku]

    # Try solving the Sudoku and check if there is a unique solution
    return solve_sudoku(sudoku_copy)
```

The function below is probably the most important one as it checks a users solution for a sudoku and therefore is the main function for this challenge to obtain the flag. <br/> 
```py
def check_sudoku_mapping(solved_sudoku, empty_sudoku):
    print(f'Sudoku from Client:\n{solved_sudoku}\n')
    print(f'Empty Sudoku:\n{empty_sudoku}')

    def is_valid_sudoku(sudoku):
        # Check rows and columns
        for i in range(9):
            row = sudoku[i]
            col = [sudoku[j][i] for j in range(9)]
            if len(set(row)) != 9 or len(set(col)) != 9:
                return False

        # Check 3x3 subgrids
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                subgrid = [sudoku[x][y] for x in range(i, i + 3) for y in range(j, j + 3)]
                if len(set(subgrid)) != 9:
                    return False

        return True

    # Check if solved Sudoku is valid
    if not is_valid_sudoku(solved_sudoku):
        return False, "Solved Sudoku is not valid."

    # Check if empty Sudoku correctly maps to solved Sudoku
    for i in range(9):
        for j in range(9):
            if empty_sudoku[i][j] != '.':
                if empty_sudoku[i][j] != str(solved_sudoku[i][j]):
                    return False, "Empty Sudoku does not map correctly to the solved Sudoku."

    return True, "Sudoku mapping is valid."
```

### Socket Service

The python script below opens a socket on port `1337` and than waits for clients to connect. <br/>
It uses the functions described above to provide random sudokus, check the solutions and pass another random sudoku. If a user passes 50 rounds of random sudokus he obtains the flag. <br/>
```py
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
```




