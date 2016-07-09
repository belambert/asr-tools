import logging

from collections import OrderedDict

import asr_tools.logging
from asr_tools.nbest import NBest
from asr_tools.sentence import Sentence

logger = logging.getLogger('asr_tools')


def read_transcript_table(f):
    """Given a file, read in the transcripts into a hash table
    indexed by IDs."""
    trans_table = OrderedDict()
    trans = read_transcript(f)
    for s in trans:
        trans_table[s.id_] = s
    return trans_table

def read_transcript(f):
    trans = []
    for line in f:
        line = line.strip()
        id_, words = line.split(maxsplit=1)
        s = Sentence(id_, words.split())
        trans.append(s)
    return trans

def read_nbest_file(f):
    "Read a Kaldi n-best file."
    nbests = []
    nbest = []
    current_id = None
    prev_id = None
    id_ = None
    while True:
        logger.debug('|NBESTS| = {}'.format(len(nbests)))
        logger.debug('|NBEST| = {}'.format(len(nbest)))
        entry = read_nbest_entry_lines(f)  # this is a sentence, which is spread across several lines
        logger.debug('ENTRY: ' + str(entry))
        if not entry:
            nbests.append(NBest(nbest, id_))
            logger.debug(nbest)
            break
            # yield NBest(nbest, id_)
        id_ = entry[0]
        id_ = id_.rsplit('-', maxsplit=1)[0]
        if not prev_id:
            prev_id = id_
        if id_ != prev_id:
            nbests.append(NBest(nbest, prev_id))
            nbest = []
            prev_id = id_
        s = entry_lines_to_sentence(entry)
        nbest.append(s)
    return nbests

def read_nbest_entry_lines(f):
    entry_lines = []
    while True:
        line = f.readline()
        if line == '':
            if len(entry_lines) == 0:
                return None
            else:
                return entry_lines
        if line == '\n':
            return entry_lines
        else:
            entry_lines.append(line.strip())

def entry_lines_to_sentence(lines):
    words = []
    lmscores = []
    acscores = []
    id_ = lines.pop(0)
    id_ = id_.rsplit('-', maxsplit=1)[0]
    for line in lines:
        tokens = line.split()
        if len(tokens) == 4:
            s1, s2, word, scores = tokens
            assert(int(s1) == int(s2) - 1)
            score_parts = scores.split(',')
            lmscores.append(float(score_parts[0]))
            acscores.append(float(score_parts[1]))
            words.append(tokens[2])
    lmscore = sum(lmscores)
    acscore = sum(acscores)
    return Sentence(id_, words, lmscore=lmscore, acscore=acscore)

# def read_nbest_file(f):
#     "Read a Kaldi n-best file."
#     nbest = []
#     current_id = None
#     prev_id = None
#     id_ = None
#     while True:
#         entry = read_nbest_entry_lines(f)  # this is a sentence.
#         # logger.info('TEST')
#         # print(entry)
#         if not entry:
#             # print(nbest)
#             break
#             # yield NBest(nbest, id_)
#         id_ = entry[0]
#         id_ = id_.rsplit('-', maxsplit=1)[0]
#         if not prev_id:
#             prev_id = id_
#         if id_ != prev_id:
#             yield NBest(nbest, prev_id)
#             nbest = []
#             prev_id = id_
#         s = entry_lines_to_sentence(entry)
#         nbest.append(s)
