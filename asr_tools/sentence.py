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
Just a class to represent a sentence or utterance.
"""

class Sentence(object):
    """Represents a sentence or utterance."""

    def __init__(self, id_, words, acscore=None, lmscore=None, lmscores=None, acscores=None):
        """Constructor.  ID and words are required."""
        self.id_ = id_
        self.words = words
        self.acscore = acscore
        self.lmscore = lmscore
        self.eval_ = None
        self.feature_vector = None
        self.lmscores = lmscores
        self.acscores = acscores

    def __str__(self):
        """Returns a string representation of this object."""
        sentence_str = ' '.join(self.words).lower()
        return sentence_str

    def wer(self):
        """Returns this sentence's WER if the sentence already has been evaluated.
        Otherwise throw an exception."""
        if self.eval_:
            return self.eval_.wer()
        else:
            raise Exception('No cached evaluation for this sentence.')

    def score(self, lmwt=14):
        """Return the overall score as specified by the ASR engine:
        acoustic_score + lm_score * lm_weight."""
        return self.acscore + self.lmscore * lmwt
