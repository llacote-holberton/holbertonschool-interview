#!/usr/bin/python3
"""Single func module to validate a suite of numbers as valid UTF-8 string """


def check_multibyte_header(byte) -> int:
    """
        Uses binary & comparison to check pattern matches header byte
        by applying a "mask" which only keeps the relevant '1'.
        Directly returns the number of "continuation bytes" expected.
    """
    if (byte & 0b10000000) == 0b00000000:  # 0xxxxxxx  → 1 byte char
        return 0  # Will be understood as False by caller
    elif (byte & 0b11100000) == 0b11000000:  # 110xxxxx  → 2 bytes char
        return 1
    elif (byte & 0b11110000) == 0b11100000:  # 1110xxxx  → 3 bytes char
        return 2
    elif (byte & 0b11111000) == 0b11110000:  # 11110xxx  → 4 bytes char
        return 3
    else:
        return 0


def is_continuation_byte(byte) -> bool:
    """Check if byte matches the 10xxxxxx mask which marks 'continuation'"""
    return (byte & 0b11000000) == 0b10000000        # 10xxxxxx


def validUTF8(data: list) -> bool:
    """Validates that list of int can be interpreted as valid UTF8 string"""
    if len(data) == 0:
        return False

    data_is_valid_UTF8_sequence = None
    # Renamed from multibyte_counter which was less explicit
    expected_continuation_bytes = 0
    # Loop parsing potential UTF-8 sequence
    for n in data:
        # Reduce the int to its 8 lesser binary digits
        # Using 255 in binary and the & binary operator
        #   which only keeps the 1 present "both sides"
        current_byte = n & 0b11111111  # Hexa would be 0xFF

        # Determine the "nature" of current int
        # If multibyte > 0 this MUST be a continuation byte
        if expected_continuation_bytes > 0:
            if is_continuation_byte(current_byte):
                expected_continuation_bytes -= 1
                continue
            else:
                data_is_valid_UTF8_sequence = False
                break
        # Multibyte counter is currently 0 so we can
        #   directly affect it.
        else:
            expected_continuation_bytes = check_multibyte_header(current_byte)
            if expected_continuation_bytes == 0:
                if is_continuation_byte(current_byte):
                    data_is_valid_UTF8_sequence = False
                    break
            else:
                continue
    else:
        data_is_valid_UTF8_sequence = (expected_continuation_bytes == 0)
    return data_is_valid_UTF8_sequence

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
# NOTE: comparing "as string" would be possible but far less performant
#   because of conversion cost
# bits = format(byte, '08b')  # ex: 195 → "11000011"
#
# if bits[0] == '0':           # 0xxxxxxx
#     n_bytes = 1
# elif bits[:3] == '110':      # 110xxxxx
#     n_bytes = 2
# elif bits[:4] == '1110':     # 1110xxxx
#     n_bytes = 3
# elif bits[:5] == '11110':    # 11110xxx
#     n_bytes = 4
