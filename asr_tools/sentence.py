
class Sentence:
    """Represents a sentence or utterance."""

    def __init__(self, id_, words, acscore=None, lmscore=None):
        """Constructor.  ID and words are required."""
        self.id_ = id_
        self.words = words
        self.acscore = acscore
        self.lmscore = lmscore
        self.eval_ = None

    def __str__(self):
        """Returns a string representation of this object."""
        sentence_str = ' '.join(self.words).lower()
        return sentence_str

    def wer(self):
        if self.eval_:
            return self.eval_.wer()
        else:
            return 0.0

    def score(self, lmwt=10):
        return self.acscore + self.lmscore * lmwt
