import unittest
import logging
from unittest.mock import MagicMock, call
from ezlog import log_call, log_member_call
from ezlog import wrappers


class Test_log_call(unittest.TestCase):

    def setUp(self):
        self.log = MagicMock()
        wrappers.default_logging = MagicMock()
        wrappers.default_logging.log = self.log

    def test_log(self):
        
        @log_call()
        def test_func_name(a, b):
            return 'ret_val'

        test_func_name('test_param1', 'test_param2')

        intro = self.log.call_args_list[0][0]
        self.assertEqual(wrappers.default_log_level, intro[0])
        self.assertEqual(intro[1],
                         "Calling 'test_func_name' with args:"
                         " ('test_param1', 'test_param2'):")
        ending = self.log.call_args_list[1][0]
        self.assertEqual(wrappers.default_log_level, ending[0])
        self.assertEqual(ending[1],
                         "Done 'test_func_name', with result: 'ret_val'")

    def test_log_one_line(self):
        
        @log_call(one_line=True)
        def func_name(a, b):
            return 'ret_val'

        func_name('test_param1', 'test_param2')

        one_line = self.log.call_args_list[0][0]
        self.assertEqual(wrappers.default_log_level, one_line[0])
        self.assertEqual(one_line[1],
                         "Called 'func_name' with args: "
                         "('test_param1', 'test_param2'),"
                         " with result: 'ret_val'")

    def test_exception(self):

        class TestExClass(Exception):
            pass

        @log_call()
        def func_name():
            raise TestExClass('TEST_EXCEPTION')
        
        raised = False

        try:
            func_name()
            self.fail()
        except TestExClass:
            raised = True

        self.assertTrue(raised)

        intro = self.log.call_args_list[0][0]
        self.assertEqual(wrappers.default_log_level, intro[0])
        self.assertEqual(intro[1],
                         "Calling 'func_name':")
        ex = self.log.call_args_list[1][0]
        self.assertEqual(logging.ERROR, ex[0])
        self.assertEqual(ex[1], "Done 'func_name' with exception")
        self.assertTrue('exc_info' in self.log.call_args_list[1][1])

class Test_log_member_call(unittest.TestCase):

    def setUp(self):
        self.log = MagicMock()
        wrappers.default_logging = MagicMock()
        wrappers.default_logging.log = self.log

    def test_log(self):
        
        class TestClass():
            @log_member_call()
            def test_func_name(self, a, b):
                return 'ret_val'
        
        a = TestClass()
        a.test_func_name('test_param1', 'test_param2')

        intro = self.log.call_args_list[0][0]
        self.assertEqual(wrappers.default_log_level, intro[0])
        self.assertEqual(intro[1],
                         "Calling "
                         "'Test_log_member_call.test_log.<locals>."
                         "TestClass.test_func_name'"
                         " with args:"
                         " ('test_param1', 'test_param2'):")
        ending = self.log.call_args_list[1][0]
        self.assertEqual(wrappers.default_log_level, ending[0])
        self.assertEqual(ending[1],
                         "Done "
                         "'Test_log_member_call.test_log.<locals>."
                         "TestClass.test_func_name'"
                         ", with result: 'ret_val'")
        
"""
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