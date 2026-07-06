# Overview

This directory holds exercise on computing optimal way to combine different values to reach a specific number.

# Exercises - Making Change - Change comes from within

File 0-making_change.py

## Instructions

Given a pile of coins of different values, determine the fewest number of coins needed to meet a given amount `total`.

* Prototype: `def makeChange(coins, total)`
* Return: fewest number of coins needed to meet `total`
	* If `total` is `0` or less, return `0`
	* If `total` cannot be met by any number of coins you have, return `-1`
* `coins` is a list of the values of the coins in your possession
* The value of a coin will always be an integer greater than `0`
* You can assume you have an infinite number of each denomination of coin in the list
* Your solution&#39;s runtime will be evaluated in this task

```
carrie@ubuntu:~/making_change$ cat 0-main.py
#!/usr/bin/python3
&quot;&quot;&quot;
Main file for testing
&quot;&quot;&quot;

makeChange = __import__(&#39;0-making_change&#39;).makeChange

print(makeChange([1, 2, 25], 37))

print(makeChange([1256, 54, 48, 16, 102], 1453))

carrie@ubuntu:~/making_change$
```
```
carrie@ubuntu:~/making_change$ ./0-main.py
7
-1
carrie@ubuntu:~/making_change$
```
