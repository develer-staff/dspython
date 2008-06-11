from stackless import *

test_exception = 0

ch = channel()

def f1(n):
    print "f1 called"
    for i in xrange(n):
        #print "f1", i
        if i == 4:
            if test_exception:
                1/0
        if i % 100 == 0:
            schedule()

def f2(n):
    print "f2 called"
    for i in xrange(n):
        #print "f2", i
        if i % 100 == 0:
            schedule()

def tt(n, timeout):
    t1 = tasklet(f1)(n)
    t2 = tasklet(f2)(n)
    t1.insert()
    t2.insert()
    global victim
    victim = run_watchdog(timeout)
    # print"*ick*"
    # do not print, this kills PyWin.
    # also re-insert and let it finish!
    victim.run()

tt(10, 100)
if victim:
    print "Watchdog was called"
    print victim
    

def infinite():
    global count
    count = 0
    while 1:
        count += 1

def test_inf(limit):
    print "calling infinite"
    tasklet(infinite)().insert()
    victim = run_watchdog(limit)
    if victim:
        print "gotcha!"
    print "%d reached after %d iterations." % (limit, count)
    