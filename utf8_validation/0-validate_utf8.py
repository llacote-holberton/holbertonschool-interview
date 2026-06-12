#!/usr/bin/python3
"""Single func module to validate a suite of numbers as valid UTF-8 string """


def validUTF8(data:list) -> bool:
    pass


# === BUSINESS REQUIREMENTS ===
# Return: True if data is a valid UTF-8 encoding, else return False
# A character in UTF-8 can be 1 to 4 bytes long
# The data set can contain multiple characters
# The data will be represented by a list of integers
# Each integer represents 1 byte of data, therefore you only need to handle
#   the 8 least significant bits of each integer.

# === Resources ===
# https://lokalise.com/blog/
#   what-is-character-encoding-exploring-unicode-utf-8-ascii-and-more/
