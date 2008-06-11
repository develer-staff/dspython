"""
This module tests the stackless behavior, when an
object is destroyed inside a tasklet, that calls
a __del__ method. The problem is, that this __del__
is run with f_back == NULL. We have to take care
not to run this as tasklet, or supply an extra tasklet
object.mro
However, without taking care, this will crash.
"""

from stackless import *

class a:
    def __del__(self):
        pass

def bummer():
    x = a()

tasklet(bummer)().run()
