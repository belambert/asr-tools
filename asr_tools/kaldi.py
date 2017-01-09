"""
Functions primarily for reading and writing Kaldi transcripts
and n-best files.
"""

import logging
import itertools
from collections import OrderedDict
from asr_tools.nbest import NBest
from asr_tools.sentence import Sentence
from asr_tools.evaluation import Evaluation

LOGGER = logging.getLogger('asr_tools')

def read_transcript_table(f):
    """Given a file, read in the transcripts into a hash table
    indexed by IDs."""
    trans_table = OrderedDict()
    trans = read_transcript(f)
    for s in trans:
        trans_table[s.id_] = s
    return trans_table

def read_transcript(f):
    """Read a transcript file."""
    trans = []
    for line in f:
        line = line.strip()
        id_, words = line.split(maxsplit=1)
        s = Sentence(id_, words.split())
        trans.append(s)
    return trans

def read_nbest_file(f, progress=False):
    "Read a Kaldi n-best file."
    nbests = []
    nbest = []
    prev_id = None
    id_ = None
    while True:
        LOGGER.debug('|NBESTS| = {:,d}'.format(len(nbests)))
        LOGGER.debug('|NBEST| = {:,d}'.format(len(nbest)))
        entry = read_nbest_entry_lines(f)  # this is a sentence, which is spread across several lines
        LOGGER.debug('ENTRY: ' + str(entry))
        if not entry:
            nbests.append(NBest(nbest, id_))
            break
        # Just check if the ID changed, let entry_lines_to_sentence parse the ID line
        id_line = entry[0]
        id_ = id_line.split()[0].rsplit('-', maxsplit=1)[0]
        rank = int(id_line.split()[0].rsplit('-', maxsplit=1)[1])
        # Just starting out.
        if not prev_id:
            prev_id = id_
            assert rank == len(nbest) + 1
        # If the ID changed, then create an NBest, and start over.
        if id_ != prev_id:
            nbests.append(NBest(nbest, prev_id))
            nbest = []
            prev_id = id_
            if progress:
                if len(nbests) % 1000 == 0:
                    print('Read {:,d} nbests.'.format(len(nbests)))
        else:
            assert rank == len(nbest) + 1
        s = entry_lines_to_sentence(entry)
        nbest.append(s)
    return nbests

def read_nbest_entry_lines(f):
    """Read all the lines that correspond to a single sentence of a single nbest."""
    entry_lines = []
    while True:
        line = f.readline()
        if line == '':
            # When there's a blank line, return None
            if len(entry_lines) == 0:
                return None
            else:
                return entry_lines
        if line == '\n':
            return entry_lines
        else:
            entry_lines.append(line.strip())
    # TODO - Is this handling all cases?

def entry_lines_to_sentence(lines):
    """Convert all the string lines corresponding to a sentence into a
    sentence object."""
    words = []
    lmscores = []
    acscores = []
    id_line = lines.pop(0)
    id_tokens = id_line.split()
    id_ = id_tokens[0].rsplit('-', maxsplit=1)[0] # Get the ID
    evaluation = None
    # If there's more than one token on the first line, it's the evaluation.
    if len(id_tokens) > 1:
        _, reflen, matches, errs = id_tokens
        evaluation = Evaluation(int(reflen), int(matches), int(errs))
    # The last line should be a single token.
    assert len(lines[-1].split()) == 1
    for line in lines:
        tokens = line.split()
        if len(tokens) == 4:
            s1, s2, _, scores = tokens
            assert int(s1) == int(s2) - 1         # TODO - add more more sanity checks
            score_parts = scores.split(',')
            lmscores.append(float(score_parts[0]))
            acscores.append(float(score_parts[1]))
            words.append(tokens[2])
    lmscore = sum(lmscores)
    acscore = sum(acscores)
    sent = Sentence(id_, words, lmscore=lmscore, acscore=acscore, lmscores=lmscores, acscores=acscores)
    sent.eval_ = evaluation
    return sent

def write_nbests(f, nbests, save_eval=False):
    """Mimics Kaldi's output, which includes a lot of spaces at the end of lines."""
    for nbest in nbests:
        for i, sentence in enumerate(nbest.sentences, start=1):
            id_line = nbest.id_ + '-' + str(i)
            if save_eval:
                id_line = '{} {} {} {}'.format(id_line, sentence.eval_.ref_len,
                                               sentence.eval_.matches, sentence.eval_.errs)
            f.write(id_line + ' \n') # Kaldi puts an extra space here...
            f.write('0 1 <eps> \n')
            counter = 1
            for word, lmscore, acscore in itertools.zip_longest(sentence.words, sentence.lmscores,
                                                                sentence.acscores, fillvalue=0.0):
                f.write('{} {} {} {},{}, \n'.format(counter, counter+1, word, lmscore, acscore))
                counter += 1
            f.write('{} \n'.format(len(sentence.words) + 1))
            f.write('\n')
