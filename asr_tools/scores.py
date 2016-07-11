import operator

"""
File for storing score related functions.  Currently this only has one function, 'monotone',
which I'm using to check if n-bests are correctly sorted.
"""

def monotone(L, comparison=operator.lt, key=lambda x: x):
    return all(comparison(key(x), key(y)) for x, y in zip(L, L[1:]))
