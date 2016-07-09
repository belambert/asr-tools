import asr_tools.evaluation_util

from asr_tools.evaluation_util import evaluate
from asr_tools.evaluation_util import sum_evals
from asr_tools.evaluation_util import get_global_reference
from asr_tools.sentence_util import print_sentence


def nbest_oracle_sort(nbest, n=None):
    """Sort an n-best list by it's WER."""
    nbest = nbest.copy()
    if n: nbest.sentences = nbest.sentences[:n]
    nbest.sentences = sorted(nbest.sentences, key=lambda x: x.eval_.wer())
    return nbest

def nbest_best_sentence(nbest, n=None):
    """Find and return the sentence with the lowest WER in the n-best list."""
    sentences = nbest.sentences
    if n: sentences = sentences[:n]
    return min(sentences, key=lambda x: x.wer())

def nbest_oracle_eval(nbest, n=None):
    """Return the evaluation object of the best sentence in the nbest list."""
    return nbest_best_sentence(nbest, n=n).eval_

def evaluate_nbest(nbest, force=False):
    """Run our evaluation on each sentence in the nbest list.  Will skip evaluation if one
    is already there, unless forced to.  Saves the evaluation with each sentence."""
    id_ = nbest.id_
    for s in nbest.sentences:
        if force or s.eval_ is None:    # Only compute the evaluation if not already computed.
            e = evaluate(asr_tools.evaluation_util.REFERENCES, s)
            s.eval_ = e
    return nbest.sentences[0].eval_

def evaluate_nbests(nbests):
    """Return a single evaluation of list of n-best lists."""
    evals = list(map(evaluate_nbest, nbests))
    return sum_evals(evals)

def evaluate_nbests_oracle(nbests):
    """Return a single oracle evaluation for a list of n-best lists."""
    evals = list(map(nbest_oracle_eval, nbests))
    return sum_evals(evals)

def evals_by_depth(nbests, n=100):
    """Return overall oracle evaluations as a function of the depth of the n-best lists."""
    evals_by_depth = [None] * n
    for i in range(n):
        evals = []
        for nbest in nbests:
            evals.append(nbest_oracle_eval(nbest, i + 1))
        evals_by_depth[i] = sum_evals(evals)
    return evals_by_depth

def print_nbest(nbest, acscore=True, lmscore=True, tscore=True, tscore_wip=False,
                wcount=False, lmwt=10.0, maxwords=None, print_instances=False):
    """Returns a string representation of the object."""
    # This might be relatively slow because of all the string concatenation
    print_str = ''
    hyp = nbest.sentences[0]
    best = nbest_best_sentence(nbest)
    best_rank = nbest.sentences.index(best)
    print_str += 'ID: {} (#{} is best)\n'.format(nbest.id_, best_rank + 1)

    # Print reference if available
    ref = get_global_reference(nbest.id_)
    if ref:
        print_str += 'REF:  ' + str(ref) + '\n'
    else:
        print_str += '    No reference found.\n'
    print_str += 'HYP:  ' + str(hyp) + '\n'
    # print_str += 'BEST: '.format(best_rank + 1) + str(best) + '\n'
    print_str += 'BEST: ' + str(best) + '({})\n'.format(best_rank + 1)

    if print_instances:
        for i, s in enumerate(nbest.sentences):
            sentence_str = print_sentence(s, acscore=acscore, lmscore=lmscore, tscore=tscore,
                                          tscore_wip=tscore_wip, wcount=wcount, lmwt=lmwt, maxwords=maxwords)
            print_str += '{:3d} '.format(i + 1) + sentence_str
            if best_rank == i:
                print_str += ' **'
            print_str += '\n'
    print(print_str)

def print_nbest_ref_hyp_best(nbest):
    """Print three sentences: the reference, the top hypothesis, and the lowest WER
    hypothesis on the n-best list."""
    ref = get_global_reference(nbest.id_)
    hyp = nbest.sentences[0]
    best = nbest_best_sentence(nbest)
    best_rank = nbest.sentences.index(best)
    print_diff(ref, best, prefix1='REF: ', prefix2='BEST:')
    print_diff(best, hyp, prefix1='BEST:', prefix2='HYP: ')
    print('=' * 60)
