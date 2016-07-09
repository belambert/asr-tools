

def rerank_nbests(nbests, func):
    """Given a a list of nbests and a function, rerank all the nbests
    with the given function."""
    for nbest in nbests:
        rerank_nbest(nbest, func)

def rerank_nbest(nbest, func):
    """Given an n-best list and a function, rerank the n-best list
    using that function."""
    nbest.sentences = sorted(nbest.sentences, key=func)
