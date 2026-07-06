# Overview

This directory holds exercise on computing how to determine the perimeter of a shape under specific constraints.

# Exercises - Island Perimeter

File 0-island_perimeter.py

## Instructions

Create a function `def island_perimeter(grid):` that returns the perimeter of the island described in `grid`:

- `grid` is a list of list of integers:
  - 0 represents water
  - 1 represents land
  - Each cell is square, with a side length of 1
  - Cells are connected horizontally/vertically (not diagonally). 
  - `grid` is rectangular, with its width and height not exceeding 100
- The grid is completely surrounded by water
- There is only one island (or nothing).
- The island doesn&#39;t have &quot;lakes&quot; (water inside that isn&#39;t connected to the water surrounding the island).

```
guillaume@ubuntu:~/$ cat 0-main.py
#!/usr/bin/python3
&quot;&quot;&quot;
0-main
&quot;&quot;&quot;
island_perimeter = __import__(&#39;0-island_perimeter&#39;).island_perimeter

if __name__ == &quot;__main__&quot;:
    grid = [
        [0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0]
    ]
    print(island_perimeter(grid))

guillaume@ubuntu:~/$ 
guillaume@ubuntu:~/$ ./0-main.py
12
guillaume@ubuntu:~/$ 
```
