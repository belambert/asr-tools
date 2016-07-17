from asr_tools.nbest_util import evaluate_nbests, print_nbest, evaluate_nbests_oracle

"""
Functions to help print evaluations...

Where should this be located?
"""

def print_eval(nbests):
    """Print an evaluation and an oracle evaluation."""
    eval = evaluate_nbests(nbests)
    print('Eval:')
    print(eval)
    print('Oracle eval:')
    print(evaluate_nbests_oracle(nbests))

def print_train_test_eval(train_nbests, test_nbests):
    """Given a train set and a test set of nbest list, print evaluation
     on each of them."""
    print()
    print('Train eval:')
    print_eval(train_nbests)
    print()
    print('Test eval:')
    print_eval(test_nbests)

def print_nbests(nbests):
    """Just print a set of n-bests."""
    for nbest in nbests:
        print('NBEST:')
        print_nbest(nbest, acscore=True, lmscore=True, tscore=True, maxwords=10, print_instances=True)
