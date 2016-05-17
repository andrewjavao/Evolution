import time
import datetime


def fprint(file, msg):
    msg = ("[%s] : %s\n") % (datetime.datetime.now(), msg)
    try:
        f = open(file, "a+")
        f.write(msg)
    except Exception, e:
        print(msg)
    finally:
        f.close()


MAX_ESCAPE_SHOCK_PERCENT = 0.05
DELTA_TIME = 2.0

is_continue = True
record_time = None



class foo(object):
    def __init__(self, a, b):
        self.a = a

    self.b = b
        print(self.a, self.b)


f = foo(1, 2)

