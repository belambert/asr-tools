import unittest

from asr_tools.kaldi import read_nbest_file
from asr_tools.kaldi import read_transcript_table
from asr_tools.kaldi import read_transcript
from asr_tools.evaluation_util import evaluate

class Testing(unittest.TestCase):

    nbest_file = "test/data/librispeech1/lat.1.nbest.txt"
    ref_file = "test/data/librispeech1/dev_clean.ref"
    hyp_file = "test/data/librispeech1/dev_clean.14_0.5.tra.txt"

    # Make sure we can read the main (3) types of files.
    def test_read_nbest(self):
        with open(self.nbest_file) as f:
            nbests = list(read_nbest_file(f))
            self.assertTrue(len(nbests) == 40)

    def test_read_transcript(self):
        with open(self.ref_file) as f:
            refs = read_transcript_table(f)
            self.assertTrue(len(refs) == 2703)

    def test_read_hyp(self):
        with open(self.hyp_file) as f:
            refs = read_transcript(f)
            self.assertTrue(len(refs) == 2703)

    # This compares a hyp file to a ref file--this test is probably too slow
    def test_evaluation(self):
        with open(self.hyp_file) as h, open(self.ref_file) as r:
            ref_table = read_transcript_table(r)
            hyps = read_transcript(h)
            evals = []
            for hyp in hyps:
                ref = ref_table[hyp.id_]
                eval_ = evaluate(ref_table, hyp)
                evals.append(eval_)
            overall_eval = sum(evals[1:], evals[0])
            self.assertTrue(overall_eval.ref_len == 54402)
            self.assertTrue(overall_eval.matches == 51159)
            self.assertTrue(overall_eval.errs == 3815)

    # python ./bin/sklearn-test.py  ~/data/librispeech1/nbests/lat.1.nbest.txt ~/data/librispeech1/dev_clean.ref
    # python ./bin/test-fe.py  ~/data/librispeech1/nbests/lat.1.nbest.txt
    # Other things to test:
    # Computing Oracle WER?
    # python ./bin/perceptron-training.py  ~/data/librispeech1/nbests/lat.1.nbest.txt.testing.2x \
    #    ~/data/librispeech1/dev_clean.ref
