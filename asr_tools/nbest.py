from io import StringIO

"""
Representation of n-best lists.
"""

class NBest:
    """Represents an n-best list of ASR hypotheses."""

    sentences = None
    id_ = None

    def __init__(self, sentences, id_=None):
        """Sentences and IDs are required."""
        assert(sentences is not None)
        assert(len(sentences) > 0)
        self.sentences = sentences
        self.id_ = id_

    def __str__(self):
        """Returns a string representation of the object."""
        print_str = StringIO()
        print_str.write('ID: {}\n'.format(self.id_))
        for i, s in enumerate(self.sentences):
            print_str.write('{:3d} {}\n'.format(i + 1, s))
        return print_str.getvalue()
