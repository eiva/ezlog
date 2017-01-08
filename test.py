from typing import Callable, Dict, Any, TypeVar, cast
from functools import wraps

I = TypeVar('I')
IKW = TypeVar('IKW')
O = TypeVar('O')
TFun = TypeVar('TFun', bound=Callable[..., Any])

# https://github.com/python/mypy/issues/1551

"""
def log_call(**opt: Dict[str, Any]) -> Callable[[Callable[[I], O]], Callable[[I], O]]:
    def decorator(f: Callable[[I], O]) -> Callable[[I], O]:
        def log_call_wrapper(*args: Any) -> Any:
            return f(*args)
        return log_call_wrapper
    return decorator
"""

class log_call:
    def __init__(self, **kwargs: Any) -> None:
        pass

    def __call__(self, f: TFun) -> TFun:
        @wraps(f)
        def wrapper(*args, **kwargs) -> Any:
            return f(*args, **kwargs)
        return cast(TFun, wrapper)

"""
Working solution #1
def log_call(f: Callable[[I], O]) -> Callable[[I], O]:
    def log_call_wrapper(*args: I, **kwargs:Any) -> O:
        return cast(Any, f)(*args, **kwargs)
    return log_call_wrapper
"""

@log_call()
def test(a: int)->str:
   return str(a)

test("test")

