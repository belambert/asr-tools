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
A context-based timer, which is useful because we've been doing a lot of timing lately.
"""

import sys
import time

class Timer:
    """Keep track of execution time, printing status and time before and after."""

    def __init__(self, name='Timing'):
        """Optionally give it a name."""
        self.name = name
        self.start = None
        self.end = None
        self.interval = None

    def __enter__(self):
        """When the context in entered, start the timer and print the timer name."""
        sys.stdout.write("{:30}".format(self.name + '...'))
        sys.stdout.flush()
        self.start = time.clock()
        return self

    def __exit__(self, *args):
        """When we leave the context, stop the timer and print how long it too."""
        self.end = time.clock()
        self.interval = self.end - self.start
        sys.stdout.write(" {:.3f}s".format(self.interval))
        print()
        sys.stdout.flush()
