#!/usr/bin/python3
"""Script resolving the N queens puzzle"""

import sys  # Required for input grab


def nqueens_solver():
    """All-in-one N queens puzzle solver, requires an >=4 int as argument"""

# === Inner functions: Initialization helpers ===
    def init__ensure_valid_argument():
        """Ensures program is called with proper arguments to resolve puzzle"""

        if len(sys.argv) != 2:
            print("Please give a number for chess size matching number of queens!")
            print(sys.argv)
            exit(1)

        try:
            N = int(sys.argv[1])
        # TypeError cannot happen because sys module guarantees input to be string.
        except ValueError as e:
            print("N must be a number")
            exit(1)

        if N < 4:
            print("N must be at least 4")
            exit(1)

        return N


    def init__setup_state_registries(N: int):
        """Defines and set default values for the 'truth tables' lists & set"""

        # From the brainstorming we can infer several variables to hold "state".
        occupied_columns = [False for _ in range(N)]
        # Using "list creation by repetition" syntax
        occupied_upwards_diagonals = [False] * (2 * N - 1)

        # For those since the value can be negative we'll use a Set for now.
        #   Later I'll try to find how to use a truth table like the rest.
        occupied_downward_diagonals = set()

        # Index will represent line, Value the column for that queen.
        # Initializing at -1 because 0 is a "valid key" in that context.
        queens_positions = [-1] * N

        return (
            occupied_columns,
            occupied_upwards_diagonals,
            occupied_downward_diagonals,
            queens_positions
        )


    def is_safe_position(row_index, col_index):
        """Checks desired grid position is not used/threatened in any way"""
        # Check col not locked
        if occupied_columns[col_index]:
            return False
        # Check not across occupied downwards diagonal
        downwards_diag_code = row_index - col_index
        if downwards_diag_code in occupied_downward_diagonals:
            return False
        # Check not across occupied upwards diagonal
        upwards_diag_code = row_index + col_index
        if occupied_upwards_diagonals[upwards_diag_code]:
            return False
        return True


    def update_state_registries(row_index, col_index, mode):
        """Updates registries to set or unset a 'lock value'"""
        downwards_diag_code = row_index - col_index
        upwards_diag_code = row_index + col_index

        if mode == "unlock":
            occupied_columns[col_index] = False
            occupied_downward_diagonals.discard(downwards_diag_code)
            occupied_upwards_diagonals[upwards_diag_code] = False

        elif mode == "lock":
            occupied_columns[col_index] = True
            occupied_downward_diagonals.add(downwards_diag_code)
            occupied_upwards_diagonals[upwards_diag_code] = True

        else:
            raise ValueError("Only supported modes are 'lock' and 'unlock'")


    def lock_queen_position(row_index, col_index):
        """Sets the col for a queen in given row and locks related positions"""
        queens_positions[row_index] = col_index
        update_state_registries(row_index, col_index, "lock")


    def unlock_queen_position(row_index, col_index):
        """Forgets the col for a given queen and frees related positions"""
        queens_positions[row_index] = -1
        update_state_registries(row_index, col_index, "unlock")


    def backtrack():
        """"""
        nonlocal current_queen
        # Special syntax which allows inner function to MODIFY a parent var.
        current_queen -= 1
        if current_queen >= 0:
            update_state_registries(
                current_queen,
                queens_positions[current_queen],
                "unlock"
            )


    # Initializing everything we need to work
    N = init__ensure_valid_argument()
    (   # Beware that variable names match the ones in function, in same order!
        occupied_columns,
        occupied_upwards_diagonals,
        occupied_downward_diagonals,
        queens_positions
    ) = init__setup_state_registries(N)
    solutions = []

    # Starting exploration
    current_queen = 0
    while current_queen >= 0:
        if current_queen == N:
            # Means we found a valid solution, so save it and backtrack
            solutions.append([[r, c] for r, c in enumerate(queens_positions)])
            backtrack()
            continue

        # Computing starting positions for search.
        cr_row_idx = current_queen
        col_search_start = queens_positions[current_queen] + 1

        # Trying to find a valid col pos for current line insertion.
        cr_col_idx = next(
            (idx for idx in range(col_search_start, N)
            if is_safe_position(cr_row_idx, idx)),
            None
        )
        # Valid position found, we affect and go to next line.
        if cr_col_idx is not None:
            lock_queen_position(cr_row_idx, cr_col_idx)
            current_queen +=1
        # No valid position found meaning we need to backtrack and try
        #   with previous queen in next free col pos.
        else:
            queens_positions[current_queen] = -1
            backtrack()

    for solution in solutions:
        print(solution)



nqueens_solver()









# ===== Task instructions ====
# The N queens puzzle is the challenge of placing N non-attacking queens
# on an N×N chessboard. Write a program that solves the N queens problem.
# Usage: nqueens N
# If the user called the program with the wrong number of arguments, 
#   print Usage: nqueens N, followed by a new line, and exit with the status 1
# where N must be an integer greater or equal to 4
# If N is not an integer, print N must be a number, followed by a new line,
#   and exit with the status 1
# If N is smaller than 4, print N must be at least 4, followed by a new line,
#   and exit with the status 1
# The program should print every possible solution to the problem
# One solution per line
# Format: see example
# You don't have to print the solutions in a specific order
# You are only allowed to import the sys module

# ===== ARCHITECTURE DESIGN NOTES =====
# === Why the formula for upwards diagonals ===
# occupied_upwards_diagonals = [False] * (2 * N - 1)
# Each diagonal has the same "cell value" (line + number)
# Since we count from 0, last diagonal will be the last cell with value
# (N-1 + N-1). Then we have to account for the "mini-diagonal" (0, 0).
# -> (N-1) + (N-1) + 1 = 2N -2 + 1 = 2N - 1


# ===== BRAINSTORMING =====
# The usual way to resolve this problem is using backtracking process,
#   in which we define as many "branches" as they are potential solutions
#   with as many required subbranches, then start exploring at each step
#   if the current value is breaking the rules (= stopping the "potential")
#   or not.
#   If not then we check if there is yet another element to check behind,
#     if none then we have found a complete solution.
#   If yes then we "lock" this branch as a dead-end, backtrack to the start
#     of the next and restart process.
# In this context the constraints are:
#   1/ Each queen can "reach" ("attack") every position horizontally,
#      vertically and in diagonal.
#      Which implies that...
#      Any row and column is "locked" as soon as one queen is somewhere inside.
#         Consequently each queen has "its own line" & every line must have 1.
#      The cells matching "45° diagonals" crossing every placed queen's cells
#        are also condemned.
#      => Realm of solutions is reduced with each computation step taken.
# Picking an example.
# With a 4 queens on 4-size grid...
# Starting with placing Queen A at 0,0.
# For the remaining queens, forbidden positions are...
# Every cell of line 0
# Every cell of column 0
# Every cell which computation of "line number - column number" is the same
#   as in A's cell (0 - 0 = 0), representing the "descending diagonal"
#   
# Every cell which computation of "line number + column number" is the same
#   as in A's cell (0+0).
# So valid positions for Queen B on line 1 are only cells in columns 2 & 3.
# (1, 0 is "locked column", 1,1 has "descending diagonal" 0 so locked diagonal).
#
