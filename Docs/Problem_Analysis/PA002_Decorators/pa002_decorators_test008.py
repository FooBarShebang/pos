#!/usr/bin/python

import functools
import inspect

def stat_meth_dbc(strClass):
    """
    Implements 'Design by Contract' for static methods via a parametric
    decorator.
    """
    def wrapper(input_func):
        """
        Closure of 'stat_meth_dbc' decorator.
        """
        @functools.wraps(input_func)
        def decorated(*args, **kwargs):
            """
            Closure of 'wrapper' closure of 'stat_meth_dbc' decorator.
            Implements input and output data check for the static method
            to be decorated.
            """
            print 'Design by Contract:'
            print 'Input check for {}.{}'.format(strClass,
                                                    input_func.__name__)
            print input_func.__doc__
            print inspect.getargspec(input_func)
            print inspect.getcallargs(input_func, *args, **kwargs)
            gResult = input_func(*args, **kwargs)
            print 'Output type: {}'.format(type(gResult))
            return gResult
        return decorated
    return wrapper

class Test_Class(object):
    """
    Class to be tested in terms of 'Design by Contract' decorator.
    """
    
    @staticmethod
    @stat_meth_dbc('Test_Class')
    def test_meth(a, b, *args, **kwargs):
        """
        Static method test_meth to be tested in terms of 'Design by
        Contract' decorator.
        """
        print 'Inside test method'
        return '{} != {}'.format(a, b)

#test area

objTest = Test_Class()
print Test_Class.test_meth(1, 2, "test")
print Test_Class.test_meth.__name__
print Test_Class.test_meth.__doc__
print
print objTest.test_meth(1, 2, "test")
print objTest.test_meth.__name__
print objTest.test_meth.__doc__
