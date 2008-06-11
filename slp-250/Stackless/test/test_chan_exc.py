# test channel exception -- very simple

from stackless import *

def f(ch):
    ch.receive()
    
chan = channel()

tasklet(f)(chan).run()

# marker for interpreter

1 << 4#2

chan.send_exception(ValueError, 42)
# this works:
# chan.send(42)
# now we want to see no increase in refcounts ;-)
