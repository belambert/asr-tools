#!/usr/bin/env python3

import argparse
import operator
import termcolor
import colorama
import asr_tools.evaluation_util

from asr_tools.kaldi import read_nbest_file
from asr_tools.kaldi import read_transcript_table
from asr_tools.nbest_util import evaluate_nbests, print_nbest
from asr_tools.sentence import Sentence
from asr_tools.scores import monotone


def main():
    """Main method to show n-best lists, printing to console."""
    parser = argparse.ArgumentParser()
    parser.add_argument("nbest_file", type=argparse.FileType('r'))
    parser.add_argument("ref_file", nargs='?', type=argparse.FileType('r'))  # optional
    parser.add_argument("--verbose", '-v', default=True)
    args = parser.parse_args()
    colorama.init()
    nbests = list(read_nbest_file(args.nbest_file))
    if args.ref_file:
        refs = read_transcript_table(args.ref_file)
        asr_tools.evaluation_util.REFERENCES = refs
        overall_eval = evaluate_nbests(nbests)
    for nbest in nbests:
        print('NBEST:')
        print_nbest(nbest, acscore=True, lmscore=True, tscore=True, maxwords=10)
        if not monotone(nbest.sentences, comparison=operator.lt, key=Sentence.score):
            print(termcolor.colored('WARNING: Non-montonic scores', 'red', attrs=['bold']))

    if args.ref_file:
        print(overall_eval)


if __name__ == "__main__":
    main()
