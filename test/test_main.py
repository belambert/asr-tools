import unittest

from asr_tools.kaldi import read_nbest_file
from asr_tools.kaldi import read_transcript_table
from asr_tools.kaldi import read_transcript
from asr_tools.evaluation_util import evaluate

class Testing(unittest.TestCase):
    """Class for testing asr_tools package."""

    nbest_file = "test/data/librispeech1/lat.1.nbest.txt"
    ref_file = "test/data/librispeech1/dev_clean.ref"
    hyp_file = "test/data/librispeech1/dev_clean.14_0.5.tra.txt"

    # Make sure we can read the main (3) types of files.
    def test_read_nbest(self):
        """Can we read n-best list files properly?"""
        with open(self.nbest_file) as f:
            nbests = list(read_nbest_file(f))
            self.assertTrue(len(nbests) == 40)

    def test_read_transcript(self):
        """Can we read transcript files properly?"""
        with open(self.ref_file) as f:
            refs = read_transcript_table(f)
            self.assertTrue(len(refs) == 2703)

    def test_read_hyp(self):
        """Can we read hypothesis files properly?"""
        with open(self.hyp_file) as f:
            refs = read_transcript(f)
            self.assertTrue(len(refs) == 2703)

    def test_evaluation(self):
        """This compares a hyp file to a ref file--this test is probably too slow.
        This may also not be a good package to have this test?"""
        with open(self.hyp_file) as h, open(self.ref_file) as r:
            ref_table = read_transcript_table(r)
            hyps = read_transcript(h)
            evals = []
            for hyp in hyps:
                eval_ = evaluate(ref_table, hyp)
                evals.append(eval_)
            overall_eval = sum(evals[1:], evals[0])
            self.assertTrue(overall_eval.ref_len == 54402)
            self.assertTrue(overall_eval.matches == 51159)
            self.assertTrue(overall_eval.errs == 3815)
