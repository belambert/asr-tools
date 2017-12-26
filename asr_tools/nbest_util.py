# Copyright 2012-2018 Ben Lambert

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
Utility functions for handling nbest lists.
These functions have dependencies on evaluation_util, not the other way around.
"""

from io import StringIO

import asr_tools.evaluation_util
from asr_tools.evaluation_util import evaluate, sum_evals, get_global_reference, print_diff
from asr_tools.sentence_util import print_sentence

# Oracle related functions
def nbest_oracle_eval(nbest, n=None):
    """Return the evaluation object of the best sentence in the nbest list."""
    return nbest.oracle_hyp(n=n).eval_

def evaluate_nbests_oracle(nbests):
    """Return a single oracle evaluation for a list of n-best lists."""
    evals = list(map(nbest_oracle_eval, nbests))
    return sum_evals(evals)

# Evaluating n-bests
def evaluate_nbest(nbest, force=False):
    """Run our evaluation on each sentence in the nbest list.  Will skip evaluation if one
    is already there, unless forced to.  Saves the evaluation with each sentence."""
    for s in nbest.sentences:
        if force or s.eval_ is None:    # Only compute the evaluation if not already computed.
            evaluate(asr_tools.evaluation_util.REFERENCES, s)
        assert s.eval_  # Make sure we have one
    return nbest.sentences[0].eval_

# This could run mulitple threads, but I've been having trouble getting that working
def evaluate_nbests(nbests):
    """Return a single evaluation of list of n-best lists."""
    evals = list(map(evaluate_nbest, nbests))
    return sum_evals(evals)

def evals_by_depth(nbests, n=100):
    """Return overall oracle evaluations as a function of the depth of the n-best lists."""
    evals_by_depth_ = [None] * n
    for i in range(n):
        evals = []
        for nbest in nbests:
            evals.append(nbest_oracle_eval(nbest, i + 1))
        evals_by_depth_[i] = sum_evals(evals)
    return evals_by_depth_


# Printing n-bests
# TODO: This might be relatively slow because of all the string concatenation
def print_nbest(nbest, acscore=True, lmscore=True, tscore=True, tscore_wip=False,
                wcount=False, lmwt=10.0, maxwords=None, print_instances=False):
    """Returns a string representation of the object.  Doesn't actually *print*."""
    print_str = ''
    hyp = nbest.sentences[0]
    best = nbest.oracle_hyp()
    best_rank = nbest.rank(best)
    print_str += 'ID: {} (#{} is best)\n'.format(nbest.id_, best_rank + 1)

    # Print reference if available
    ref = get_global_reference(nbest.id_)
    if ref:
        print_str += 'REF:  ' + str(ref) + '\n'
    else:
        print_str += '    No reference found.\n'
    print_str += 'HYP:  ' + str(hyp) + '\n'
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

def score_string(s, acscore=True, lmscore=True, tscore=False):
    """Return a string that represents the score.  Which scores are included
    are toggled by the args to this function."""
    output = StringIO()
    number_template = '{:8,.2f}'
    spaces = 2
    if acscore:
        output.write(number_template.format(s.acscore) + ' ' * spaces)
    if lmscore:
        output.write(number_template.format(s.lmscore) + ' ' * spaces)
    if tscore:
        output.write(number_template.format(s.score()) + ' ' * spaces)
    return output.getvalue()

def print_nbest_ref_hyp_best(nbest):
    """Print three sentences: the reference, the top hypothesis, and the lowest WER
    hypothesis on the n-best list."""
    ref = get_global_reference(nbest.id_)
    hyp = nbest.sentences[0]
    best = nbest.oracle_hyp()
    best_rank = nbest.rank(best)
    suffix1 = "{} ({})".format(score_string(best), best_rank + 1)
    suffix2 = "{}".format(score_string(hyp))
    print(nbest.id_)
    print('REF:  {}'.format(ref))
    print_diff(best, hyp, prefix1='BEST:', prefix2='HYP: ', suffix1=suffix1, suffix2=suffix2)
    print('=' * 60)

def print_nbests(nbests):
    """Just print a set of n-bests."""
    for nbest in nbests:
        print('NBEST:')
        print_nbest(nbest, acscore=True, lmscore=True, tscore=True, maxwords=10, print_instances=True)

# Printing evaluations
def print_nbest_eval(nbests):
    """Print an evaluation and an oracle evaluation."""
    eval_ = evaluate_nbests(nbests)
    print('Eval:')
    print(eval_)
    print('Oracle eval:')
    print(evaluate_nbests_oracle(nbests))

def print_train_test_eval(train_nbests, test_nbests):
    """Given a train set and a test set of nbest list, print evaluation
     on each of them."""
    print()
    print('Train eval:')
    print_nbest_eval(train_nbests)
    print()
    print('Test eval:')
    print_nbest_eval(test_nbests)
