from stackless import *

import sys

def f():
    print "in function"
    print sys.exc_info()
    
def testfunc():
    try:
        1/0
    except:
        print "before tasklet"
        print sys.exc_info()
        tasklet(f)().run()
        print "after tasklet"
        print sys.exc_info()

# make sure that we run toplevel
print "hard switching"
stackless.enable_softswitch(0)
tasklet(testfunc)()
run()
print "soft switching"
stackless.enable_softswitch(1)
tasklet(testfunc)()
run()
