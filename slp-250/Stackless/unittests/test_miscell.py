# import common

import pickle
import unittest
import stackless

def is_soft():
    softswitch = stackless.enable_softswitch(0)
    stackless.enable_softswitch(softswitch)
    return softswitch

def runtask():
    x = 0
    # evoke pickling of an xrange object
    dummy = xrange(10)
    for ii in xrange(1000):
        x += 1


class TestWatchdog(unittest.TestCase):

    def lifecycle(self, t):
        # Initial state - unrun
        self.assert_(t.alive)
        self.assert_(t.scheduled)
        self.assertEquals(t.recursion_depth, 0)
        # allow hard switching
        t.set_ignore_nesting(1)
        
        # Run a little
        res = stackless.run(10)
        self.assertEquals(t, res)
        self.assert_(t.alive)
        self.assert_(t.paused)
        self.failIf(t.scheduled)
        self.assertEquals(t.recursion_depth, 1)

        # Push back onto queue
        t.insert()
        self.failIf(t.paused)
        self.assert_(t.scheduled)
        
        # Run to completion
        stackless.run()
        self.failIf(t.alive)
        self.failIf(t.scheduled)
        self.assertEquals(t.recursion_depth, 0)
        

    def test_aliveness1(self):
        """ Test flags after being run. """
        t = stackless.tasklet(runtask)()
        self.lifecycle(t)

    def test_aliveness2(self):
        """ Same as 1, but with a pickled unrun tasklet. """
        import pickle
        t = stackless.tasklet(runtask)()
        t_new = pickle.loads(pickle.dumps((t)))
        t.remove()
        t_new.insert()
        self.lifecycle(t_new)
   
    def test_aliveness3(self):
        """ Same as 1, but with a pickled run(slightly) tasklet. """

        t = stackless.tasklet(runtask)()
        t.set_ignore_nesting(1)

        # Initial state - unrun
        self.assert_(t.alive)
        self.assert_(t.scheduled)
        self.assertEquals(t.recursion_depth, 0)

        # Run a little
        res = stackless.run(100)
        
        self.assertEquals(t, res)
        self.assert_(t.alive)
        self.assert_(t.paused)
        self.failIf(t.scheduled)
        self.assertEquals(t.recursion_depth, 1)
        
        
        # Now save & load
        dumped = pickle.dumps(t)
        t_new = pickle.loads(dumped)        

        # Remove and insert & swap names around a bit
        t.remove()
        t = t_new
        del t_new
        t.insert()

        self.assert_(t.alive)
        self.failIf(t.paused)
        self.assert_(t.scheduled)
        self.assertEquals(t.recursion_depth, 1)
        
        # Run to completion
        if is_soft():
            stackless.run()
        else:
            t.kill()
        self.failIf(t.alive)
        self.failIf(t.scheduled)
        self.assertEquals(t.recursion_depth, 0)
    
#///////////////////////////////////////////////////////////////////////////////

if __name__ == '__main__':
    import sys
    if not sys.argv[1:]:
        sys.argv.append('-v')

    unittest.main()
