#!/usr/bin/env python3

import argparse
import gzip
import asr_tools.evaluation_util

from asr_tools.io import open_file_stream
from asr_tools.kaldi import read_nbest_file
from asr_tools.kaldi import read_transcript_table
from asr_tools.kaldi import write_nbests
from asr_tools.nbest_util import evaluate_nbests
from asr_tools.nbest_util import evaluate_nbests_oracle
from asr_tools.nbest_util import evals_by_depth

def main():
    """Main method for computing Oracle WER."""
    parser = argparse.ArgumentParser()
    parser.add_argument("nbest_file", type=open_file_stream, help='A file containing n-best lists.  Read as a gzip file if filename ends with .gz')
    parser.add_argument("ref_file", type=argparse.FileType('r'))
    parser.add_argument("output", type=argparse.FileType('w'))
    args = parser.parse_args()

    print('Reading n-best lists...')    
    nbests = list(read_nbest_file(args.nbest_file))
    print('# of nbests: {}'.format(len(nbests)))
    print('Reading transcripts...')
    refs = read_transcript_table(args.ref_file)
    asr_tools.evaluation_util.REFERENCES = refs

    # This is the slow part.
    print('Running evaluation...')
    overall_eval = evaluate_nbests(nbests)

    # Write them back out to a file
    write_nbests(args.output, nbests, save_eval=True)

    args.nbest_file.close()

if __name__ == "__main__":
    main()
