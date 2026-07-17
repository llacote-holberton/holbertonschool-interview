#!/usr/bin/python3
"""
Prime game resolver for 2 competitors, for n >= 1
Prime game is one where each contestant removes
  'a prime number and all multiple of it' alternatively.
Goal is to not be the one having to play with no prime number left to pick
  (reminder: 1 is not a prime number because a primer number is a number which
   can only be divided by two different divisors: 1 and itself).
"""

# NOTE: order chosen specifically, and counter-intuitively, because will
#   shorten the piece of code "returning the name of the winner"
P1 = "Maria"
P2 = "Ben"
players = [P2, P1]  # Reminder: Maria always 1st to play
# wins = {P2: 0, P1: 0}


def round_resolver(ceiling: int) -> int:
    """Returns the number of moves required to finish"""
    total_moves = 0
    if ceiling <= 1:
        return total_moves
    if ceiling == 2:  # Not sure if it would work with regular system
        return (1 + total_moves)
    prime_candidates = [True] * (ceiling + 1)
    # By essence 0 and 1 are not prime.
    prime_candidates[0] = False
    prime_candidates[1] = False
    i = 2
    # We simulate "square root check" by upgrading the while condition
    while i * i <= ceiling:
        # If True means must be a prime number
        if prime_candidates[i]:
            # print("Prime number confirmed: ", i)
            # So we can make a valid move let's count it.
            # total_moves += 1
            # Then we must "mark as composed" all its multiple
            j = 2
            while j * i <= ceiling:
                # print("fi as {i} and j as {j} multiply to:", i*j)
                prime_candidates[i*j] = False
                j += 1
        i += 1
    for n in range(0, ceiling+1):
        total_moves += int(prime_candidates[n])
    return total_moves


# Made obsolete by the fact wins counters must be isWinner inner variables.
# def victory_resolver(total_moves: int) -> None:
#     """Determines if first or second player wins and affects victory"""
#     winner = players[total_moves % 2]
#     wins[winner] += 1


def isWinner(x, nums):
    """Simulates the primegame of x rounds each using the next int from nums
        to determine the winner, if any (equality on rounds won = no winner).
    """
    # MUST be LOCAL because otherwise keeps count between isWinner calls.
    wins = {P2: 0, P1: 0}
    # Initializing the loop of rounds
    for r in range(0, x):
        # Responsability: calling the "round resolver" each time.
        total_moves = round_resolver(nums[r])
        # Affecting the winner's count
        winner = players[total_moves % 2]
        wins[winner] += 1
    # Comparing number of wins and returning winner.
    if wins[P2] == wins[P1]:
        return None
    elif wins[P2] < wins[P1]:
        return players[1]
    else:
        return players[0]


if __name__ == "__main__":
    # print("For 2 should be 1 move(s): ", round_resolver(2))
    # print("For 3 should be 2 move(s): ", round_resolver(3))
    # print("For 12 should be (2/4/6/8/10/12) + (3/9) + 5 + 11 so 5: ",
    #       round_resolver(12))
    # print(victory_resolver(0))
    # print(victory_resolver(1))
    # print(victory_resolver(3))
    # print(victory_resolver(5))
    # print("After 4 rounds with 3 Maria victories counts are: ", wins)
    pass

# ========== BRAINSTORM ==========
# The game revolves about a set of numbers, which is the integer sequence
#   from 1 to n.
# Because each time we remove one prime number and all its multiple the number
#   of elements to process reduces gradually
# Except this approach, whether using a List or Set, means having to scan
#  each and every cell of the "updated table"
# => Complexity and time is still big.
# Best way is to view it like this.
# a) Each number, at start, is a candidate to be qualified as "prime number"
# b) So we can set a Truthy value to each to mean "I am still candidate"
#    or "I have yet to be determined as a multiple of anything else"
# c) Because conceptually gamers "remove multiples of prime numbers"
#    we can just make several loops over table with...
#    i. Picking n: if it is still "truthy" it means it hasn't yet been
#       eliminated by previous rounds. So it must be prime
#       (this only works because we loop from the ground up).
#    ii. From that statement "n must be a prime number", we deduce that
#        every multiple of it is not prime so we "jump" from one multiple
#        to the next until we come short of list's end.
# Another point is: we don't need to parse all numbers up to n.
# Because by essence if n was a "non-prime" number then it must have
#   a prime factor which is inferior or equal to its square root.
# => Last point is: we must count all rounds of loops done once limit reached.
# If represents how many plays are done before game stops because "impossible".
# So if it is even, then 1st player loses. If it is odd, 1st player wins.
