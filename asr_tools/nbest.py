import sys

from io import StringIO

from asr_tools.sentence import Sentence
from asr_tools.evaluation_util import get_global_reference
from asr_tools.evaluation_util import print_diff
from asr_tools.nbest_util import nbest_best_sentence

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

    def print_with_wer(self):
        """Returns a string representation of the object."""
        best = nbest_best_sentence(self)
        best_rank = self.sentences.index(best)
        print_str = StringIO()
        print_str.write('ID: {} (#{} is best)\n'.format(self.id_, best_rank))
        for i, s in enumerate(self.sentences):
            print_str.write('{:3d} {}'.format(i + 1, s))
            if best_rank == i:
                print_str.write(' **')
            print_str.write('\n')
        print(print_str.getvalue())

    def print_ref_hyp_best(self):
        """Print three sentences: the reference, the top hypothesis, and the lowest WER
        hypothesis on the n-best list."""
        ref = get_global_reference(self.id_)
        hyp = self.sentences[0]
        best = nbest_best_sentence(self)
        best_rank = self.sentences.index(best)
        print_diff(ref, best, prefix1='REF: ', prefix2='BEST:')
        print_diff(best, hyp, prefix1='BEST:', prefix2='HYP: ')
        print('=' * 60)

# This is another possible way to print the ref/hyp/best
# print_str = ''
# print_str += 'ID: {} (#{} is best)\n'.format(self.id_, best_rank)
# if get_global_reference(self.id_):
#     print_str += '{:3} '.format('') + str(ref) + '\n'
# else:
#     print_str += '    No reference found.\n'
# print_str += '{:3d} '.format(1) + str(hyp) + '\n'
# print_str += '{:3d} '.format(best_rank + 1) + str(best) + '\n'
# print(ref)
