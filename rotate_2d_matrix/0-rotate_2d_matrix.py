#!/usr/bin/python3
"""Script rotating 90° clockwise a 2d matrix"""


def rotate_2d_matrix(matrix):
    """Applies an inplace clock-wise 90° rotation"""
    n = len(matrix)
    if n < 2:
        return matrix
    # Using the "target position formulae" requires to work "like an onion".
    # We must proceed "layer by layer".
    # And because we "swap elements two by two" logically we only need to
    # "work on the first half", using the // to get an integer.
    for layer in range(0, n // 2):
        # ltl = Layer's Top Left. lbr = Layer's Bottom Right
        # We need this because we work in "successive rings of increasingly
        #   smaller radius" so we need to calculate the boundaries.
        top_left = layer
        # Using the computed formula that gives the "swap colummn"
        #   to compute the "diagonal boundary"
        # (N-1 because we start counting from 0, - layer to target
        #  "the current layer's corner")
        bottom_right = n-1 - layer
        # We now have the layer boundaries to work within
        # sq_st = square_start, name chosen to remind that we make affectations
        #   while "jumping" from one corner to the next in a square pattern
        for cell in range(top_left, bottom_right):
            # Required to calculate the other corner's positions
            offset = cell - top_left
            # Defining corners's coordinates, clock-wise
            c_tl = (top_left, cell)  # c_tl = corner__topleft
            # Imagine a circling whirlpool. we progress by "gliding downwards"
            #   the target point on the right side's column
            c_tr = (cell, bottom_right)  # c_tr = corner__topright
            # Here the "fixed portion" is the row as we are
            # "gliding on the bottom side towards the left"
            # c_br = corner__bottomright
            c_br = (bottom_right, bottom_right - offset)
            # And here we "glide upwards" across the left side
            # c_bl = corner__bottomleft
            c_bl = (bottom_right - offset, top_left)

            # Now we just have to make our revolving "square jumps"
            # 0. Store top left value aside for now
            topleft_initial_value = matrix[c_tl[0]][c_tl[1]]
            # 1. Reaffect 1st (top left) with next one's (bottom left).
            matrix[c_tl[0]][c_tl[1]] = matrix[c_bl[0]][c_bl[1]]
            # 2. Same to "translate" bottom_right value to bottom left.
            matrix[c_bl[0]][c_bl[1]] = matrix[c_br[0]][c_br[1]]
            # 3. Same to "translate" top_right value to bottom_right.
            matrix[c_br[0]][c_br[1]] = matrix[c_tr[0]][c_tr[1]]
            # 4. We finish circling by translating top left to top right
            matrix[c_tr[0]][c_tr[1]] = topleft_initial_value


# Embedded self-test
if __name__ == "__main__":
    # 1) Source matrix 15x15, filled up sequentially from 1 to 225
    n = 15
    mtx_source = [[row * n + col + 1 for col in range(n)] for row in range(n)]
    # Importing modules is forbidden so can't use copy.deepcopy(mtx_source)
    mtx_result = [[row * n + col + 1 for col in range(n)] for row in range(n)]

    # 2) Target matrix, also sequential filling but "in a 90° clockwise kind".
    # Calculated independantly with formula derived from (i,j) -> (j, n-1-i)
    # rotated[i][j] = original[n-1-j][i]
    mtx_target = [
        [mtx_source[n - 1 - j][i] for j in range(n)]
        for i in range(n)
    ]

    # 3) Applying function
    rotate_2d_matrix(mtx_result)

    # 4) Check (message displayed if assertion gets False return)
    assert mtx_result == mtx_target, "Function didn't correctly rotate"
    # Only printed if assertion was validated
    print("OK: clock-wise 90° rotation is validated on odd matrix 15x15.")

# ======== INSTRUCTIONS ===========
# Given an n x n 2D matrix, rotate it 90 degrees clockwise.
# Prototype: def rotate_2d_matrix(matrix):
# Do not return anything. The matrix must be edited in-place.
# You can assume the matrix will have 2 dimensions and will not be empty.

# ======== BRAINSTORMING ==========
# Rotating clock-wise means that for an Nth layers we would move indexes.
# But the two-sequence process (mirroring diagonally then horizontally)
#   is apparently more performant at scale so we'll go with it.
# Third way is to find a way to apply the geometrical formula (x,y)→(y,−x)
# Except the indexes in computer arrays do not follow the same logic.
# (in geometry vertical index goes "upwards" and not "downwards" AND
#  it makes the rotation relative to the origin (0,0)).
# x would be the column index so (counter-intuitively) i.
# y would be the row index so (counter-intuitively) j, or rather, -j to
#   take into account index "grows downwards" in computer.
# x, y -> y, -x => i, j => i, -j.
# Now we must take into account that the "rotation origin" must be the center
#   of the matrix and not the origin.
# (Honestly the "reasoning/demonstration" was too hard for me, asked Claude)
#   so the final formula is this: j′=(n−1)−i, i′=j
# Finally we need to take into account the fact that we write as we read.
# Because we work on a square (4 sides), we know that if we "jump" from
#  a starting cell to apply the value from the "next jump point", after N
#  swaps matching "side number N" we'll get back to our starting point.
# AND we must ensure we lose no data as we write.
# This implies three things...
# 1. We must process like this:
#  "value at current pos is now set to value at jump pos"
# 2. We must store the value of the starting point to not lose it immediately.
# 3. We must count how many jumps we make to know when we "finish the round"
#   and affect the "initial value" to "the last jump's cell".

# WRONG ORDER MADE COUNTER-CLOCKWISE HERE.
# Now we just have to make our revolving "square jumps"
# 0. Store top left value aside for now
# topleft_initial_value = matrix[c_tl[0]][c_tl[1]]
# 1. Reaffect first corner (top left) with next one's (top right) value
# matrix[c_tl[0]][c_tl[1]] = matrix[c_tr[0]][c_tr[1]]
# 2. Same to "translate" bottom_right value to top_right.
# matrix[c_tr[0]][c_tr[1]] = matrix[c_br[0]][c_br[1]]
# 3. Same to "translate" bottom_left value to bottom_right.
# matrix[c_br[0]][c_br[1]] = matrix[c_bl[0]][c_bl[1]]
# 4. Finally we finish circling by translating top left to bottom left
# matrix[c_bl[0]][c_bl[1]] = topleft_initial_value
