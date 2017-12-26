# pylint: disable=global-statement

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
Utility functions for keeping track of ASR references and for evaluating
ASR hypotheses.
"""

import copy
from collections import OrderedDict

from edit_distance import SequenceMatcher, edit_distance
from asr_tools.evaluation import Evaluation
from asr_tools.kaldi import read_transcript_table
from asr_evaluation.asr_evaluation import print_diff as eval_print_diff

REFERENCES = OrderedDict()

def evaluate_hyps(hyps, ref_table):
    """Given a list of hypotheses and a reference table, return a list of
    evaluations for the respective hypotheses."""
    evals = []
    for hyp in hyps:
        eval_ = evaluate(ref_table, hyp)
        evals.append(eval_)
    return sum(evals[1:], evals[0])

def sentence_editdistance(s1, s2):
    """Given two 'sentence' objects compute the edit distance and
    return the distance."""
    distance, _ = edit_distance(s1.words, s2.words)
    return distance

def evaluate(ref_table, s):
    """Given a sentence and a reference table, create and return an
    Evaluation object. Save a copy in the sentence."""
    ref = ref_table.get(s.id_)
    if ref is None:
        raise Exception('No reference loaded for ID: {}'.format(s.id_))
    distance, matches = edit_distance(ref.words, s.words)
    eval_ = Evaluation(len(ref.words), matches, distance)
    s.eval_ = eval_
    return eval_

def set_global_references(ref_file):
    """Given a reference file, read it into the global table with the name
    REFERENCES."""
    global REFERENCES
    REFERENCES = read_transcript_table(ref_file)

def get_global_reference(id_):
    """Look-up ASR references by id."""
    return REFERENCES.get(id_)

def print_diff(s1, s2, prefix1='REF:', prefix2='HYP:', suffix1=None, suffix2=None):
    """Print a readable diff between two sentences.

    This is the only place we use anything from asr-evaluation."""
    a = s1.words
    b = s2.words
    sm = SequenceMatcher(a, b)
    eval_print_diff(sm, s1.words, s2.words, prefix1=prefix1, prefix2=prefix2, suffix1=suffix1, suffix2=suffix2)

def sum_evals(evals):
    """Sum a list of evaluations.  Returns the first evaluation if there's
    only one."""
    if len(evals) == 1:
        return copy.copy(evals[0])
    else:
        return sum(evals[1:], evals[0])
