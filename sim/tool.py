import functools
import time

def performance(prefix):
    def performance_decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **argskw):
            if prefix.upper() != 'DEBUG':
                return f(*args, **argskw)
            t1 = time.time()
            r = f(*args, **argskw)
            t2 = time.time()
            duraction = t2 - t1
            print 'function %s takes %ds' % (f.__name__, duraction)
            return r
        return wrapper
    return performance_decorator
