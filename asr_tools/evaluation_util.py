from collections import OrderedDict

from asr_tools.evaluation import Evaluation
from edit_distance import SequenceMatcher, edit_distance
from asr_evaluation.asr_evaluation import print_diff as eval_print_diff

REFERENCES = OrderedDict()

def evaluate_hyps(hyps, ref_table):
    evals = []
    for hyp in hyps:
        ref = ref_table[hyp.id_]
        eval_ = evaluate(ref_table, hyp)
        evals.append(eval_)
    return sum(evals[1:], evals[0])

def sentence_editdistance(s1, s2):
    """Given two 'sentence' objects compute the edit distance and
    return the distance."""
    distance, matches = edit_distance(s1.words, s2.words)
    return distance

def evaluate(ref_table, s):
    """Given a sentence and a reference table, create and return an
    Evaluation object."""
    ref = ref_table.get(s.id_)
    if ref is None:
        raise Exception('No reference loaded for ID: {}'.format(s.id_))
    distance, matches = edit_distance(ref.words, s.words)
    eval_ = Evaluation(len(ref.words), matches, distance)
    return eval_

def set_global_references(ref_file):
    """Given a reference file, read it into the global table with the name
    REFERENCES."""
    global REFERENCES
    REFERENCES = read_transcript_table(ref_file)

def get_global_reference(id_):
    """Look-up ASR references by id."""
    global REFERENCES
    return REFERENCES.get(id_)

def print_diff(s1, s2, prefix1='REF:', prefix2='HYP:'):
    """Print a readable diff between two sentences."""
    a = s1.words
    b = s2.words
    sm = SequenceMatcher(a, b)
    eval_print_diff(sm, s1.words, s2.words, prefix1=prefix1, prefix2=prefix2)

def sum_evals(evals):
    if len(evals) == 1:
        return evals[0]
    else:
        return sum(evals[1:], evals[0])
