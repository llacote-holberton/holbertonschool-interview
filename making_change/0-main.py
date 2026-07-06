#!/usr/bin/python3
"""
Main file for testing
"""

from functools import wraps
import time
makeChange = __import__('0-making_change').makeChange


# Shamelessly copy/pasting from
#   https://dev.to/kcdchennai/python-decorator-to-measure-execution-time-54hk
# Also confer*
#   https://medium.com/@blueberry92450/
#          using-functools-wraps-in-python-decorator-952030a70615
# On the benefits of using the dedicated decorator @wraps
def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f'Func {func.__name__}{args} {kwargs} took {total_time:.4f} sec')
        return result
    return timeit_wrapper


@timeit
def assert_behaviour(
    case_label: str,
    coins: list,
    total: int,
    expected_optimal_number: int
):
    """Checks the algorithm works as intended"""
    print(f"\n=== Asserting behaviour for test case: {case_label} ===")
    print("Test case parameters")
    print(f"Total to reach: {total}\nAvailable coins: {coins}")
    print(f"Expected num for optimal combination: {expected_optimal_number}")
    result = (makeChange(coins, total))
    if expected_optimal_number is None:
        failure_msg = f"For {total} and f{coins},normally NO SOLUTION."
        # @warning: MUST USE THIS SYNTAX EXACTLY: assert condition, message
        #   WITHOUT PARENTHESES!!
        assert result == -1, failure_msg
    else:
        failure_msg = f"""
           For {total} and f{coins},
           expected {expected_optimal_number}, got {result}."""


print("=== STARTING BEHAVIOUR CHECKS ===")
test_case_1 = "1. Official case a: basic small example"
assert_behaviour(test_case_1, [1, 2, 25], 37, 7)

test_case_2 = "2. Official case b: more complex example"
assert_behaviour(test_case_2, [1256, 54, 48, 16, 102], 1453, None)

test_case_3 = "3. Custom case, canonical system (euros)"
euros = [1, 2, 5, 10, 20, 50, 100, 200]
assert_behaviour(test_case_3, euros, 263, 5)

test_case_4 = "4. Non-trivial set of 10 coins from 1 to 157"
complex_set = [1, 3, 7, 12, 19, 31, 53, 79, 101, 157]
assert_behaviour(test_case_4, complex_set, 431, 5)

test_case_5 = "5. BIG number"
big_coins = [1, 20000, 50000]
assert_behaviour(test_case_5, big_coins, 80004, 8)

print("\n=== ALL ASSERTIONS PASSED ===")
