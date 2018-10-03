#!/usr/bin/python

import functools
import inspect

def class_meth_dbc(method):
    """
    Implements 'Design by Contract' for class methods via decorator.
    """
    @functools.wraps(method)
    def decorated(instance, *args, **kwargs):
        """
        Decorator 'class_meth_dbc' closure. Implements input and output
        data check for the class method to be decorated.
        """
        print 'Design by Contract:'
        print 'Input check for {}.{}'.format(
                                    instance.__name__, method.__name__)
        print method.__doc__
        print inspect.getargspec(method)
        print inspect.getcallargs(method, instance, *args, **kwargs)
        gResult = method(instance, *args, **kwargs)
        print 'Output type: {}'.format(type(gResult))
        return gResult
    return decorated

class Test_Class(object):
    """
    Class to be tested in terms of 'Design by Contract' decorator.
    """
    
    @classmethod
    @class_meth_dbc
    def test_meth(cls, a, b, *args, **kwargs):
        """
        Class method test_meth to be tested in terms of 'Design by
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
