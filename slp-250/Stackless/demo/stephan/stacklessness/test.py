from stacklessness import *

def f():
    print 'f1'
    schedule()
    print 'f2'

def g():
    print 'g1'
    schedule()
    print 'g2'
    
def h():
    print 'h1'
    schedule()
    print 'h2'
    
t1 = tasklet(f)()
t2 = tasklet(g)()
t3 = tasklet(h)()
t1.run()
