"""Unsure, if an explicit tasklet.become(tasklet()) should be tested."""

import unittest
import sys
from stackless import tasklet, channel, getcurrent

VERBOSE = False


class TestTaskletBecome(unittest.TestCase):
    def testSimpleTaskletBecome(self):
        def f(ch):
            if VERBOSE: print "\tBecoming a tasklet inside f(ch)"
            #become_tasklet()
            got = tasklet().capture(42)
            yum = repr(got)
            res = ch.receive()
            if VERBOSE:
                print "\tCaptured inside    f(ch):", yum
                print "message received: " + res
                print "\tFunction f(ch) finished"

        ch = channel()
        if VERBOSE:
            print
            print "First in main(TestTaskletBecome):",
        foo =  getcurrent()
        if VERBOSE:
            print foo
            print "Now calling a function f(ch)"
        bar = f(ch)
        if VERBOSE: print "Back in  main(TestTaskletBecome):", bar
        ch.send("Did it work out right?")
        self.assertEquals(42, bar)


if __name__ == '__main__':
    if not sys.argv[1:]: sys.argv.append('-v')
    unittest.main()
