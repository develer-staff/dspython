import stackless
import util
import pickle

count = 0
niceTasklet = None

def NiceFunction():
    global count
    print "NiceFunction:Enter"
    try:
        while 1:
            util.BeNice()
            count += 1
    except:
        print "NiceFunction:Error"

def Pickler():
    global niceTasklet, count
    while 1:
        util.BeNice()
        if count >= 10:
            count = 0
            print "dump",
            s = pickle.dumps(niceTasklet)
            print "kill",
            niceTasklet.kill()
            print "load",
            niceTasklet = pickle.loads(s)
            print "insert"
            niceTasklet.insert()

def Run():
    global niceTasklet
    print "Run:Enter"
    niceTasklet = stackless.tasklet(NiceFunction)()
    stackless.tasklet(Pickler)()
    print "Run:Exit"
