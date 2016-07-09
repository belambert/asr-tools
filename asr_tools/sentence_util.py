from io import StringIO

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
