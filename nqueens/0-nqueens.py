#!/usr/bin/python3
"""Script resolving the N queens puzzle"""

import sys  # Required for input grab

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


# Let's first find one solution for N = 4.
N = 4

# From the brainstorming we can infer several variables to hold "state".
occupied_lines = set()  # actually superfluous, kept for now for simplicity.
# At first I thought about using a Set in which columns numbers would be added
#   as we place queens thus locking their respective "columns".
# But in fact using a "truth table" is even quicker.
# Using classic comprehension list syntax
occupied_columns = [False for _ in range(N)]

# Using "list creation by repetition" syntax
occupied_upwards_diagonals = [False] * (2 * N - 1)
# Why?
# Each diagonal has the same "cell value" (line + number)
# Since we count from 0, last diagonal will be the last cell with value
# (N-1 + N-1). Then we have to account for the "mini-diagonal" (0, 0).
# -> (N-1) + (N-1) + 1 = 2N -2 + 1 = 2N - 1

# For those since the value can be negative we'll use a Set for now.
#   Later I'll try to find how to use a truth table like the rest.
occupied_downward_diagonals = set()

# Index will represent line, Value the column for that queen.
# Initializing at -1 because 0 is a "valid key" in that context.
queens_positions = [-1] * N


def find_valid_pos(N):
    pass


def is_safe_position(row_index, col_index):
    # Was the culprit! Because I changed for a while
    #   and in this while when backtracking we need
    #   to temporarily keep the previously stored col index
    #   so I had removed the "reset value to -1"...
    # This check was always returning false.
    # Plus with the new while loop design we are guaranteed
    #   to only have one queen per row anyways. So it is now useless.
    # Check row unused yet
    # if queens_positions[row_index] != -1:
    #     return False
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
    queens_positions[row_index] = col_index
    update_state_registries(row_index, col_index, "lock")


def unlock_queen_position(row_index, col_index):
    queens_positions[row_index] = -1
    update_state_registries(row_index, col_index, "unlock")


solutions = []
# New approach: while lets us manipulate the "loop control" freely.
# Contrarily to for which has its inner counter, untouchable.
current_queen = 0  # Hereafter 'cr'
while current_queen >= 0:  # <= N only gets one valid solution at best
    if current_queen == N:
        # We found a valid solution
        # So we should save the current queens_positions
        #   in a "solutions_list" or something
        solutions.append([[r, c] for r, c in enumerate(queens_positions)])
        # THEN restart exploration with row 0 and col...
        #   "next free col?"
        current_queen -= 1

        # unlock_queen_position(current_queen, queens_positions[current_queen])
        # WRONG: fully unlocking meant resetting the queen's position to -1
        #  thus making the code start always from same position.
        # We just want to backtrack, so just free the state registries
        update_state_registries(
            current_queen,
            queens_positions[current_queen],
            "unlock"
        )
        continue  # Required to immediately "restart cycle" with updated info

    # Computing starting position for search.
    # Row is easy, it's directly the value of current_queen.
    # For Col it's kinda smart but not very intuitive...
    # Because we "initialize" value at -1, if that is the case,
    #   then we didn't explore that row yet. So we can start at col pos 0.
    #   so "stored value + 1" == -1 + 1 == 0 so it works.
    # If it was >=0 it means we have already attempted this row at least once
    #   and stored a col position which seemed fair at the time...
    # But restart because a previous loop cycle for next line was a dead-end
    #   and triggered a backtrack. So we know "memorized position" is bad
    #   so we want to re-start search for next one. So "stored value + 1"
    #   also works.
    cr_row_idx = current_queen
    col_search_start = queens_positions[current_queen] + 1

    # And since now I have functions which always use row and col,
    # I can generate a new "search grid" every loop with updated start
    #   instead on trying to rely on occupied_columns.
    cr_col_idx = next(
        (idx for idx in range(col_search_start, N)
        if is_safe_position(cr_row_idx, idx)),
        None  # Next actually can have a "fallback option"
        # But it means the whole expression before "is the first parameter"
    )
    if cr_col_idx is not None:
        lock_queen_position(cr_row_idx, cr_col_idx)
        current_queen +=1  # Drawback of this approach: manually push counter
    else:
        # prev_queen_row = current_queen -1
        # prev_queen_col = queens_positions[prev_queen_row]
        # if current_queen >= 0:
        # WRONG: because I delete the stored position so it will "derail"
        #     the logic of "I backtracked because dead end so I want to"
        #     "restart from the right of where I was"
        #     unlock_queen_position(prev_queen_row, prev_queen_col)
        # current_queen -= 1
        queens_positions[current_queen] = -1  # Security, should not harm
        current_queen -= 1
        # Unlock the registries ONLY, keep the stored memory,
        #   otherwise will make infinite loop.
        if current_queen >= 0:
            update_state_registries(
                current_queen, 
                queens_positions[current_queen],
                "unlock"
            )

for solution in solutions:
    print(solution)

# We start a loop in which we try to find a valid position
#   for each subsequent queen on her exclusive line.
# for queen_number in range(N):
# 
# 
#     try:
#         free_col_index = next(i for i, occ in enumerate(occupied_columns) 
#             if is_safe_position(queen_number, i))
#         # If exception didn't raise it means we found a safe column pos for
#         #    current row number, so we can place our queen and update "states".
#         lock_queen_position(queen_number, free_col_index)
#     except StopIteration as e:
#         # We didn't find how to pursue in this situation, meaning that we must
#         #   try "moving further" the previous queen to see if that unlocks...
#         print("No solution found, need backtrack!")
#         prev_queen_row = queen_number -1
#         prev_queen_col = queens_positions[prev_queen_row]
#         # Need to reset states which were affected previously
#         # Remove truthness for "state" tables, then reset "main table"
#         unlock_queen_position(prev_queen_row, prev_queen_col)
#         # FINALLY "push back" the main counter to force loop to restart
#         #   "from the previous queen"
#         queen_number -= 1
# 
#     # Problem: how to backtrack if I end up blocked???
# 
# 
# print(queens_positions)

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
