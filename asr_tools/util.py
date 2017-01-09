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
