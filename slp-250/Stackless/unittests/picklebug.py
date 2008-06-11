"""
This file was needed to figure out a deep problem with generator pickling.
I'm adding this file to the unittests as a template to cure similar
problems in the future. This file only works in a debug build.
"""

import sys, gc
import cPickle as pickle
from stackless import *

try:
    genschedoutertest
except NameError:
    try:
        execfile("test_pickle.py")
    except SystemExit:
        pass

t=tasklet(genschedoutertest)(20,13)
t.run()
s = pickle.dumps(t)
t.run()
del t
pre = None
post = None
newob = None
del pre, post, newob
gc.collect()
pre = stackless._get_all_objects()
post = pre[:]

print "refs before unpickling, objects", sys.gettotalrefcount(), len(pre)
pickle.loads(s).run()
post = None
gc.collect()
post = stackless._get_all_objects()
for i, ob in enumerate(post):
    if id(ob) == id(pre):
        del post[i]
del i, ob
gc.collect()
print "refs after  unpickling, objects", sys.gettotalrefcount(), len(post)
newob = post[:len(post)-len(pre)]
print "look into newob"
del pre, post
gc.collect()
