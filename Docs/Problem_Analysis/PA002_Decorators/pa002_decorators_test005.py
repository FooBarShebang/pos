#!/usr/bin/python

import functools
import inspect

GLOBAL_DBC = {
    'test_func' : {
        'Some_key' : True
        },
    }

def func_dbc(dictLookUp):
    """
    Implements 'Design by Contract' for functions via a parametric
    decorator.
    """
    def wrapper(input_func):
        """
        Closure of 'func_dbc' decorator.
        """
        @functools.wraps(input_func)
        def decorated(*args, **kwargs):
            """
            Closure of 'wrapper' closure of 'func_dbc' decorator.
            Implements input and output data check for the function to
            be decorated using external look-up dictionary.
            """
            if input_func.__name__ in dictLookUp.keys():
                print 'Design by Contract:'
                print 'Input check for {}'.format(input_func.__name__)
                print input_func.__doc__
                print inspect.getargspec(input_func)
                print inspect.getcallargs(input_func, *args, **kwargs)
            else:
                print '{} is not under Design by Contract'.format(
                                                    input_func.__name__)
            gResult = input_func(*args, **kwargs)
            if input_func.__name__ in dictLookUp.keys():
                print 'Output type: {}'.format(type(gResult))
            return gResult
        return decorated
    return wrapper

@func_dbc(GLOBAL_DBC)
def test_func(a, b, *args, **kwargs):
    """
    Function test_func to be tested in terms of 'Design by Contract'
    decorator.
    """
    print 'Inside test function'
    return '{} != {}'.format(a, b)

@func_dbc(GLOBAL_DBC)
def test_func2(a, b, *args, **kwargs):
    """
    Function test_func to be tested in terms of 'Design by Contract'
    decorator.
    """
    print 'Inside test function'
    return '{} != {}'.format(a, b)

#test area

print test_func(1, 2, "test")
print test_func.__name__
print test_func.__doc__
print
print test_func2(1, 2, "test")
print test_func2.__name__
print test_func2.__doc__
