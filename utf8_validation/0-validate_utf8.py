#!/usr/bin/python3
"""Single func module to validate a suite of numbers as valid UTF-8 string """


def validUTF8(data: list) -> bool:
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

# === Logic design ===
# Each integer represents a byte.
# Several bytes can, or not, represent an UTF-8 character (from 1 to 4).
# First byte of a valid character MUST declare how many bytes the character
#   takes to be complete.
# 0b10000000
# if   (byte & 0x80) == 0x00:  n_bytes = 1  # 0xxxxxxx
# elif (byte & 0xE0) == 0xC0:  n_bytes = 2  # 110xxxxx
# elif (byte & 0xF0) == 0xE0:  n_bytes = 3  # 1110xxxx
# elif (byte & 0xF8) == 0xF0:  n_bytes = 4  # 11110xxx
# So process is...
# - Define "data_is_valid_UTF8_sequence" as None
# - Start a loop which will traverse the list of integers
# - Exit conditions are: invalid "sequence" found (False), end reached (True)
# - Define a "multibyte counter" at 0
# - Grab next item, extracts the 8 lesser digits of binary form
# - Compare with UTF-8 format AND "context"
#   * "Multybite == 0" and "format = single-byte char"
#      -> NEXT
#   * "Multibyte == 0" and "format = multibyte head"
#      -> Set multibyte to the expected number of bytes
#         MINUS ONE (obviously should NOT count the header one)
#      -> NEXT
#   * "Multibyte == 0" and "format = continuation char"
#      -> data_is_valid_UT8_sequence = False
#      -> BREAK
#   * "Multibyte  > 0" and "format = continuation char"
#      -> decrement multibyte by 1
#      -> NEXT
#   * "Multibyte  > 0" and "format != continuation char"
#      -> data_is_valid_UT8_sequence = False
#      -> BREAK
#   * Fin de boucle atteinte sans soucis
#     -> ELSE if multibyte == 0 data_is_valid_UTF8_sequence = True
#   Return data_is_valid_UTF8_sequence
# In v2 I could add the fact I store the "reduced byte"
#   to recreate a printable UTF-8 string. :)
