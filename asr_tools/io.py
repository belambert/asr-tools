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
