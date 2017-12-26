# Copyright 2012-2018 Ben Lambert

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
Print a sentence, optionally with lots of additional information like the ASR scores.
"""

from io import StringIO

# TODO - This doesn't actually print it, it returns a string...
def print_sentence(s, acscore=True, lmscore=True, tscore=True, tscore_wip=False,
                   wcount=False, lmwt=10.0, maxwords=None, wer=True):
    """Prints all sentence scores including acoustic, lm, overall, etc."""
    output = StringIO()
    number_template = '{:8,.2f}'
    spaces = 2
    if maxwords:
        sentence_str = ' '.join(s.words[:maxwords]).lower()
    else:
        sentence_str = ' '.join(s.words).lower()
    if acscore:
        output.write(number_template.format(s.acscore) + ' ' * spaces)
    if lmscore:
        output.write(number_template.format(s.lmscore) + ' ' * spaces)
    if tscore:
        output.write(number_template.format(s.score(lmwt=lmwt)) + ' ' * spaces)
    if tscore_wip:
        output.write(number_template.format(s.score(lmwt=lmwt) + len(s.words) * 0.5) + ' ' * spaces)
    if wcount:
        output.write('{:5}'.format(len(s.words)) + ' ' * spaces)
    if wer and s.eval_:
        output.write('{:5.0%}  '.format(s.eval_.wer()))

    output.write(sentence_str)
    return output.getvalue()
