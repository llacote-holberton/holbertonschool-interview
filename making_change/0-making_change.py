#!/usr/bin/python3
"""Module providing function to compute optimal way to give change"""


def makeChange(coins, total) -> int:
    """
       Given a set of coin, provides optimal way to 'reach' total
       coins: list of integers all strictly superior to 0.
       total: amount to 'reach' with the minimum combination of coins.
       Return: number of coins.
    """

    if len(coins) < 1 or total <= 0:
        return 0

    




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
#    Is 1+1 strictly inferior (so better) to "previously best found combination"
#    NO -> We don't do anything.
#
#    Trying coin 3: 3 <=3 True. If we "put one 3 on table" wha's left? 0".
#    We fall on our feet since by design array[0] = 0.
#    Is 0 + 1 < 2 (best solution found until then)? YES.
#    => We affect 1 as the new best solution for array[3].
#    AND if we want, we can also have an array indicating which is the 
#      "best starting coin" for reaching that value (so like, choice[3] = 3).


