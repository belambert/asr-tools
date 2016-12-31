import time

class Timer:

    def __init__(self, name='timer'):
        self.name = name
    
    def __enter__(self):
        print("Starting {} timer.".format(self.name))
        self.start = time.clock()
        return self

    def __exit__(self, *args):
        self.end = time.clock()
        self.interval = self.end - self.start
        print('{} took: {:.3f} seconds'.format(self.interval))
