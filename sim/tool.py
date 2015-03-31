import functools
import time, threading

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
            current_thread = threading.currentThread()
            print '[At %s: %03d] func %s takes %ds' % (current_thread, int(time.time())%100, f.__name__, duraction, )
            return r
        return wrapper
    return performance_decorator
