#!/usr/bin/python3
"""Module calculating how many steps required to reach n length string"""


def minOperations(n) -> int:
    """Function finding minimum number of operations to reach length n"""
    if n <= 1:
        # Either 1 so "result already achieved since we always start with 1"
        # Or 0 / negative which is "out of bounds" since substract forbidden.
        return 0

    # Couldn't make the mathematical demonstration and still a bit fuzzy...
    # But we are using two important ideas.
    # Any >1 integer can be decomposed in a multiplication of prime numbers.
    # ab >= a +b by applying Order compatibility with multiplication
    # (for a, b >= 2: (a−1)(b−1) ≥1 --> ab -a -b + 1 >= 1 --> ab >= 1-1 +a +b)
    operations_count = 0
    divisor = 2
    dividend = n
    # print(f"@dev: Starting the progressive reduction of n as {n}")
    while (dividend >= divisor):
        if dividend % divisor == 0:
            # print(f"Current: {dividend} is multiple of {divisor}, dividing")
            dividend //= divisor  # BEWARE! Confer "IMPORTANT" after func.

            operations_count += divisor
            # print(f"Op count = {operations_count}, dividend = {dividend}")
        else:
            divisor += 1
    return operations_count


# IMPORTANT: do not use /= operator which makes a float to keep remainder.
# Because even if technically we know "no remainder" would happen
#   it would still make python convert number as a float...
# Which could lead to bugs for large numbers / many loops.

if __name__ == "__main__":

    print("====== SELF-TESTS ======")
    print(f"Case: n <= 0,  expected min_o = 0; returned? {minOperations(0)}")
    print(f"Case: n == 1,  expected min_o = 0; returned? {minOperations(1)}")
    print(f"Case: n == 2,  expected min_o = 2; returned? {minOperations(2)}")
    print(f"Case: n == 3,  expected min_o = 3; returned? {minOperations(3)}")
    print(f"Case: n == 4,  expected min_o = 4; returned? {minOperations(4)}")
    print(f"Case: n == 5,  expected min_o = 5; returned? {minOperations(5)}")
    print(f"Case: n == 6,  expected min_o = 5; returned? {minOperations(6)}")
    print(f"Case: n == 7,  expected min_o = 7; returned? {minOperations(7)}")
    print(f"Case: n == 8,  expected min_o = 6; returned? {minOperations(8)}")
    print(f"Case: n == 9,  expected min_o = 6; returned? {minOperations(9)}")
    print(f"Case: n == 10, expected min_o = 7; returned? {minOperations(10)}")
    print(f"Case: n == 12, expected min_o = 7; returned? {minOperations(12)}")
    print(f"Case: n == 16, expected min_o = 8; returned? {minOperations(16)}")
    print(f"Case: n == 36, expected min_o = 10; returned? {minOperations(36)}")
    print(f"Case: n == 64, expected min_o = 12; returned? {minOperations(64)}")
    print(f"Case: n == 72, expected min_o = 12; returned? {minOperations(72)}")
    print(f"Case: n == 77, expected min_o = 18; returned? {minOperations(77)}")
    print(f"Devil case 666, expected 45; returned? {minOperations(666)}")
    print(f"Lucky case 777, expected 47; returned? {minOperations(777)}")

    # NOTE: pasting here a skeleton suggested by AI to make test code
    #   more readable / maintenable / extensible...
    tests = {
        1: 0,
        2: 2,
        # Etc...
        72: 12,
        # You got it
        777: 47
    }
    # NOTE: drawback of this in current state is no message on success.
    for n, expected in tests.items():
        assert minOperations(n) == expected, f"Failed for {n}"
