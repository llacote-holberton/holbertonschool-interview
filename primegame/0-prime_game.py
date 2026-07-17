#!/usr/bin/env python3
"""
Prime game resolver for 2 competitors, for n >= 2
Prime game is one where each contestant removes 
  'a prime number and all multiple of it' alternatively.
Goal is to not be the one having to play with no prime number left to pick
  (reminder: 1 is not a prime number because a primer number is a number which
   can only be divided by two different divisors: 1 and itself).
"""





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
