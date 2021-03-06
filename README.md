# (E)a(z)y (log)ging

Wrappers to make eazy logging of functions and members calls.
Allow to track parameters, exceptions and performance of functions.

# Installation

Simple as `pip3 install ezlog`

# Some examples on how to use it

To log function call
```python
from ezlog.wrappers import log_call

@log_call()
def test(a, b):
    print("test_fiunction_called")
    return 4

test(2, "test")
```

To log class member call
```python
from ezlog.wrappers import log_member_call

 class A:
	@log_member_call()
    def test(self, a, b, **kwargs):
		print("test_called")

a=A()
a.test(2, 4, test={"d":"t", "c":"o"})
```

# Customization

Default behavior can be overriden using followin module wide parameters:

- default_log_level 
  Override for default logging level.

- default_performance_measure 
  Override default behavior for measuring performance or not.

- default_logging 
  Override default logger.

- default_eps
  Limit for prevent spamming extremely low measurements.

- default_one_line_log
  Override default logging style.
  If True - log only one line (Called (args), result)
  If False(default) - log in 2 lines (Calling... Done).

- default_log_arguments
  Override default settings to log arguments or not.

- default_log_result
  Override default settings to log function result or not.