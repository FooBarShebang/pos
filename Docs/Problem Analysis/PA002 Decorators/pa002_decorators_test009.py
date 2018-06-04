#!/usr/bin/python

import functools
import inspect

GLOBAL_DBC = {
    'test_function' : {
        'Some_key' : True
        },
    }

#design by contract implementation

def function_dbc(dictLookUp):
    """
    Implements 'Design by Contract' for functions via a parametric
    decorator.
    """
    def wrapper(input_func):
        """
        Closure of 'function_dbc' decorator.
        """
        @functools.wraps(input_func)
        def decorated(*args, **kwargs):
            """
            Closure of 'wrapper' closure of 'function_dbc' decorator.
            Implements input and output data check for the function to
            be decorated using external look-up dictionary.
            """
            if input_func.__name__ in dictLookUp.keys():
                print 'Design by Contract:'
                print 'Input check for {} function'.format(input_func.__name__)
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

def method_dbc(method):
    """
    Implements 'Design by Contract' for instance methods via decorator.
    """
    @functools.wraps(method)
    def decorated(instance, *args, **kwargs):
        """
        Decorator 'method_dbc' closure. Implements input and output data
        check for the instance method to be decorated.
        """
        print 'Design by Contract:'
        print 'Input check for {}.{} instance method'.format(
                        instance.__class__.__name__, method.__name__)
        print inspect.getargspec(method)
        print inspect.getcallargs(method, instance, *args, **kwargs)
        gResult = method(instance, *args, **kwargs)
        print 'Output type: {}'.format(type(gResult))
        return gResult
    return decorated

def property_dbc(method):
    """
    Implements 'Design by Contract' for property getter via decorator.
    """
    @functools.wraps(method)
    def decorated(instance, *args, **kwargs):
        """
        Decorator 'property_dbc' closure. Implements output data check for the
        property getter to be decorated.
        """
        gResult = method(instance, *args, **kwargs)
        print 'Design by Contract:'
        print 'Output check for {}.{} getter property'.format(
                        instance.__class__.__name__, method.__name__)
        print 'Output type: {}'.format(type(gResult))
        return gResult
    return property(decorated)

def property_setter_dbc(method):
    """
    Implements 'Design by Contract' for property setter via decorator.
    """
    @functools.wraps(method)
    def decorated(instance, *args, **kwargs):
        """
        Decorator 'property_dbc' closure. Implements input data check for the
        property setter to be decorated.
        """
        print 'Design by Contract:'
        print 'Input check for {}.{} setter property'.format(
                        instance.__class__.__name__, method.__name__)
        print inspect.getargspec(method)
        print inspect.getcallargs(method, instance, *args, **kwargs)
        method(instance, *args, **kwargs)
    return decorated

def classmethod_dbc(method):
    """
    Implements 'Design by Contract' for class methods via decorator.
    """
    @functools.wraps(method)
    def decorated(instance, *args, **kwargs):
        """
        Decorator 'classmethod_dbc' closure. Implements input and output
        data check for the class method to be decorated.
        """
        print 'Design by Contract:'
        print 'Input check for {}.{} class method'.format(
                                    instance.__name__, method.__name__)
        print inspect.getargspec(method)
        print inspect.getcallargs(method, instance, *args, **kwargs)
        gResult = method(instance, *args, **kwargs)
        print 'Output type: {}'.format(type(gResult))
        return gResult
    return classmethod(decorated)

def staticmethod_dbc(strClass, dictLookup):
    """
    Implements 'Design by Contract' for static methods via a parametric
    decorator.
    """
    def wrapper(input_func):
        """
        Closure of 'staticmethod_dbc' decorator.
        """
        @functools.wraps(input_func)
        def decorated(*args, **kwargs):
            """
            Closure of 'wrapper' closure of 'staticmethod_dbc' decorator.
            Implements input and output data check for the static method
            to be decorated.
            """
            print 'Design by Contract:'
            print 'Input check for {}.{} static method'.format(strClass,
                                                    input_func.__name__)
            print inspect.getargspec(input_func)
            print inspect.getcallargs(input_func, *args, **kwargs)
            gResult = input_func(*args, **kwargs)
            print 'Output type: {}'.format(type(gResult))
            return gResult
        return staticmethod(decorated)
    return wrapper

#user defined

@function_dbc(GLOBAL_DBC)
def test_function(a, b, *args, **kwargs):
    """
    Function test_function to be tested in terms of 'Design by Contract'
    decorator.
    """
    print 'Inside test_function'
    return '{} != {}'.format(a, b)

@function_dbc(GLOBAL_DBC)
def test_function2(a, b, *args, **kwargs):
    """
    Function test_function2 to be tested in terms of 'Design by Contract'
    decorator.
    """
    print 'Inside test_function2'
    return '{} != {}'.format(a, b)

class Test_Class(object):
    """
    Class to be tested in terms of 'Design by Contract' decorator.
    """
    
    _Design_Contract = {"test_staticmethod" : None,
                        "test_classmethod" : None}
    
    def __init__(self, strName):
        """
        """
        self.name = strName
    
    @method_dbc
    def test_method(self, a, b, *args, **kwargs):
        """
        Method test_method to be tested in terms of 'Design by Contract'
        decorator.
        """
        print 'Inside test method'
        return '{} != {}'.format(a, b)
    
    @property_dbc
    def Name(self):
        """
        Getter property Name. Returns the value of the instance attribute name.
        """
        return self.name
    
    @Name.setter
    @property_setter_dbc
    def Name(self, strName):
        """
        Setter property Name. Sets the value of the instance attribute name.
        """
        self.name = strName
    
    @classmethod_dbc
    def test_classmethod(cls, a, b, *args, **kwargs):
        """
        Class method test_classmethod to be tested in terms of 'Design by
        Contract' decorator.
        """
        print 'Inside test_classmethod method'
        return '{} != {}'.format(a, b)
    
    @staticmethod_dbc('Test_Class', _Design_Contract)
    def test_staticmethod(a, b, *args, **kwargs):
        """
        Static method test_staticmethod to be tested in terms of 'Design by
        Contract' decorator.
        """
        print 'Inside test_staticmethod method'
        return '{} != {}'.format(a, b)

#test area
print test_function(1, 2, "test")
print
print test_function2(1, 2, "test")
print
objTest = Test_Class('Who cares')
print objTest.test_method(1, 2, "test")
print
print objTest.Name
print
objTest.Name = 'What ever'
print
print objTest.Name
print
print Test_Class.test_classmethod(1, 2, "test")
print
print objTest.test_classmethod(1, 2, "test")
print
print Test_Class.test_staticmethod(1, 2, "test")
print
print objTest.test_staticmethod(1, 2, "test")