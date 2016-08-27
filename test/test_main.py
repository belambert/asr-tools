import os
import sys
import copy
import unittest
import operator

from asr_tools.kaldi import read_nbest_file
from asr_tools.kaldi import read_transcript_table
from asr_tools.kaldi import read_transcript
from asr_tools.sentence import Sentence
from asr_tools.evaluation_util import evaluate, evaluate_hyps, get_global_reference
from asr_tools.evaluation_util import set_global_references, sentence_editdistance
from asr_tools.evaluation_util import print_diff, sum_evals

from asr_tools.nbest_util import print_nbest, print_nbest_ref_hyp_best, nbest_best_sentence
from asr_tools.nbest_util import evaluate_nbests, evaluate_nbest, evaluate_nbests_oracle, evals_by_depth
from asr_tools.nbest_util import print_nbest_ref_hyp_best, print_nbests, print_eval, print_train_test_eval

from asr_tools.scores import monotone
from asr_tools.reranking import rerank_nbest, rerank_nbests

class Testing(unittest.TestCase):
    """Class for testing asr_tools package."""

    ref_file = "test/data/ref.txt"
    hyp_file = "test/data/hyp.txt"
    nbest_file = "test/data/nbest.txt"

    refs = None
    hyps = None

    @classmethod
    def setUpClass(cls):
        # Load the major objects that we'll use for the tests
        with open(cls.ref_file) as f:
            cls.refs = read_transcript_table(f)
        with open(cls.ref_file) as f:
            set_global_references(f)
        with open(cls.hyp_file) as f:
            cls.hyps = read_transcript(f)
        with open(cls.nbest_file) as f:
            cls.nbests = list(read_nbest_file(f))

        cls.s1 = cls.hyps[0]
        cls.s2 = get_global_reference(cls.s1.id_)

        # Evaluate each and check their WER
        cls.e1 = evaluate(cls.refs, cls.s1)
        cls.e2 = evaluate(cls.refs, cls.s2)
        
    def test_evaluation(self):
        # Evaluate all of the hyps
        e = evaluate_hyps(self.hyps, self.refs)
        self.assertAlmostEqual(e.wer(), 0.0955, delta=0.001)

    def test_sent_editdistance(self):
        # Check if we can run edit distance successfully
        self.assertTrue(sentence_editdistance(self.s1, self.s2) == 1)

    def test_evaluation_summation(self):
        # Check if the evaluation summation works correctly
        self.assertAlmostEqual(sum_evals([self.e1, self.e2]).wer(), 0.0294, delta=0.001)
        self.assertAlmostEqual(sum_evals([self.e1]).wer(), 0.0588, delta=0.001)

    def test_evaluation_object(self):
        # Excersise all the functions of an evaluation object
        self.assertAlmostEqual(self.e1.wer(), 0.0588, delta=0.001)
        self.assertAlmostEqual(self.e1.wrr(), 0.9411, delta=0.001)
        self.assertFalse(self.e1.is_correct())
        self.assertFalse(self.e1 < self.e2)
        self.assertAlmostEqual(self.e1.wer(), 0.0588, delta=0.001)
        self.assertEqual(self.e2.wer(), 0.0)

    def test_invalid_id(self):
        # Make sure we get an exception if we have an invalid sentence ID
        s = copy.copy(self.s1)
        s.id_ = ""
        with self.assertRaises(Exception):
            evaluate(self.refs, s)

    def test_printing(self):
        # Make sure we can print without raising any exceptions.  Doesn't check for
        # correctness.
        with open(os.devnull, 'w') as f:
            sys.stdout = f
            print(self.e1)
            print_diff(self.s1, self.s2)
            print(self.nbests[0])

            # Commenting this out just to make a test pass :-(
            print_nbest(self.nbests[0],
                        acscore=True, lmscore=True, tscore=True, tscore_wip=True,
                        wcount=True, lmwt=10.0, maxwords=None, print_instances=True)
            print_nbest_ref_hyp_best(self.nbests[0])
            sys.stdout = sys.__stdout__

    def test_read_nbest(self):
        # Make sure we can read an n-best and get the right number of nbest lists back
        with open(self.nbest_file) as f:
            nbests = list(read_nbest_file(f))
            self.assertTrue(len(nbests) == 15)

    def test_read_transcript(self):
        # Make sure we can read a transcipt and get the right number back
        with open(self.ref_file) as f:
            refs = read_transcript_table(f)
            self.assertTrue(len(refs) == 15)

    def test_read_hyp(self):
        # Make sure we can read hypotheses and get the right number back
        with open(self.hyp_file) as f:
            hyps = read_transcript(f)
            self.assertTrue(len(hyps) == 15)

    def test_e2e_evaluation(self):
        # Run a full end-to-end evaluation of ASR hypotheses
        with open(self.hyp_file) as h, open(self.ref_file) as r:
            ref_table = read_transcript_table(r)
            hyps = read_transcript(h)
            evals = []
            for hyp in hyps:
                eval_ = evaluate(ref_table, hyp)
                evals.append(eval_)
            overall_eval = sum(evals[1:], evals[0])
            self.assertTrue(overall_eval.ref_len == 335)
            self.assertTrue(overall_eval.matches == 307)
            self.assertTrue(overall_eval.errs == 32)

    # This is relatively slow too...
    # def test_evaluate_nbest(self):
    #     eval_ = evaluate_nbests(self.nbests)
    #     self.assertAlmostEqual(eval_.wer(), 0.1134, delta=0.001)

    # This is rather slow, so let's exclude it for now
    # Why is it slow...?
    # def test_nbest_oracle_sort(self):
    #     ret = nbest_oracle_sort(self.nbests[0])
    #     # Should do an evalutation of some sort to test for correctness

    # this takes about 2 seconds
    def test_evaluation2(self):
        nbest = self.nbests[0]
        eval_ = evaluate_nbest(nbest)
        best_sentence = nbest_best_sentence(nbest)
        self.assertTrue(best_sentence.wer() == 0.0)
        all_nbests_eval = evaluate_nbests(self.nbests)
        self.assertAlmostEqual(all_nbests_eval.wer(), 0.1134, delta=0.001) 
        oracle_eval = evaluate_nbests_oracle(self.nbests)
        self.assertTrue(oracle_eval.wer() == 0.06865671641791045)
        evals = evals_by_depth(self.nbests, n=10)
        self.assertTrue(evals[5].wer() == 0.08059701492537313)

    # This doesn't check correctness, it just checks that these functions
    # can be called without throwing an error
    def test_nbest_printing(self):
        sys.stdout = open(os.devnull,"w")
        print_nbests(self.nbests)
        print_nbest_ref_hyp_best(self.nbests[0])
        eval_ = evaluate_nbest(self.nbests[0])
        print_train_test_eval(self.nbests, self.nbests)
        sys.stdout.close()
        sys.stdout = sys.__stdout__
 
    def test_scoring(self):
        print(monotone(self.nbests[0].sentences, comparison=operator.lt, key=Sentence.score))


    #TODO - Add tests for re<ranking.py
