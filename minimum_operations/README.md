# Overview

This directory holds exercise on how to design an algorithm which 
  creates a character string made of single character H, of length n,
  in the most efficient way (minimum of operations) while being only allowed two processes.
  1/ Copy all current string
  2/ Paste the copied (bufferized) onto the existing.
  (Of course you do not have to re-paste-all between each paste ;)).

# Exercise

## Minimum operations 

File 0-minoperations.py

## Instructions

In a text file, there is a single character H. Your text editor can execute only two operations in this file: Copy All and Paste. Given a number n, write a method that calculates the fewest number of operations needed to result in exactly n H characters in the file. Be smart about how you utilize the memory!
```
    Prototype: def minOperations(n)
    Returns an integer
    If n is impossible to achieve, return 0
```

## Example of detailed steps to achieve result
n = 9

H => Copy All => Paste => HH => Paste =>HHH => Copy All => Paste => HHHHHH => Paste => HHHHHHHHH
