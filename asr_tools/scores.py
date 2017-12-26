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
File for storing score related functions.  Currently this only has one function, 'monotone',
which I'm using to check if n-bests are correctly sorted.
"""

import operator

def monotone(L, comparison=operator.lt, key=lambda x: x):
    """Check if all the numbers are monotonically increasing."""
    return all(comparison(key(x), key(y)) for x, y in zip(L, L[1:]))
