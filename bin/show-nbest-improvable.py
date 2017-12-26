#!/usr/bin/env python3

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


import argparse
import asr_tools.evaluation_util

from asr_tools.io import open_file_stream
from asr_tools.kaldi import read_nbest_file
from asr_tools.kaldi import read_transcript_table
from asr_tools.nbest_util import evaluate_nbests, print_nbest_ref_hyp_best, print_nbest


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
        if nbest.is_improveable():
            print_nbest_ref_hyp_best(nbest)
            # print_nbest(nbest)
    print(overall_eval)

if __name__ == "__main__":
    main()
