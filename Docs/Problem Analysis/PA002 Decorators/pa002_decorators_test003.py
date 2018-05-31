#!/usr/bin/python

import functools
import inspect

def func_dbc(input_func):
    """
    Implements 'Design by Contract' for functions via a decorator.
    """
    @functools.wraps(input_func)
    def decorated(*args, **kwargs):
        """
        Decorator 'func_dbc' closure. Implements input and output data
        check for the function to be decorated.
        """
        print 'Design by Contract:'
        print 'Input check for {}'.format(input_func.__name__)
        print input_func.__doc__
        print inspect.getargspec(input_func)
        print inspect.getcallargs(input_func, *args, **kwargs)
        gResult = input_func(*args, **kwargs)
        print 'Output type: {}'.format(type(gResult))
        return gResult
    return decorated

@func_dbc
def test_func(a, b, c= 'foo', **kwargs):
    """
    Function test_func to be tested in terms of 'Design by Contract'
    decorator.
    """
    print 'Inside test function'
    return '{} = {} + {}'.format(c, a, b)

#test area

print test_func(1, 2)
print test_func(1, 2, "test")
print test_func(1, 2, c = "test")
print test_func.__name__
print test_func.__doc__
