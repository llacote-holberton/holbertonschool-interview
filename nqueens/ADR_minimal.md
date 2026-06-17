# Architecture Decision Records (ADR) - N-Queens Solver

## 1. Data Structures (Chessboard State)

### `occupied_columns` (List)
* **Decision:** Used a list of booleans acting as a truth table, rather than a `Set`.
* **Reason:** Direct index access in a list to check if a column is free (e.g., `occupied_columns[3]`) is the fastest method in Python (constant time complexity, O(1)).

### `occupied_upwards_diagonals` (List)
* **Decision:** Used a list of booleans of size 2N - 1.
* **Reason:** On a grid, the sum of `row + column` always yields a constant and predictable positive integer for each upward diagonal. This mathematical property allows us to use it as a direct index in a pre-allocated list.

### `occupied_downward_diagonals` (Set)
* **Decision:** Used a `Set` (collection of unique elements) instead of a list.
* **Reason:** The `row - column` calculation used to identify downward diagonals can yield negative numbers. Python lists do not handle negative indexes well for direct storage (unless a mathematical offset is applied). A `Set` handles the addition and lookup of these arbitrary values natively with excellent performance.

### `queens_positions` (List)
* **Decision:** Used a 1D array initialized with `-1`, where the index represents the row and the stored value represents the column.
* **Reason:** Avoids the memory overhead and iteration complexity of a full 2D matrix. Initializing with `-1` is crucial because `0` is a valid column index on the chessboard. This instantly distinguishes an unexplored row from an occupied one.

## 2. Resolution Mechanics

### Closure Architecture (Nested Functions)
* **Decision:** Encapsulated all the logic and state variables inside the main `nqueens_solver()` function.
* **Reason:** Provides perfect state isolation. It prevents the use of global variables while removing the need to pass state variables as arguments to every evaluation or modification sub-function.

### Iterative `while` Loop
* **Decision:** Used a `while` loop based on a `current_queen` counter instead of a `for` loop or a strictly recursive function.
* **Reason:** A `for` loop freezes its internal counter, making backtracking overly complex. Classic recursion risks hitting the call stack limit (`RecursionError`) on very large grids. The `while` loop allows free manipulation of the exploration "cursor" both forwards and backwards.

### `backtrack()` Function and `nonlocal` Keyword
* **Decision:** Created a dedicated, argument-free sub-function for backtracking, using `nonlocal current_queen`.
* **Reason:** Strict code factorization (DRY principle). Backtracking is triggered in two distinct scenarios: reaching a dead end and finding a complete solution. The `nonlocal` keyword allows this utility to directly modify the main cursor without polluting the local scope.

### Selective Amnesia During Backtracking
* **Decision:** When returning to a previous row, the receded queen's position is kept in memory (not reset to `-1`). Only the row that led to the complete dead end is reset to `-1`.
* **Reason:** This is the core mechanic of the search tree. Keeping the old position allows the algorithm to compute `old_column + 1` in the next loop iteration to explore new branches, rather than getting stuck in an infinite loop on the first column.

# FRENCH TRANSLATION (thanks to IA ^^)


## 1. Structures de Données (L'état de l'échiquier)

### `occupied_columns` (List)
* **Décision :** Utilisation d'une liste de booléens agissant comme une table de vérité, plutôt qu'un `Set`.
* **Raison :** L'accès direct par index dans une liste pour vérifier si une colonne est libre (ex: `occupied_columns[3]`) est la méthode la plus rapide en Python (complexité temporelle constante).

### `occupied_upwards_diagonals` (List)
* **Décision :** Utilisation d'une liste de booléens de taille `2 * N - 1`.
* **Raison :** Dans une grille, la somme `ligne + colonne` donne toujours un entier positif constant et prévisible pour chaque diagonale montante. On peut donc utiliser ce résultat mathématique comme index direct dans une liste pré-allouée.

### `occupied_downward_diagonals` (Set)
* **Décision :** Utilisation d'un `Set` (ensemble de valeurs uniques) au lieu d'une liste.
* **Raison :** Le calcul `ligne - colonne` pour identifier les diagonales descendantes peut générer des nombres négatifs. Les listes Python supportent mal les index négatifs pour du stockage direct (sans appliquer d'offset mathématique). Le `Set` gère l'ajout et la recherche de ces valeurs arbitraires nativement avec d'excellentes performances.

### `queens_positions` (List)
* **Décision :** Utilisation d'un tableau 1D initialisé avec des `-1`, où l'index représente la ligne et la valeur stockée représente la colonne.
* **Raison :** Évite la lourdeur en mémoire et en itération d'une matrice 2D complète. L'initialisation à `-1` est cruciale car `0` est un index de colonne valide sur l'échiquier. Cela permet de distinguer instantanément une ligne inexplorée d'une ligne occupée.

## 2. Mécanique de Résolution

### Architecture par "Closures" (Fonctions imbriquées)
* **Décision :** Encapsuler toute la logique et les variables d'état à l'intérieur de la fonction principale `nqueens_solver()`.
* **Raison :** Isolation parfaite de l'état. Évite l'utilisation de variables globales tout en supprimant le besoin de faire transiter les variables d'état en arguments ("passe-plat") à chaque appel des sous-fonctions d'évaluation ou de modification.

### Boucle `while` itérative
* **Décision :** Utilisation d'une boucle `while` basée sur un compteur `current_queen` au lieu d'une boucle `for` ou d'une fonction strictement récursive.
* **Raison :** La boucle `for` fige son compteur, rendant le retour en arrière complexe. La récursivité classique expose au risque de dépassement de la limite d'appels (RecursionError) sur de très grandes grilles. Le `while` permet de manipuler librement le "curseur" d'exploration vers l'avant ou l'arrière.

### Fonction `backtrack()` et mot-clé `nonlocal`
* **Décision :** Création d'une sous-fonction sans argument dédiée au retour en arrière, utilisant `nonlocal current_queen`.
* **Raison :** Factorisation stricte (principe DRY). Le backtrack est invoqué dans deux cas distincts : lors d'une impasse et lors de la découverte d'une solution complète. Le mot-clé `nonlocal` permet à cet utilitaire de modifier directement le curseur principal sans polluer la portée locale.

### Amnésie sélective lors du Backtracking
* **Décision :** Lors d'un retour à la ligne précédente, la position de la reine reculée est conservée en mémoire (pas de remise à `-1`). On remet à `-1` uniquement la ligne qui a mené à l'impasse complète.
* **Raison :** Mécanique centrale de l'arbre de recherche. Conserver l'ancienne position permet à l'algorithme de calculer `ancienne_colonne + 1` au tour de boucle suivant pour explorer de nouvelles branches au lieu de tourner en boucle infinie sur la première colonne.
