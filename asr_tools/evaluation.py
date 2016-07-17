
class Evaluation(object):
    """An class the represents an evaluation.  This doesn't have any particular
    requirements on what's being evaluated.  So it could be a single sentence
    evaluation, or an evaluation for an entire corpus."""

    ref_len = None
    matches = None
    errs = None

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
        lines = ["Ref length: {:>10,d}".format(self.ref_len),
                 "Matches:    {:>10,d}".format(self.matches),
                 "Errors:     {:>10,d}".format(self.errs),
                 "WER:        {:>10.2%}".format(self.wer())]
        return '\n'.join(lines)

    def __lt__(self, other):
        """Comparison is done by WER."""
        return (self.wer() - other.wer()) < 0
