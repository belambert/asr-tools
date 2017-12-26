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
A class that represents an evaluation.  This doesn't have any particular
requirements on what's being evaluated.  So it could be a single sentence
evaluation, or an evaluation for an entire corpus.
"""

class Evaluation(object):
    """A class that represents an evaluation.  This doesn't have any particular
    requirements on what's being evaluated.  So it could be a single sentence
    evaluation, or an evaluation for an entire corpus."""

    def __init__(self, ref_len, matches, errs):
        """Constructor requires ref_len, # of matches, and # of errors."""
        self.ref_len = ref_len
        self.matches = matches
        self.errs = errs

    def wer(self):
        """Calculate word error rate (WER)"""
        return self.errs / self.ref_len

    def wrr(self):
        """Calculate word recognition rate (WRR)"""
        return self.matches / self.ref_len

    def is_correct(self):
        """The thing being evaluated is correct if there are zero errors."""
        return self.errs == 0

    def __add__(self, other):
        """Add each field, creating a new object."""
        return Evaluation(self.ref_len + other.ref_len,
                          self.matches + other.matches,
                          self.errs + other.errs)

    def __str__(self):
        """Print the primary evaluation metrics."""
        lines = ["WER:        {:>10.2%}".format(self.wer())]
        return '\n'.join(lines)

    def __lt__(self, other):
        """Comparison is done by WER."""
        return (self.wer() - other.wer()) < 0
