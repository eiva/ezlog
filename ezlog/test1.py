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

    a=A()
    a.test(2, 4, test={"d":"t", "c":"o"})

    test(1, 2)