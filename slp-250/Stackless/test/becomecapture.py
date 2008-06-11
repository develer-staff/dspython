from stackless import *
def testit():
    print "capture"
    print repr(tasklet().capture(None))
    print "become"
    print repr(tasklet().become(None))
    print "capture"
    print repr(tasklet().capture(None))
    print "become"
    print repr(tasklet().become(None))
    print "done"
testit()
