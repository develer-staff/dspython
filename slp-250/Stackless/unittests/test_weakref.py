import unittest
import weakref
import gc

from stackless import *

class Counter(object):
    ctr = 0
    def __call__(self, *args):
        self.ctr += 1
        return self.ctr

    def get(self):
        return self.ctr

class TestWeakReferences(unittest.TestCase):
    def testSimpleTaskletWeakRef(self):
        counter = Counter()
        t = tasklet(lambda:None)()
        t_ref = weakref.ref(t, counter)
        self.assertEquals(t_ref(), t)
        del t
        # we need to kill it at this point to get collected
        stackless.run()
        self.assertEquals(t_ref(), None)
        self.assertEquals(counter.get(), 1)

    def testSimpleChannelWeakRef(self):
        counter = Counter()
        c = channel()
        c_ref = weakref.ref(c, counter)
        self.assertEquals(c_ref(), c)
        del c
        # we need to kill it at this point to get collected
        stackless.run()
        self.assertEquals(c_ref(), None)
        self.assertEquals(counter.get(), 1)

if __name__ == '__main__':
    import sys
    if not sys.argv[1:]:
        sys.argv.append('-v')
    unittest.main()
