#!/usr/bin/env python3

import argparse
import asr_tools.evaluation_util

from asr_tools.kaldi import read_nbest_file
from asr_tools.kaldi import read_transcript_table
from asr_tools.nbest_util import evaluate_nbests


def main():
    """Main method for figuring out which examples from n-best lists
    are potentially improvable."""
    parser = argparse.ArgumentParser()
    parser.add_argument("nbest_file", type=argparse.FileType('r'))
    parser.add_argument("ref_file", type=argparse.FileType('r'))
    args = parser.parse_args()

    nbests = list(read_nbest_file(args.nbest_file))
    refs = read_transcript_table(args.ref_file)
    asr_tools.evaluation_util.REFERENCES = refs

    overall_eval = evaluate_nbests(nbests)
    for nbest in nbests:
        # print(nbest)
        nbest.print_ref_hyp_best()
        # pass
    print(overall_eval)

if __name__ == "__main__":
    main()
