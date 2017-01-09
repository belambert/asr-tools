"""
Utility functions for I/O.
"""

import gzip

def open_file_stream(filename):
    """Open specified filename and return a stream.  If the filename ends
    with a '.gz' then read the file as a gzip file.  This is used in some
    of the argparse definitions for this project."""
    if filename.endswith('.gz'):
        return gzip.open(filename, 'rt')
    else:
        return open(filename, 'rt')
