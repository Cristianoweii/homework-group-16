import math
import random
from sympy import *
from sympy.ntheory import discrete_log

def discreteLogarithm(a, b, m):
    return discrete_log(m, b, a)

def prime_generator(a, b):
    check = true
    while check:
        i = random.randrange(a, b)
        if isprime(i):
            check = false
    return i

def divisor_number(p):
    for q in range(pow(2, 10), (p - 1) // 2):
        if (p - 1) % q == 0 & isprime(q):
            return q

def findPrimefactors(s, n):
    # Print the number of 2s that divide n
    while n % 2 == 0:
        s.add(2)
        n = n // 2
    for i in range(3, int(sqrt(n)), 2):
        while n % i == 0:
            s.add(i)
            n = n // i
    if n > 2:
        s.add(n)

def findPrimitive(n):
    s = set()
    if not isprime(n):
        return -1
    phi = n - 1
    findPrimefactors(s, phi)

    for r in range(2, phi + 1):
        flag = False
        for it in s:
            if pow(r, phi // it, n) == 1:
                flag = True
                break
        if not flag:
            return r
    return -1
