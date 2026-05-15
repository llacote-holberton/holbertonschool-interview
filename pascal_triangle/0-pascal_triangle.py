#!/usr/bin/python3
"""Module providing a Pascal Triangle's generator"""


def pascal_triangle(n):
    """
    Generates a Pascal's Triangle as a list (pt) which shows
    the number of combinations of K elements in a N set.
    """
    pt = []
    # Adding additional clause guard to cover non int
    if (not isinstance(n, int) or n <= 0):
        return pt
    # So we know we start with 0 for index, and 1 as first and last value.
    # We also know that for a cell of row i and index j, its value is
    # the addition of the cells of index j and j - 1 in row i - 1
    # So we can initialize the first iteration which will take care of columns
    for i in range(0, n):
        # Then we start creating the values in row
        # Since we know the first value is 1, we can use directly the range()
        #   function and use their values.
        # Also means we ust use "n+1" to have it included.
        row = []
        for j in range(0, i+1):
            # print(f"i is {i} and j is {j}")
            if (j == 0 or j == i):
                row.append(1)
            else:
                # Let's try and learn that "unusual" ternary syntax
                # In fact useless since i = 0 or 1 already "excluded"
                #   in the if above with direct assignation of 1.
                # op1 = pt[i-1][j-1] if i > 0 else 0
                # op2 = pt[i-1][j] if i > 0 else 0
                # row.append(op1 + op2)
                # So we can just go straight for a direct assignation.
                row.append(pt[i-1][j-1] + pt[i-1][j])
        # And we affect the resulting list as the "first level value"
        pt.append(row)
        # print(pt)
    # Don't forget to return ;)
    return pt
