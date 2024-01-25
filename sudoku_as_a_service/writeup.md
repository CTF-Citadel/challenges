# Sudoku as a Service - SaaS

## Description
```
Are you able to solve all my Sudoku-Puzzles in under 10 seconds?

The service does only accept the format below:
[[2, 8, 3, 5, 1, 4, 6, 7, 9], 
 [6, 5, 9, 2, 3, 7, 1, 8, 4], 
 [1, 7, 4, 8, 6, 9, 2, 5, 3], 
 [4, 3, 1, 9, 5, 2, 8, 6, 7], 
 [8, 6, 7, 1, 4, 3, 9, 2, 5], 
 [9, 2, 5, 6, 7, 8, 3, 4, 1], 
 [5, 4, 6, 3, 8, 1, 7, 9, 2], 
 [3, 9, 8, 7, 2, 5, 4, 1, 6], 
 [7, 1, 2, 4, 9, 6, 5, 3, 8]]
```

## Writeup

Taking a look at the service I connected to using netcat. <br/>
```sh
kali@kali nc 127.0.0.1 1337
Welcome challenger! Are you fast enough to solve all my Sudokus?

Sudoku 1/50:
. . . . 4 . 9 8 .
. . . . . . 1 2 .
. . . . 3 . . . .
. . . 5 . 8 6 4 1
. 1 . . . . . 5 .
. . . 4 . 6 . 3 .
. . . . . . 4 . 2
. . . . . . . . .
. . 9 . . 3 . . 6

123
Wrong Sudoku!
```

Looking at this anybody should know that we need to make a script to automatically read the sudokus, solve them and send them back in the correct format. <br/>
For this purpose I wrote a small python script. <br/>
```py
import socket, json

# Function to solve empty Sudoku from Server
def solve_sudoku_string(sudoku_str):
    def is_valid_move(sudoku, row, col, num):
        # Check if 'num' is not in the same row and column
        if num in sudoku[row] or num in [sudoku[i][col] for i in range(9)]:
            return False

        # Check if 'num' is not in the 3x3 subgrid
        subgrid_row, subgrid_col = 3 * (row // 3), 3 * (col // 3)
        return num not in [sudoku[subgrid_row + i][subgrid_col + j] for i in range(3) for j in range(3)]

    def find_empty_cell(sudoku):
        for i in range(9):
            for j in range(9):
                if sudoku[i][j] == '.':
                    return (i, j)  # Return the coordinates of an empty cell
        return None  # Return None if no empty cell is found

    def solve_sudoku(sudoku):
        empty_cell = find_empty_cell(sudoku)
        if not empty_cell:
            return True  # Puzzle solved

        row, col = empty_cell
        for num in range(1, 10):
            if is_valid_move(sudoku, row, col, num):
                sudoku[row][col] = num

                if solve_sudoku(sudoku):
                    return True  # Continue solving

                sudoku[row][col] = '.'  # Backtrack if the solution is not found

        return False  # No solution found

    def parse_sudoku_string(sudoku_str):
        lines = sudoku_str.strip().split('\n')
        return [[int(num) if num.isdigit() else '.' for num in line.split()] for line in lines]

    # Parse the input Sudoku string
    initial_sudoku = parse_sudoku_string(sudoku_str)

    # Solve the Sudoku
    solve_sudoku(initial_sudoku)

    # Return the solved Sudoku
    return initial_sudoku

def main():
    # Connect to socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("127.0.0.1", 1337))
        found_flag = False 

        while True:
            data = s.recv(1024).decode()
            print(data)

            # Check if Flag was found
            if "TH{" in data:
                print(f'\nFlag: {data}')
                found_flag = True
                break

            # Check if we got Sudoku in server response
            if not found_flag and '. ' in data:
                solved_sudoku = solve_sudoku_string(data)

                # if a solution is found, send it back to server
                if solved_sudoku:
                    sudoku_json = json.dumps(solved_sudoku)
                    print(f'Solved Sudoku:\n')
                    print(sudoku_json)
                    print('\n')

                    s.send(sudoku_json.encode())

if __name__ == "__main__":
    main()
``` 

Executing this script I automatically solve the sudokus and send them back in under `10` seconds as stated in the challenge description. <br/>
```sh
kali@kali python3 test.py 
Welcome challenger! Are you fast enough to solve all my Sudokus?


Sudoku 1/50:

. 8 . . . . . . .
. . . . . . . . .
1 . 4 . 6 9 2 . .
4 . . . . 2 . . 7
. . . 1 . . . . .
. . . . . 8 . . .
5 . . . 8 . . . .
. 9 . 7 2 . 4 . .
. . . 4 . 6 . 3 8

Solved Sudoku:

[[2, 8, 3, 5, 1, 4, 6, 7, 9], [6, 5, 9, 2, 3, 7, 1, 8, 4], [1, 7, 4, 8, 6, 9, 2, 5, 3], [4, 3, 1, 9, 5, 2, 8, 6, 7], [8, 6, 7, 1, 4, 3, 9, 2, 5], [9, 2, 5, 6, 7, 8, 3, 4, 1], [5, 4, 6, 3, 8, 1, 7, 9, 2], [3, 9, 8, 7, 2, 5, 4, 1, 6], [7, 1, 2, 4, 9, 6, 5, 3, 8]]

---------------------------------------------------------------------------------------------

Sudoku 50/50:

. 2 . 8 . . 9 . .
. 9 . . . . . . .
. . 1 . . 4 . . .
. . . 3 . . . . 8
. . . . . 8 5 6 9
. 7 8 . . 9 . . .
. . . . . . . . .
. 4 7 . 2 . . . 3
8 . . . 9 . . . .

Solved Sudoku:

[[3, 2, 4, 8, 1, 5, 9, 7, 6], [5, 9, 6, 2, 3, 7, 1, 8, 4], [7, 8, 1, 9, 6, 4, 2, 3, 5], [9, 6, 5, 3, 4, 2, 7, 1, 8], [4, 3, 2, 1, 7, 8, 5, 6, 9], [1, 7, 8, 6, 5, 9, 3, 4, 2], [2, 1, 9, 4, 8, 3, 6, 5, 7], [6, 4, 7, 5, 2, 1, 8, 9, 3], [8, 5, 3, 7, 9, 6, 4, 2, 1]]


TH{554943de-caef-47cf-8024-661b5b5c56fd}
```

Solving `50` Sudokus in a row solves this challenge and concludes this writeup.  