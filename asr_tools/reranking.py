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
Very basic functions for re-ranking n-best lists.

Not used locally in the asr-tools package, but might be used in semlm or other packages.
"""

# TODO: re-ranking doesn't necessarily have to *actually* re-rank.  It could just
# compute statistics

def rerank_nbests(nbests, func):
    """Given a a list of nbests and a function, rerank all the nbests
    with the given function."""
    for nbest in nbests:
        rerank_nbest(nbest, func)

def rerank_nbest(nbest, func):
    """Given an n-best list and a function, rerank the n-best list
    using that function."""
    print("REGULAR")
    nbest.sentences.sort(key=func)

def pseudo_rerank_nbests(nbests, func):
    """Given a a list of nbests and a function, rerank all the nbests
    with the given function."""
    for nbest in nbests:
        pseudo_rerank_nbest(nbest, func)

def pseudo_rerank_nbest(nbest, func):
    """Given an n-best list and a function, rerank the n-best list
    using that function."""
    print("PSEUDO")
    best = nbest.sentences.min(key=func)
    nbest.sentences.remove(best)
    nbest.sentences.insert(0, best)

    
