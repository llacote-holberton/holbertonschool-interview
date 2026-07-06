#!/usr/bin/python3
"""Module providing function to compute optimal way to give change"""

import logging

# ===== LOGGER CONFIGURATION =====
# We explicitely define "message level" and "handler"
#   directly at our log's level instead of "global" (root).
log = logging.getLogger('makeChange')

# Using a "global var" to switch level
dev_mode = True
if dev_mode:
    log.setLevel(logging.DEBUG)
else:
    log.setLevel(logging.ERROR)

# Setting up handler
handler = logging.FileHandler("makeChange.log")
handler.setFormatter(logging.Formatter("%(asctime)s %(message)s"))
log.addHandler(handler)
log.propagate = False  # To avoid bubbling up to root and display twice.


# ===== MODULE MAIN FUNCTION =====
def makeChange(coins, total) -> int:
    """
       Given a set of coin, provides optimal way to 'reach' total
       coins: list of integers all strictly superior to 0.
       total: amount to 'reach' with the minimum combination of coins.
       Return: number of coins.
    """

    if len(coins) < 1:
        return -1

    if total <= 0:
        return 0

    if total == 1:
        return 1

    ceiling = total + 1
    # Array storing the "best solutions of coin combination amount"
    #   for all values from 1 to total.
    # To allow our algorithm to work (requires math comparison)
    #   we set the default value to a "ceiling" which must NOT be confused
    #   with an actual computed solution. So to be sure we set it to "total+1"
    # We must use this special writing because we need cell 0 to have 0.
    best_combinations_for_sequences = [0] + [ceiling] * total
    # Because I like to be thorough although not strictly required by exo.
    # Note total + 1 to have the same number of cells as previous array.
    # Not sure it's required but just in case.
    best_coin_for_numbers = [None] * (total + 1)

    log.debug("List of coins before sort: %s", coins)
    # Core logic.
    # We must ensure our list of coins is sorted otherwise logic cannot work.
    coins.sort()  # By design we know all are integers, we can sort in-place.
    log.debug("List of coins after sort: %s", coins)

    def bottom_up_method() -> int:
        # We start an outer loop which will try to find, for a given value,
        #   the minimum absolute number of coins AND the "best starting coin".
        # 0 is useless to assert, because we need 0 coin.
        for i in range(min(coins), ceiling):
            # Starting inner loop to try each coin value and see if it can
            #   allow us to reach a better combination than "i * coins of 1")
            for c in coins:
                if c <= i:
                    # Put "1 coin of c" and "number of coins required
                    #   to shore up the difference"
                    # Will only be strictly inferior if there was an
                    #   existing combination in that "complement cell"
                    combination = 1 + best_combinations_for_sequences[i - c]
                    if combination < best_combinations_for_sequences[i]:
                        # We found a new best combination.
                        best_combinations_for_sequences[i] = combination
                        best_coin_for_numbers[i] = c

    bottom_up_method()
    log.debug("Minimum number of coins for each value in sequence")
    log.debug(best_combinations_for_sequences)
    log.debug("Best 'starting coin' for each value")
    log.debug(best_coin_for_numbers)
    log.debug(f"Best for {total} is {best_combinations_for_sequences[total]}")

    if (best_combinations_for_sequences[total] == ceiling):
        return -1
    else:
        return best_combinations_for_sequences[total]


# ========== INSTRUCTIONS ==========
# Return: fewest number of coins needed to meet total
# * If total is 0 or less, return 0
# * If total cannot be met by any number of coins you have, return -1
# * Coins is a list of the values of the coins in your possession.
#   The value of a coin will always be an integer greater than 0
# * You can assume you have an infinite number of
#      each denomination of coin in the list
# * Your solution's runtime will be evaluated in this task

# ========== BRAINSTORM ==========
# So we need to find how to combine in the minimum of operations
# The Greedy algorithm cannot bear every case especially not
#   the ones where list of coins is not "canonical".
# We either can use Greedy with backtracking and memory
#   Or we can use brute-force.
# Basically to know the minimum number with any set
#   we must work "from the ground up".
# For each increasing "target value" we use each coin piece
#   to try and see if using that coin value would allow us
#   to get the same target value with a lesser multiple than
#   the coin used in a previous attempt.
# Ex: target value 4, coins 1, 2, 4.
# 1: 1 <= 1 so 1 coin of 1 to make 1.
#
# 2: Trying coin 1: we take the number of coins we used
#     to get '1', we add one more coin of same value 1, we check
#     if result is inferior or equal to target. Here, true.
#    So "for target value 2", at this step the minimum combination found is 2.
#    Then we try coin 2: it's <= '2', since it's the first try we just "add 1"
#      is coin '2'* 1 count <= 2 ? YES
#    Is that "coin count" is inferior to the previous combination found (1+1)
#    We must a) affect that "new best minimum" as value
#      for the cell of index "current target value".
#    Coin 4 is > to target value so ignored
#
# 3: Trying coin 1: 1 <= 3 True. If we "put one 1 on table" what's left ? 2
#    Is there a combination allowing is to get "2" ?
#    We check our array at index 2.
#    Because we tried 2 before, and there is a value for it,
#      we read that value: 1 (one coin of value 2).
#    We then check if that "amount of coins" is inferior to
#    what is currently stored as "number of coins" for that target value.
#    => How to get a "default" indicating that we didn't compute anything yet
#    BUT can be checked with a comparison operator? None wouldn't work.
#    => Simplest is to set a clear limit: the "total" amount is probably right.
#       Or maybe total + 1 ? Something to clear once I develop.
#    Back on track: is 1 + 1 inferior to target (4) ? YES.
#    We affect 2 as the value for array[3] -> "best combination found so far"
#
#    Trying coin 2: 2 <= 3 True. If we "put one 2 on table" what's left? 1".
#    Do we have a combination of pieces to get value 1? Check array[1], value 1
#    Is 1+1 strictly < (so better) to "previously best found combination"
#    NO -> We don't do anything.
#
#    Trying coin 3: 3 <=3 True. If we "put one 3 on table" wha's left? 0".
#    We fall on our feet since by design array[0] = 0.
#    Is 0 + 1 < 2 (best solution found until then)? YES.
#    => We affect 1 as the new best solution for array[3].
#    AND if we want, we can also have an array indicating which is the
#      "best starting coin" for reaching that value (so like, choice[3] = 3).
