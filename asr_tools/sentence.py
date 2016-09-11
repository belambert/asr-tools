
class Sentence(object):
    """Represents a sentence or utterance."""
    
    def __init__(self, id_, words, acscore=None, lmscore=None):
        """Constructor.  ID and words are required."""
        self.id_ = id_
        self.words = words
        self.acscore = acscore
        self.lmscore = lmscore
        self.eval_ = None
        self.feature_vector = None

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

    def score(self, lmwt=10):
        """Return the overall score as specified by the ASR engine:
        acoustic_score + lm_score * lm_weight."""
        return self.acscore + self.lmscore * lmwt
