from random import sample


## Check format

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


## For solving sudokus

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


## For creating sudokus

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


## For checkign if sent back Sudoku is valid

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