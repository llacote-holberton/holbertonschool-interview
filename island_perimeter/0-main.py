#!/usr/bin/python3
"""
Main file for testing Island Perimeter algorithm
"""

from functools import wraps
import time
island_perimeter = __import__('0-island_perimeter').island_perimeter

if __name__ == "__main__":
    grid = [
        [0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0]
    ]
    print(island_perimeter(grid))


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
    island_map: list,
    expected_perimeter_length: int
):
    """Checks the algorithm works as intended"""
    print(f"\n=== Asserting behaviour for test case: {case_label} ===")
    print("Test case parameters")
    print(f"Island map:\n-----\n{island_map}\n-----")
    print(f"Expected perimeter length: {expected_perimeter_length}")
    result = island_perimeter(island_map)
    failure_msg = f"""
           For this map expected perimeter was {expected_perimeter_length},
           got {result} instead."""
    assert result == expected_perimeter_length, failure_msg


print("=== STARTING BEHAVIOUR CHECKS ===")
print("Note: Perimeter = island_cells_count * 4) - (shared_borders * 2)")
print("A nice way to double-check manually")

test_case_1 = "1. Official case a: basic 'small L' island (perimeter = 12)"
small_L_island = [
    [0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0],
    [0, 1, 1, 1, 0, 0],
    [0, 0, 0, 0, 0, 0]
]
assert_behaviour(test_case_1, small_L_island, 12)

test_case_2 = "2. Custom case: single cell island (perimeter = 4)"
single_cell_island = [
    [0, 0, 0],
    [0, 1, 0],
    [0, 0, 0]
]
assert_behaviour(test_case_2, single_cell_island, 4)

test_case_3 = "3. Custom case, 2-cell square island (perimeter = 8)"
twocells_squared_island = [
    [0, 0, 0, 0],
    [0, 1, 1, 0],
    [0, 1, 1, 0],
    [0, 0, 0, 0]
]
assert_behaviour(test_case_3, twocells_squared_island, 8)

test_case_4 = "4. No island (water only, perimeter = 0)"
no_island = [
    [0, 0],
    [0, 0]
]
assert_behaviour(test_case_4, no_island, 0)
# Mini-variant
assert_behaviour(test_case_4, [[0], [0], [0]], 0)

test_case_5 = "5. Island touching map's bottom line (perimeter = 12)"
island_touching_bottom = [
    [0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0, 0],
    [0, 1, 1, 1, 0, 0],
    [0, 1, 1, 1, 0, 0]
    # Beware of "off-map" BEING WATER!! So not 9 but 12!
]
assert_behaviour(test_case_5, island_touching_bottom, 12)

test_case_6 = "6. Single 'island cell' map (perimeter = 4!)"
single_point_island = [[1]]
assert_behaviour(test_case_6, single_point_island, 4)

test_case_7 = "7. Full-grid land island (perimeter 2*5 + 2*3 = 16)"
fullgrid_island = [
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1]
]
assert_behaviour(test_case_7, fullgrid_island, 16)

test_case_8 = "8. Complex shape (perimeter = 28, 15 squares and 16 shared)"
complex_shape_island = [
    [0, 1, 0, 0, 0, 1],
    [1, 1, 0, 0, 0, 1],
    [1, 1, 0, 1, 1, 1],
    [0, 1, 1, 1, 0, 0],
    [0, 0, 1, 1, 0, 0]
]
assert_behaviour(test_case_8, complex_shape_island, 28)

print("\n=== ALL ASSERTIONS PASSED ===")
