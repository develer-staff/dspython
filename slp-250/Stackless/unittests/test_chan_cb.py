import unittest


class ChannelMonitor:
    "A channel monitor acting as a callback for set_channel_callback()."
    
    def __init__(self):
        self.history = []

    def __call__(self, channel, tasklet, isSending, willBlock):
        tup = (channel, tasklet, isSending, willBlock, tasklet.tempval)
        self.history.append(tup)
        

class ChannelCallbackTestCase(unittest.TestCase):
    "A collection of channel callback tests."
    
    def test0(self):
        "Simple monitored channel send from main tasklet."

        import stackless

        # create players
        chan = stackless.channel()
        main = stackless.getmain() # implicit sender
        receiver = stackless.tasklet(lambda ch:ch.receive())
        receiver = receiver(chan)

        # send a value to a monitored channel
        chanMon = ChannelMonitor()
        stackless.set_channel_callback(chanMon)
        val = 42
        chan.send(val)
        stackless.set_channel_callback(None)

        # compare sent value with monitored one
        # found = chanMon.history[0][1].tempval
        # self.failUnlessEqual(val, found) # FAILS - why?
        # 
        # fails, because the value is moved from sender to receiver
        # also, I need to modify channels a little :-)
        # this one works, because I keep a copy of the value.
        # 
        # print chanMon.history
        found = chanMon.history[0][-1]
        self.failUnlessEqual(val, found)


if __name__ == "__main__":
    unittest.main()
