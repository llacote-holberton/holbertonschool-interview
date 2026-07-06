#!/usr/bin/python3
"""Module providing function to compute perimeter of ASCII island map"""

import logging


# ===== LOGGER CONFIGURATION =====
# We explicitely define "message level" and "handler"
#   directly at our log's level instead of "global" (root).
log = logging.getLogger('islandPerimeter')

# Using a "global var" to switch level
dev_mode = True
if dev_mode:
    log.setLevel(logging.DEBUG)
else:
    log.setLevel(logging.ERROR)

# Setting up handler
handler = logging.FileHandler("islandPerimeter.log")
handler.setFormatter(logging.Formatter("%(asctime)s %(message)s"))
log.addHandler(handler)
log.propagate = False  # To avoid bubbling up to root and display twice.


def island_perimeter(grid) -> int:
    size = len(grid)
    if size < 1:
        return 0

    perimeter_length = 0
    for i in range(0, size):
        for j in range(0, size):
            if grid[i][j] == 1:
                # Calculating "offsets" for top/right/bottom/left neighbours
                # 'nr' = neighbour row, 'nc' = neighbour column
                for nr, nc in [(-1, 0), (0, +1), (+1, 0), (0, -1)]:
                    # Works because dynamic conversion bool -> int
                    perimeter_length += (grid[i + nr][j + nc] == 0)

    return perimeter_length


# ========== INSTRUCTIONS ==========
# Create a function which computes the perimeter of an "island".
# We consider that each 1 represents a square of side length 1.
# Cells are NOT connected diagonally.
# We are "guaranteed" by "client" that there is only always 0 or 1 island.
# We are "guaranteed" by "client" that map cannot exceed  100 in width & height

# ========== BRAINSTORM ==========
# Each cell representing an island has value 1, 0 means water.
# A cell represents a square of side 1.
# So...
# When we find a 1, we must check all four "sides"
#   (cell above, cell right, cell bottom, cell left)
#   if that adjacent cell is 0 then it must count in perimeter.

# ========== DRAFTS ==========
# VERSION 1 writing of the "loop"
# perimeter_length = 0
# for i in range(0, size):
#     for j in range(0, size):
#         if grid[i][j] == 1:
#             # TOP
#             top = grid[i-1][j]
#             right = grid[i][j+1]
#             bottom = grid[i+1][j]
#             left = grid[i][j-1]
#             for neighbour in (top, right, bottom, left):
#                 if neighbour == 0:
#                     perimeter_length += 1
#
# VERSION 2 writing of the loop (current version but with comments)
#     perimeter_length = 0
    # for i in range(0, size):
    #     for j in range(0, size):
    #         if grid[i][j] == 1:
    #             # Calculating "offsets" for top/right/bottom/left neighbours
    #             # 'nr' = neighbour row, 'nc' = neighbour column
    #             for nr, nc in [(-1, 0), (0, +1), (+1, 0), (0, -1)]:
    #                 # Using double boolean conversion
    #                 # perimeter_length += int(not bool(grid[i + nr][j + nc]))
    #                 # Actually useless convert as Py will naturally convert
    #                 # A boolean value as int when part of an affectation (+=)
    #                 # perimeter_length += not grid[i + nr][j + nc]
    #                 # But this is the best, most explicit
    #                 perimeter_length += (grid[i + nr][j + nc] == 0)
