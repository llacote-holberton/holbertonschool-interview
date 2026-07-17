#!/usr/bin/python3

"""
Tests enrichis pour isWinner.

Rappel de la règle : pour un round de plafond n, le nombre de nombres
premiers <= n determine le winner.
  - impair -> Maria gagne (elle joue en 1er et fait le dernier coup)
  - pair   -> Ben gagne

Nombre de nombres premiers <= n (calcules a la main, pour reference) :
  n=2   -> 1 premier  (2)                      -> impair -> Maria
  n=3   -> 2 premiers (2,3)                    -> pair   -> Ben
  n=4   -> 2 premiers (2,3)                    -> pair   -> Ben
  n=5   -> 3 premiers (2,3,5)                  -> impair -> Maria
  n=7   -> 4 premiers (2,3,5,7)                -> pair   -> Ben
  n=11  -> 5 premiers (2,3,5,7,11)             -> impair -> Maria
  n=100  -> 25 premiers                         -> impair -> Maria
  n=1000 -> 168 premiers                        -> pair   -> Ben
  n=10000-> 1229 premiers                       -> impair -> Maria
"""

isWinner = __import__('0-prime_game').isWinner
# total_wins = __import__('0-prime_game').wins


def run_test(description, x, nums,
             expected_ben, expected_maria, expected_winner):
    print("=== {} ===".format(description))
    print("x = {}, nums (extrait) = {}".format(
        x, nums if len(nums) <= 10 else str(nums[:10]) + "..."))
    print("Expected -> Ben: {} win(s), Maria: {} win(s), winner: {}".format(
        expected_ben, expected_maria, expected_winner))
    result = isWinner(x, nums)
    print("Obtenu  -> winner: {}".format(result))
    status = "OK" if result == expected_winner else "ECHEC"
    print("Statut  -> {}".format(status))
    # print("Total wins: ", total_wins)
    print()



# 1) Basic case: Ben wins (all rounds have even "total_moves")
run_test(
    "Ben wins (simple case)",
    x=3,
    nums=[3, 4, 7],
    expected_ben=3,
    expected_maria=0,
    expected_winner="Ben",
)

# 2) Basic case: Maria wins (all rounds have an impair number of primes)
run_test(
    "Maria wins (simple case)",
    x=3,
    nums=[2, 5, 11],
    expected_ben=0,
    expected_maria=3,
    expected_winner="Maria",
)

# 3) Cas simple : egalite -> None
run_test(
    "Equality (simple case)",
    x=4,
    nums=[3, 5, 4, 2],  # Ben, Maria, Ben, Maria -> 2 / 2
    expected_ben=2,
    expected_maria=2,
    expected_winner=None,
)

# 4) Beaucoup de rounds, petits nombres
#    9999 rounds avec n=3 (Ben gagne chaque fois) + 1 round avec n=2 (Maria gagne)
run_test(
    "Many rounds, small/few numbers",
    x=10000,
    nums=[3] * 9999 + [2],
    expected_ben=9999,
    expected_maria=1,
    expected_winner="Ben",
)

# 5) Peu de rounds, grands nombres
run_test(
    "Few rounds, big numbers",
    x=3,
    nums=[1000, 10000, 100],
    expected_ben=1,      # n=1000 -> 168 premiers -> pair -> Ben
    expected_maria=2,     # n=10000 -> 1229 (impair) et n=100 -> 25 (impair) -> Maria
    expected_winner="Maria",
)
