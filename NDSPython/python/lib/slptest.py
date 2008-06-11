import stackless
import uthread

def Receiver(channel):
    print "  Receiver (before)"
    value = channel.receive()
    print "  Received:", value

def Sender(channel):
    print "  Sender (before)"
    channel.send("hello")
    print "  Sender (after)"

def Threebie():
    for i in xrange(3):
        print "  Threebie (iteration %d/%d)" % (i+1, 3)
        stackless.schedule()

def Test():
    print "***** Sender / Receiver (stackless)"

    channel = stackless.channel()
    stackless.tasklet(Sender)(channel) # .name = "Sender"
    stackless.tasklet(Receiver)(channel) # .name = "Receiver"
    stackless.tasklet(Threebie)() # .name = "Threebie"

    while stackless.runcount > 1:
        t = stackless.run(10000)
        if t:
            print "Timed out tasklet", t

    print "***** Receiver / Sender (stackless)"

    channel = stackless.channel()
    stackless.tasklet(Receiver)(channel)# .name = "Receiver"
    stackless.tasklet(Sender)(channel) # .name = "Sender"

    while stackless.runcount  > 1:
        t = stackless.run(10000)
        if t:
            print "Timed out tasklet", t

    print "***** Sender / Receiver (uthread)"

    channel = stackless.channel()
    uthread.new(Sender, channel) # .name = "Sender"
    uthread.new(Receiver, channel) # .name = "Receiver"
    uthread.new(Threebie) # .name = "Threebie"

    uthread.run()

    print "***** Receiver / Sender (uthread)"

    channel = stackless.channel()
    uthread.new(Receiver, channel) # .name = "Receiver"
    uthread.new(Sender, channel) # .name = "Sender"

    uthread.run()

if __name__ == "__main__":
    Test()
