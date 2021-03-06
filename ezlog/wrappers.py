import inspect
import logging
import traceback
import sys
from functools import wraps, update_wrapper, partial  # Todo!
from timeit import default_timer as timer
from typing import Callable, Any, TypeVar, cast


default_log_level = logging.DEBUG
'''
Override for default logging level.
'''

default_performance_measure = False
'''
Override default behavior for measuring performance or not.
'''

default_logging = logging
'''
Override default logger.
'''

default_eps = 0.001
'''
Limit for prevent spamming extremely low measurements.
'''

default_one_line_log = False
'''
Override default logging style.
If True - log only one line (Called (args), result)
If False(default) - log in 2 lines (Calling... Done).
'''

default_log_arguments = True
'''
Override default settings to log arguments or not.
'''

default_log_result = True
'''
Override default settings to log function result or not.
'''

TFun = TypeVar('TFun', bound=Callable[..., Any])
'''
Typedef for callback type checking.
'''


def _format_args(*args: Any, **kwargs: Any) -> str:
    args_str = str()
    kwargs_str = str()
    if len(args) != 0:
        args_str = " with args: {}".format(args)
    if len(kwargs) != 0:
        kwargs_str = " with kwargs: {}".format(kwargs)
    return args_str + kwargs_str


def _intro(name: str, arg_fmt: str, opt: Any) -> Any:
    log = opt.get("logger", default_logging)
    log_arguments = opt.get("log_arguments", default_log_arguments)
    one_line = opt.get("one_line", default_one_line_log)
    level = opt.get("level", default_log_level)
    if not log_arguments:
        arg_fmt = str()

    if not one_line:
        log.log(level, "Calling '{}'{}:".format(name, arg_fmt))
    return timer()


def _ending(result: Any, name: str,
            arg_fmt: str, opt: Any,
            intro_data: Any) -> None:
    log = opt.get("logger", default_logging)
    level = opt.get("level", default_log_level)
    measure = opt.get("measure", default_performance_measure)
    one_line = opt.get("one_line", default_one_line_log)
    log_result = opt.get("log_result", default_log_result)

    mesr_str = str()
    if measure:
        stop = timer()
        delta = stop - intro_data
        if delta > default_eps:
            mesr_str = " and took: {}".format(delta)

    res_str = str()
    if result and log_result:
        res_str = ", with result: '{}'".format(result)

    if one_line:
        log.log(level, "Called '{}'{}{}{}".
                format(name, arg_fmt, res_str, mesr_str))
    else:
        log.log(level, "Done '{}'{}{}".format(name, res_str, mesr_str))


def _exception(log: Any, name: str) -> BaseException:
    exc_type, exc_value, exc_traceback = sys.exc_info()
    try:
        exc_traceback = exc_traceback.tb_next
    except Exception:
        pass
    ex = exc_type(exc_value)
    ex.__traceback__ = exc_traceback
    ex.__cause__ = None
    log.log(logging.ERROR, "Done '{}' with exception".format(name),
            exc_info=(exc_type, exc_value, exc_traceback))
    return ex


class log_call(object):
    '''
    Wrapper to log function call.
    Not applicable to class member logging.

    Keyword arguments:

     level: int
      Default = ezlog.default_log_level
      Set log level for this call.

     one_line: bool
      Default = ezlog.default_one_line_log
      Allow to set different logging style.
      If True - log will be performed after call and looks like:
       'Called 'name', 'args' with result'
      If False - log will be performed before start and after start.

     log_arguments: bool
      Default = ezlog.default_log_arguments
      Should log function arguments or not.

     log_result: bool
      Default = ezlog.log_result
      Should log function result or not (if possible)

     measure: bool
      Default = ezlog.default_performance_measure
      Allow turn on or of performance measuring for this call.

     logger:
      Default = ezlog.default_logging
      Specify logger to be used.
      Expecting module or class with
       .log(int, str)

    Example:
    ```python
    >>> @log_call() # Make sure you dont forget about ()
    ... def test(a, b):
    ...  print("test call")
    ...  return 4
    >>>  test(2, "test")

    DEBUG:root:Calling 'test' with arguments (2, "test")
    test call
    DEBUG:root:Done 'test' with result '4'
    ```
    '''

    def __init__(self, **kwargs: Any) -> None:
        self._opt = kwargs

    def __call__(self, f: TFun) -> TFun:
        name = f.__name__

        @wraps(f)
        def log_call_wrapper(*args, **kwargs) -> Any:
            arg_fmt = _format_args(*args, **kwargs)
            data = _intro(name, arg_fmt, self._opt)
            try:
                ret = f(*args, **kwargs)
                _ending(ret, name, arg_fmt, self._opt, data)
                return ret
            except:
                log = self._opt.get("logger", default_logging)
                forward_exception = _exception(log, name)
                raise forward_exception  # This is wrapper - ignore it
        return cast(TFun, log_call_wrapper)


class log_member_call(object):
    '''
    Log call of class member function.
    (Not applicable for static or non class functions).
    For details see log_call.

    Example:
    ```python
    >>> class Test:
    ...  @log_member_call() # Make sure you dont forget about ()
    ...  def test(self, a, b):
    ...   print("test call")
    ...   return 4
    >>> t = Test()
    >>> t.test(2, "test")

    DEBUG:root:Calling 'Test.test' with arguments (2, "test")
    test call
    DEBUG:root:Done 'Test.test' with result '4'
    ```

    ```python
    class Test:
        @log_member_call(level = logging.CRITICAL)
        def test(self, a, b):
            print("test call {}, {}".format(a,b))
            return 4
    t = Test()
    print(t.test(2, "test"))
    CRITICAL:root:Calling 'Test.test' with args: (2, 'test'):
    test call 2, test
    CRITICAL:root:Done 'Test.test'
    ```
    '''
    def __init__(self, **kwargs: Any) -> None:
        self._opt = kwargs

    def __call__(self, f: TFun) -> TFun:
        @wraps(f)
        def log_member_call_wrapper(slf: Any, *args, **kwargs) -> Any:
            name = "{}.{}".format(slf.__class__.__qualname__, f.__name__)
            arg_fmt = _format_args(*args, **kwargs)
            data = _intro(name, arg_fmt, self._opt)
            try:
                ret = f(slf, *args, **kwargs)  # Calling wrapped function
                _ending(ret, name, arg_fmt, self._opt, data)
                return ret
            except:
                log = self._opt.get("logger", default_logging)
                forward_exception = _exception(log, name)
                raise forward_exception  # This is wrapper - ignore it
        return cast(TFun, log_member_call_wrapper)
