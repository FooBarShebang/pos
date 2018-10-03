#!/usr/bin/python

import functools
import inspect

def meth_dbc(method):
    """
    Implements 'Design by Contract' for instance methods via decorator.
    """
    @functools.wraps(method)
    def decorated(instance, *args, **kwargs):
        """
        Decorator 'meth_dbc' closure. Implements input and output data
        check for the instance method to be decorated.
        """
        print 'Design by Contract:'
        print 'Input check for {}.{}'.format(
                        instance.__class__.__name__, method.__name__)
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
    
    @meth_dbc
    def test_meth(self, a, b, *args, **kwargs):
        """
        Method test_meth to be tested in terms of 'Design by Contract'
        decorator.
        """
        print 'Inside test method'
        return '{} != {}'.format(a, b)
    
    @property
    @meth_dbc
    def Name(self):
        """
        Getter property Name. Returns class name.
        """
        return self.__class__.__name__
    
    @Name.setter
    @meth_dbc
    def Name(self, strName):
        """
        Setter property Name. Does nothing.
        """
        pass

#test area

objTest = Test_Class()
print objTest.test_meth(1, 2, "test")
print objTest.test_meth.__name__
print objTest.test_meth.__doc__
print
print objTest.Name
print
objTest.Name = 'What ever'
