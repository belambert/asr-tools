#!/usr/bin/env python3

import argparse
import asr_tools.evaluation_util

from asr_tools.io import open_file_stream
from asr_tools.kaldi import read_nbest_file
from asr_tools.kaldi import read_transcript_table
from asr_tools.nbest_util import evaluate_nbests, print_nbest_ref_hyp_best


def main():
    """Main method for figuring out which examples from n-best lists
    are potentially improvable."""
    parser = argparse.ArgumentParser()
    parser.add_argument("nbest_file", type=open_file_stream, help='A file containing n-best lists.  Read as a gzip file if filename ends with .gz')    
    parser.add_argument("ref_file", type=argparse.FileType('r'))
    args = parser.parse_args()

    nbests = list(read_nbest_file(args.nbest_file))
    refs = read_transcript_table(args.ref_file)
    asr_tools.evaluation_util.REFERENCES = refs

    overall_eval = evaluate_nbests(nbests)
    for nbest in nbests:
        print_nbest_ref_hyp_best(nbest)
    print(overall_eval)

if __name__ == "__main__":
    main()
