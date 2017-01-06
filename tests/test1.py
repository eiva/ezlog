import unittest


class Test_test1(unittest.TestCase):

    def test_A(self):
        pass

if __name__ == '__main__':
    unittest.main()

    @log_call
    def test(a, b):
        print("test_fiunction_called")
        return 4

    class A:

        @log_member_call
        def test(self, a, b, **kwargs):
            print("test_called")

    a = A()
    a.test(2, 4, test={"d": "t", "c": "o"})

    test(1, 2)

"""
default_log_level = logging.ERROR


@log_call() # Make sure you dont forget about ()
def test(a, b):
    print("A")
    raise Exception
    return 4

def a():
    test(2, "test")

#a()
test(2, 2)


print("-----------")
class A(object):
    @log_member_call()
    def a(self):
        raise Exception("test")
    def b(self):
        raise Exception("test")
try:
    A().a()
except Exception as e:
    print("Catched")
    raise
    

print("-----------")
"""