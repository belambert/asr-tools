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


# Should this be in ASR evaluation?

import argparse
from asr_tools.kaldi import read_transcript
from asr_tools.kaldi import read_transcript_table
from asr_tools.evaluation_util import evaluate_hyps


def arg_parser():
    """Return parsed args for this script."""
    desc = """Compute the WER between two 'transcript'-like files.
    The first token of each line should be the ID.  The order of the
    lines doesn't matter."""
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("ref_file", type=argparse.FileType('r'))
    parser.add_argument("hyp_file", type=argparse.FileType('r'))
    args = parser.parse_args()
    return args

def main():
    """Main method for computing WER."""
    args = arg_parser()
    ref_table = read_transcript_table(args.ref_file)
    hyps = read_transcript(args.hyp_file)
    print(evaluate_hyps(hyps, ref_table))

if __name__ == "__main__":
    main()
