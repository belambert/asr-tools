import operator

def monotone(L, comparison=operator.lt, key=lambda x: x):
    return all(comparison(key(x), key(y)) for x, y in zip(L, L[1:]))
