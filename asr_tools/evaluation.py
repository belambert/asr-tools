# In my previous version, I had a couple versions of evaluation object.
# Some contained the words, etc. that caused errors.
# We can use this same object for sentence error rate.

class Evaluation():
    ref_len = None
    matches = None
    errs = None

    def __init__(self, ref_len, matches, errs):
        self.ref_len = ref_len
        self.matches = matches
        self.errs = errs

    def wer(self):
        """Calculate word error rate (WER)"""
        return self.errs / self.ref_len

    def wrr(self):
        """Calculate word recognition rate (WRR)"""
        return self.matches / self.ref_len

    def is_correct():
        return errs == 0

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

    def __cmp__(self, other):
        self.wer() - other.wer()
