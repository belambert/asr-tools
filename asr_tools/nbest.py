"""
Representation of n-best lists.
"""

from io import StringIO


class NBest(object):
    """Represents an n-best list of ASR hypotheses."""

    def __init__(self, sentences, id_=None):
        """Sentences and IDs are required."""
        assert sentences is not None
        assert len(sentences) > 0
        self.sentences = sentences
        self.id_ = id_

    def __str__(self):
        """Returns a string representation of the object."""
        print_str = StringIO()
        print_str.write('ID: {}\n'.format(self.id_))
        for i, s in enumerate(self.sentences):
            print_str.write('{:3d} {}\n'.format(i + 1, s))
        return print_str.getvalue()

    def crop(self, m):
        """Throw out all but the first m of the n-best list."""
        self.sentences = self.sentences[:m]

    def hyp(self):
        """Get the n-best's hypotheis (i.e. what's on top of the list)."""
        return self.sentences[0]

    def oracle_hyp(self, n=None):
        """Find and return the sentence with the lowest WER in the n-best list."""
        sentences = self.sentences
        if n: sentences = sentences[:n]
        return min(sentences, key=lambda x: x.wer())

    def is_improveable(self):
        """Is there a hypothesis in the n-best list that's better than the
        top one?  If yes, then this n-best list is improvable."""
        return self.oracle_hyp().eval_.wer() < self.hyp().eval_.wer()

    def rank(self, sentence):
        """Return the rank of the given sentence."""
        return self.sentences.index(sentence)
