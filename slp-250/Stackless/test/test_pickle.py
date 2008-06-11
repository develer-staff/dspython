import sys, cPickle, pickle

from stackless import *

def run_pickled(func, *args):
    t = tasklet(func)(*args)
    print "starting tasklet"
    t.run()

    print "pickling"
    # hack for pickle
    if pickl == pickle:
        t.tempval = None
    pi = pickl.dumps(t)
    t.remove()
    #print pi
    file("temp.pickle", "wb").write(pi)

    print "unpickling"
    ip = pickl.loads(pi)

    print "starting unpickled tasklet"
    ip.run()

def test(n, when):
    for i in range(n):
        if i==when:
            schedule()
        print i

def rectest(nrec, lev=0):
    print lev*" " + "entering", lev+1
    if lev < nrec:
        rectest(nrec, lev+1)
    else:
        schedule()
    print lev*" " + "leaving", lev+1

pickl = pickle # note that the refcounts are correct with pickle.py
# but also note that in 2.2, pickle seems broken for extension types
# which are referencing themselves...

print
print "testing pickled iteration"
print 60*"-"
print
run_pickled(test, 20, 13)
print
print "testing pickled recursion"
print 60*"-"
print
run_pickled(rectest, 13)
