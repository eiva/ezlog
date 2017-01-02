import logging
from timeit import default_timer as timer

# import ptvsd
# shift-alt-f5

default_log_level = logging.DEBUG
'''
Override for default logging level.
'''
default_performance_measure = False
default_logging = logging
default_eps = 0.001

def __format_args(*args, **kwargs):
    args_str = str()
    kwargs_str = str()
    if len(args) != 0:
        args_str = " with args: {}".format(args)
    if len(kwargs) != 0:
       kwargs_str = " with kwargs: {}".format(kwargs)
    return args_str + kwargs_str

def __wrapper_impl(name, arg_fmt, f, opt, *args, **kwargs):
    log = opt.get("logger", default_logging)
    level = opt.get("level", default_log_level)
    measure = opt.get("measure", default_performance_measure)

    log.log(level, "Calling '{}'{}:".format(name, arg_fmt))
    try:
        if measure:
            start = timer()
        rv = f(*args, **kwargs)
        mesr_str = str()
        if measure:
            stop = timer()
            delta = stop - start
            if delta > default_eps:
                mesr_str = " and took: {}".format(delta)
        if rv == None:
            log.log(level, "Done '{}'{}".format(name, mesr_str))
        else:
            log.log(level, "Done '{}', with result: '{}'{}"
                    .format(name, rv, mesr_str))
        return rv
    except:
        log.exception("Done '{}' with exception")
        raise

def log_call(f, **kwargs):
    opt = kwargs
    def w(*args, **kwargs):
        name = f.__name__
        arg_fmt = __format_args(*args, **kwargs)
        __wrapper_impl(name, arg_fmt, f, opt, *args, **kwargs)
    return w

def log_member_call(f, **kwargs):
    opt = kwargs
    def w(slf, *args, **kwargs):
        name = "{}.{}".format(slf.__class__.__qualname__, f.__name__)
        arg_fmt = __format_args(*args, **kwargs)
        __wrapper_impl(name, arg_fmt, f, opt, slf, *args, **kwargs)
    return w