"""
Test module B for gousset testing.
Contains recursive functions and computational tasks.
"""

from typing import List


def fibo(x: List) -> List[int]:
    """
    Returns a list of Fibonacci numbers up to the length of x.
    The values in x are ignored; only the length is used.
    """
    n = len(x)
    if n == 0:
        return []
    elif n == 1:
        return [0]
    fibs = [0, 1]
    for i in range(2, n):
        fibs.append(fibs[-1] + fibs[-2])
    return fibs


def factorial(n: int) -> int:
    """
    Recursive factorial function - will show multiple calls for each invocation
    """
    if n <= 1:
        return 1
    else:
        return factorial(n - 1) * n


def sum_squares(n: int) -> int:
    """Calculate sum of squares from 1 to n"""
    return sum(i * i for i in range(1, n + 1))
