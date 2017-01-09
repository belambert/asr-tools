"""
File for storing score related functions.  Currently this only has one function, 'monotone',
which I'm using to check if n-bests are correctly sorted.
"""

import operator

def monotone(L, comparison=operator.lt, key=lambda x: x):
    """Check if all the numbers are monotonically increasing."""
    return all(comparison(key(x), key(y)) for x, y in zip(L, L[1:]))
