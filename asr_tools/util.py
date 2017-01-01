import sys
import time

class Timer:
    """Keep track of execution time, printing status and time before and after."""

    def __init__(self, name='Timing'):
        """Optionally give it a name."""
        self.name = name
    
    def __enter__(self):
        sys.stdout.write("{:30}".format(self.name + '...'))
        sys.stdout.flush()
        self.start = time.clock()
        return self

    def __exit__(self, *args):
        self.end = time.clock()
        self.interval = self.end - self.start
        sys.stdout.write(" {:.3f}s".format(self.interval))
        print()
        sys.stdout.flush()
