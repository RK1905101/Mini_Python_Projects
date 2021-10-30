# Header files
from sys import stdin, stdout
from math import ceil, gcd

# Input data
stdin = open("input", "r")

# Pre-defined values
mod = 10**9 + 7
MAX = float('inf')
MIN = -float('inf')

# Pre-defined functions

# LCM of two numbers -> int
def lcm(a, b):
    return (a * b) // gcd(a, b)

# Sum of all the digits of a number -> int
def sumdigit(n):
    s = 0
    while(n):
        s += n % 10
        n //= 10
    return s

# Check if char is vowel or not -> bool
def isvowel(s):
    if s in ['a', 'e', 'i', 'o', 'u']:
        return True
    return False

# sum of all the numbers from 1 upto n -> int
def linearsum(n):
    if n <= 0:
        return 0
    return (n * (n + 1)) // 2

# all Factors of a given number -> list
from functools import reduce
def factors(n):
    return list(set(reduce(list.__add__, ([i, n // i] for i in range(1, int(n**0.5) + 1) if n % i == 0))))

# No. of combinations (nCr) -> int
import functools
def ncr(n, r):
    r = min(r, n - r)
    a = functools.reduce(lambda x, y: x * y, range(n, n - r, -1), 1)
    b = functools.reduce(lambda x, y: x * y, range(1, r + 1), 1)
    return a // b

# returns base raised to power modulo mod -> int
def fast_power(base, power):
    result = 1
    while power > 0:
        if power % 2 == 1:
            result = (result * base) % mod
        power = power // 2
        base = (base * base) % mod
    return result

# return inverse modulo of a number -> int
def inverse_mod(q, mod):
    return fast_power(q, mod - 2) % mod

# New function
def func():
    # function body
    
    return

# Actual Code begins here
for _ in range(int(stdin.readline())):
    n = int(stdin.readline())
    n, m = map(int, stdin.readline().split())
    s = stdin.readline().strip()
    arr = list(map(int, stdin.readline().split()))
