# (E)a(z)y (log)ging

Wrappers to make eazy logging of functions and members calls.
Allow to track parameters, exceptions and performance of functions.

# Installation

Simple as `pip3 install exlog`

# Some examples on how to use it

To log function call
```python
from ezlog import log_call

@log_call
def test(a, b):
    print("test_fiunction_called")
    return 4

test(2, "test")
```

To log class member call
```python
from ezlog import log_member_call

 class A:
	@log_member_call
    def test(self, a, b, **kwargs):
		print("test_called")

a=A()
a.test(2, 4, test={"d":"t", "c":"o"})
```

# Customization
