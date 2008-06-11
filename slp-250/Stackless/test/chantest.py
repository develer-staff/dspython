def receiver(chan, name):
    while 1:
        try:
            data = chan.receive()
        except:
            print name, "** Ouch!!! **"
            raise
        print name, "got:", data
        if data == 42:
            chan.send("%s says bye" % name)
            return

import stackless, sys

# the following two are here to check about the bad
# situation that main is blocked and no sender is available.
def test_recv():
    c = stackless.channel()
    def foo(c):
        c.send(5)
    t = stackless.tasklet(foo)(c)
    print 'first receive'
    c.receive()
    print 'second receive'
    c.receive()

def test_send():
    c = stackless.channel()
    def foo(c):
        c.receive()
        stackless.schedule()
    t = stackless.tasklet(foo)(c)
    print 'first send'
    c.send(5)
    print 'second send'
    c.send(5)

chan = stackless.channel()
t1 = stackless.tasklet(receiver)(chan, "inky")
t2 = stackless.tasklet(receiver)(chan, "dinky")
stackless.run()
try:
    for i in 2,3,5,7, 42:
        print "sending", i
        chan.send(i)
        chan.send(i)
        if i==7:
            print "sending Exception"
            chan.send_exception(ValueError, i)
except ValueError:
    e, v, t = sys.exc_info()
    print e, v
    del e, v, t
print "main done."
#
# trying to clean up things, until we have a real
# channel deallocator:
print "trying cleanup:"
while chan.balance:
    if chan.balance < 0:
        chan.send(42)
    else:
        print chan.receive()
