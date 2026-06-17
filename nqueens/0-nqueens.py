#!/usr/bin/python3
"""Script resolving the N queens puzzle"""

import sys  # Required for input grab


def nqueens_solver():
    """All-in-one N queens puzzle solver, requires an >=4 int as argument"""

# === Inner functions: Initialization helpers ===
    def init__ensure_valid_argument():
        """Ensures program is called with proper arguments to resolve puzzle"""

        if len(sys.argv) != 2:
            print("Please give a number for chess size / queens number!")
            print(sys.argv)
            exit(1)

        try:
            N = int(sys.argv[1])
        # TypeError cannot happen, sys module guarantees input to be string.
        except ValueError as e:
            print("N must be a number")
            exit(1)

        if N < 4:
            print("N must be at least 4")
            exit(1)

        return N

    def init__setup_state_registries(N: int):
        """Defines and set default values for the 'truth tables' lists & set"""

        occupied_columns = [False for _ in range(N)]
        occupied_upwards_diagonals = [False] * (2 * N - 1)
        occupied_downward_diagonals = set()
        queens_positions = [-1] * N

        return (
            occupied_columns,
            occupied_upwards_diagonals,
            occupied_downward_diagonals,
            queens_positions
        )

# === Inner functions: Search process helpers ===
    def is_safe_position(row_index, col_index):
        """Checks desired grid position is not used/threatened in any way"""

        if occupied_columns[col_index]:
            return False

        downwards_diag_code = row_index - col_index
        if downwards_diag_code in occupied_downward_diagonals:
            return False

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
        """Goes to previous queen and frees up its related positions"""
        nonlocal current_queen
        current_queen -= 1
        if current_queen >= 0:
            update_state_registries(
                current_queen,
                queens_positions[current_queen],
                "unlock"
            )

    def explore():
        """Exploring all paths of the grid saving every solution found"""
        nonlocal current_queen
        while current_queen >= 0:
            if current_queen == N:
                # Means we found a valid solution, so save it and backtrack
                solutions.append(
                    [[r, c] for r, c in enumerate(queens_positions)]
                )
                backtrack()
                continue

            # Computing starting positions for search.
            cr_row_idx = current_queen
            col_search_start = queens_positions[current_queen] + 1

            # Trying to find a valid col pos for current line insertion.
            cr_col_idx = next(
                (idx for idx in range(col_search_start, N)
                    if is_safe_position(cr_row_idx, idx)), None
            )
            # Valid position found, we affect and go to next line.
            if cr_col_idx is not None:
                lock_queen_position(cr_row_idx, cr_col_idx)
                current_queen += 1
            # No valid position found meaning we need to backtrack and try
            #   with previous queen in next free col pos.
            else:
                queens_positions[current_queen] = -1
                backtrack()

    # "Main orchestration"
    #    Initializing everything we need to work
    N = init__ensure_valid_argument()
    (   # Beware that variable names match the ones in function, in same order!
        occupied_columns,
        occupied_upwards_diagonals,
        occupied_downward_diagonals,
        queens_positions
    ) = init__setup_state_registries(N)
    solutions = []

    #    Starting exploration
    current_queen = 0
    explore()

    #    Outputting solutions found
    for solution in solutions:
        print(solution)


if __name__ == "__main__":
    nqueens_solver()
