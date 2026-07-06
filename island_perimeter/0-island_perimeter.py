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
    pass
