#!/usr/bin/python3

canUnlockAll = __import__('0-lockboxes').canUnlockAll

# IMPORTANT REMINDERS:
# Function expects a list of lists which only hold positive integers
#    or None. Values do not have to match primary level's range.
# "Boxes values" are "keys to other first-level boxes"
# The "cell of index 0" is ALWAYS UNLOCKED.

print("-------- DEV MODE ---------")
devboxes = [[4], {99}, [3], [2], [2]]
canUnlockAll(devboxes)
print("----- END DEV MODE --------")

# === Official tests ===

# Simple chain
boxes = [[1], [2], [3], [4], []]
expected = True
result = canUnlockAll(boxes)
print(f"@test: Basic chain. Expected: {expected}. Returned? {result}")
# print(canUnlockAll(boxes))
# Expected print: True
# Explanation: we can read cell 0 which allows us to read 1,
# which allows us to read 2 etc... Up to "cell of index 4"
# which is empty but that is ok since it was the last yet to open.

boxes = [[1, 4, 6], [2], [0, 4, 1], [5, 6, 2], [3], [4, 1], [6]]
expected = True
result = canUnlockAll(boxes)
print(f"@test: Basic chain. Expected: {expected}. Returned? {result}")
# print(canUnlockAll(boxes))
# Expected print: True


boxes = [[1, 4], [2], [0, 4, 1], [3], [], [4, 1], [5, 6]]
expected = False
result = canUnlockAll(boxes)
print(f"@test: Basic chain. Expected: {expected}. Returned? {result}")
# Expected print: False


# === Additional tests suggested by IA ;) ===
# Empty box list
boxes = [[]]
expected = True
result = canUnlockAll(boxes)
print(f"@test: Empty list. Expected: {expected}. Returned? {result}")
# True (empty list nothing to open so technically "all can be opened")

# No "starting jump point"
boxes = [[], [1], [2]]
expected = False
result = canUnlockAll(boxes)
print(f"@test: No starting point. Expected: {expected}. Returned? {result}")
# False (the "starting unlocked" has no value to "jump to the next")

# Mutual referencement
boxes = [[1], [0]]
expected = True
result = canUnlockAll(boxes)
print(f"@test:Infinite cross-ref. Expected: {expected}. Returned? {result}")
# True (must avoid infinite loop)

# Variant of "avoid infinite loop" handling with self-referencing cell.
boxes = [[0]]
expected = True
result = canUnlockAll(boxes)
print(f"@test:Infinite self-ref. Expected: {expected}. Returned? {result}")
# True

# Extension of previous case: the two last cells are never referenced
boxes = [[1], [0], [3], []]
expected = False
result = canUnlockAll(boxes)
print(f"@test: Unreachable cells. Expected: {expected}. Returned? {result}")
# False (because single cross-reference leaving out the others)

# List which technically has all numbers matching list index and range
#   BUT using a "chaining approach" cannot work
# Technically the same as previous just with added "nesting level"
boxes = [[1], [0], [3], [2]]
expected = False
result = canUnlockAll(boxes)
print(f"@test: Unreachable + nested. Expected: {expected}. Returned? {result}")
# False

# List with keys for non-existent indexes (boxes)
boxes = [[1, 99], [2], []]
expected = True
result = canUnlockAll(boxes)
print(f"@test: Keys for oob boxes. Expected: {expected}. Returned? {result}")
# True (All existing boxes are openable even if some keys target out of bounds)

# List with duplicate keys
boxes = [[1, 1, 1], [2], []]
expected = True
result = canUnlockAll(boxes)
print(f"@test: Duplicate keys. Expected: {expected}. Returned? {result}")
# True (must handle duplicates properly to not break "chain logic")

# Variant case of "duplicate keys" handling test
boxes = [[1, 2, 3], [4], [4], [4], []]
expected = True
result = canUnlockAll(boxes)
print(f"@test: Duplicates variant. Expected: {expected}. Returned? {result}")
# True

# Unaccessible box although having exploitable value
boxes = [[1], [2], [3], [], [0]]
expected = False
result = canUnlockAll(boxes)
print(f"@test: One unreachable box. Expected: {expected}. Returned? {result}")
# False
"""
"""
