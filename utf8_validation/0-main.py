#!/usr/bin/python3
"""
Main file for testing
"""

validUTF8 = __import__('0-validate_utf8').validUTF8

# Represents 'A' valid UTF-8 character
data = [65]
print("Expected: True ('A'). Got?", validUTF8(data))

# All ASCII characters, forming UTF-8 string "Python is cool!"
data = [80, 121, 116, 104, 111, 110, 32, 105, 115, 32, 99, 111, 111, 108, 33]
print("Expected: True ('Python is cool!'). Got?", validUTF8(data))

# False because 65's binary form (01000001) does not match expected format for
# "second byte of a multibyte UTF8 character"
# Which was announced by the first byte: 11100101 = 11 + 10xxx = 3bytes char.
data = [229, 65, 127, 256]
print("Expected: False (second byte not valid UTF-8). Got?", validUTF8(data))

# Complementary tests
# True ('é')
data = [195, 169]
# 195 = 11000011  → 110xxxxx  (début 2 octets)
# 169 = 10101001  → 10xxxxxx  (continuation ✓)
# → 'é' (U+00E9)
print("Expected: True ('é'). Got?", validUTF8(data))


# True (smiley)
data = [240, 159, 152, 128]
# 240 = 11110000  → 11110xxx  (début 4 octets)
# 159 = 10011111  → 10xxxxxx  (continuation ✓)
# 152 = 10011000  → 10xxxxxx  (continuation ✓)
# 128 = 10000000  → 10xxxxxx  (continuation ✓)
# → '😀' (U+1F600)
print("Expected: True ('😀'). Got?", validUTF8(data))


data = [128]
# 128 = 10000000  → 10xxxxxx
# Un octet de continuation sans octet de tête : invalide
explanation = "could be seen as continuation byte 10xxx but no head byte"
print(f"Expected: False ({explanation}). Got?", validUTF8(data))
