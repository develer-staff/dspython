"""
runAll.py

Runs all testcases in files named test_*.py.
Should be run in the folder Stackless/unittests.
"""


import os, sys, glob, unittest, stackless

def getsoft():
    hold = stackless.enable_softswitch(False)
    stackless.enable_softswitch(hold)
    return hold

def makeSuite(target):
    "Build a test suite of all available test files."

    suite = unittest.TestSuite()
    if '.' not in sys.path:
        sys.path.insert(0, '.')
    
    for idx, filename in enumerate(glob.glob('test_*.py')):
        modname = os.path.splitext(os.path.basename(filename))[0]
        module = __import__(modname)
        tests = unittest.TestLoader().loadTestsFromModule(module)
        use_it = target == 0 or idx+1 == target
        if use_it:
            suite.addTest(tests)
            if target > 0:
                print "single test of '%s', switch=%s" % \
                      (filename, ("hard", "soft")[getsoft()])

    return suite


if __name__ == '__main__':
    hold = stackless.enable_softswitch(True)
    try:
        target = int(sys.argv[1])
    except IndexError:
        try:
            target = TARGET
        except NameError:
            target = 0
    try:
        flags = True, False
        if target:
            flags = (flags[target > 0],)
            if abs(target) == 42:
                target = 0
        for switch in flags:
            stackless.enable_softswitch(switch)
            testSuite = makeSuite(abs(target))
            unittest.TextTestRunner().run(testSuite)
    finally:
        stackless.enable_softswitch(hold)
        