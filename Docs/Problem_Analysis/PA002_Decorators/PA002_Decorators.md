# PA002 Problem Analysis on Usage of Decorators in the Design by Contract Implementation

## Introduction

The Design by Contract paradigm is one of the ways to enforce consistent communication interface between the objects. Basically, a function / method provides a contract / guarantee that it will behave deterministic, i.e. it will return specified type / range of values with the input (arguments) being also of the specified type / range of values.

For the “classical” static-binding programming languages the function / method signature is such contract at the *compilation time*. What happens with the unexpected input at the *runtime* is up to the language implementation – either ‘strong’ or ‘weak’ type casting or a runtime error. The situation becomes even less predictable in the case of polymorphic and generic programming.

With the *dynamically typed* languages, like Python, it is up to the developer how to treat the unexpected / non-conforming input: do input data sanity checks, make a completely generic, data-type independent code and live with the consequences of potentially unpredictable code behavior, or implement extensive exceptions handling. Thus, Design by Contract implemented in a dynamically typed language is a convenient way to ensure stable and deterministic data processing.

Specifically for Python the Design by Contact paradigm should include 3 major aspects:

* Input data check *before* execution of a function / method – as a measure to exclude erroneous / unpredictable / unexpected data passed into it by *user* (generically)
* Output data check after execution of a function / method – as a *quality of implementation* measure, complementing unit testing and other standard tests
* Both input and output data checks should raise a small set (even a single) of well defined exceptions, ideally, custom / user defined, so the exceptions handling can focus only on those and clearly distinguish between errors due to *bad code* and *rotten input*

Instead, consider a situation, when there is a single function, which can hook into the call chain, find a specific function’s ‘contract’ in some look-up table, check the arguments of the function’s call against the contract, execute the function’s call, and check the returned value against the contract. The easy way to do so is to pass the function’s reference and its arguments into another function explicitly, which does the before and after call checks. So, instead of calling function *f(x)* directly one should do a call to another function *h(f, x)*, which will call *f(x)* inside itself:

*f(x)* &#x21D2; *h(f, x)*

This is, basically, the core of the Python implementation of the Design by Contract discussed in this document. The trick is to how avoid the explicit call as above, so the user / programmer can keep on using *f(x)* in the code, which will be automatically translated into *h(f, x)* during execution. And the answer is simple – _**decorators**_. In spite of seemingly ‘magical’ behavior, the principle of their work is quite simple.

The first important principle is partial application as a specific case of *currying* concept, which is applicable when a single call of a function of multiple arguments can be transformed into a chain of calls of functions of lower arity (with the true currying – only unary functions calls):

&#x03BB; *fx* &#x2192; &#x03BB; *f* &#x2218; &#x03BB; *x*

Thus, in our case the function *h* must ‘generate’ dynamically some callable object based on the received *f* argument, which should accept the same arguments as *f* does (*x* in this example), and the arguments following *f* should be passed into that callable. So, the transformation is:

*f(x)* &#x21D2; *h(f, x)* &#x2192; *g(f)(x)*

Then, for each specific *f* the callable object *g(f*) can be ‘fixed’ and referenced as, for instance *F* (which process is the *partial application*), so the transformation chain is extended as:

*f(x)* &#x21D2; *h(f, x)* &#x2192; *g(f)(x)* &#x2192; *F(x)*

The final trick is to reassign the **reference** *f* from the original callable (function) to the new callable referenced as *F*. When one makes a call to *f(x)* function, the *F(x)* is called instead, therefore - *h(f, x)*.

Note, that the *partial application* is implemented in the Standard Python Library, see **functools.partial**(), which is a great tool in the case of simply reduction of the arity of a function by fixing its first argument (usually, non-callable type) at a specific value. For our purposes, however, a more direct and explicit approach using *closures* is better suited. Basically, it is a function defined in a local scope of another function.

The outer function accepts a reference to a callable object as its argument. Inside the outer function the other, inner function is defined (the closure), which should have the same parameters as the function to be decorated. Since the reference to a function to be decorated is passed as an argument of the outer function, for the inner function (closure) this reference is in ‘global’ scope in context of the outer function, so it is accessible without a need to pass it as an argument within the inner function. Thus, the inner function can call that external function to be decorated and pass into it the values, that it itself has received as arguments. The outer function, in turn, returns not the result of the execution of its closure, but the reference to the closure.

In a quasi-code terms all said above looks like.

```python
def func_real(x):
	# do something
	return something

def decorator(func):
	def closure(x):
		#do some checks
		result = func(x)
		#do some checks
		return result
	return closure

func_real = decorator(func_real)
```

The whole Python @**decorator** syntax is nothing more, that the last line of the quasi-code above, so the same can be written in a neat and less ambiguous for non-professionals way as:

```python
def decorator(func):
	def closure(x):
		#do some checks
		result = func(x)
		#do some checks
		return result
	return closure

@decorator
def func_real(x):
	# do something
	return something
```

The bottom line is that when further in the code the call to *func_real(x)* is stated, another function is called, namely *closure(x)*.

The rest of the document is not as much problem analysis research as simply illustration of how decorators can be employed in implementation of Design by Contract in different situations: functions, instance and class methods.

## Results

The examples given are mostly by these sources: <a id="bref1">[<sup>1</sup>](#aref1)</a>, [<sup>2</sup>](#aref2) and [<sup>3</sup>](#aref3).

So, the first example demonstrates the discussed above approach.

[pa002_decorators_test001.py](./pa002_decorators_test001.py)

```python
def func_dbc(input_func):
    """
    Implements 'Design by Contract' for functions via a decorator.
    """
    def decorated(*args, **kwargs):
        """
        Decorator 'func_dbc' closure. Implements input and output data
        check for the function to be decorated.
        """
        print 'Design by Contract:'
        print 'Input check for {}'.format(input_func.__name__)
        print input_func.__doc__
        print 'Number of positional arguments: {}'.format(len(args))
        print 'Names of keyword arguments: {}'.format(
                                                ' '.join(kwargs.keys()))
        gResult = input_func(*args, **kwargs)
        print 'Output type: {}'.format(type(gResult))
        return gResult
    return decorated

@func_dbc
def test_func(a, b, c='foo'):
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
```

**output**

```bash
Design by Contract:
Input check for test_func

    Function test_func to be tested in terms of 'Design by Contract'
    decorator.
    
Number of positional arguments: 2
Names of keyword arguments: 
Inside test function
Output type: <type 'str'>
foo = 1 + 2
Design by Contract:
Input check for test_func

    Function test_func to be tested in terms of 'Design by Contract'
    decorator.
    
Number of positional arguments: 3
Names of keyword arguments: 
Inside test function
Output type: <type 'str'>
test = 1 + 2
Design by Contract:
Input check for test_func

    Function test_func to be tested in terms of 'Design by Contract'
    decorator.
    
Number of positional arguments: 2
Names of keyword arguments: c
Inside test function
Output type: <type 'str'>
test = 1 + 2
decorated

        Decorator 'func_dbc' closure. Implements input and output data
        check for the function to be decorated.
```

As can be seen, the actual body of the decorated function is indeed executed, however, the intended code before and after it is executed as well. It is also clear, that the token *test_func* references not the defined function’s body but a specific instance of the closure *decorated*. Therefore the name and doc-string replacement. The second problem is that the passed arguments (positional and keyword ones) are treated as those defined by the signature of the closure, not of the decorated function itself.

The first problem has a simple solution. Inside the outer function *func_dbc* the values of the **\_\_name\_\_** and **\_\_doc\_\_** attributes of the closure should be replaced by those of the passed function argument. The standard library _**functools**_ has a function **wraps**(), which does exactly this task, therefore the direct re-assignment can be avoided, which makes the code a bit neater.

[pa002_decorators_test002.py](./pa002_decorators_test002.py)

```python
import functools

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
        print 'Number of positional arguments: {}'.format(len(args))
        print 'Names of keyword arguments: {}'.format(
                                                ' '.join(kwargs.keys()))
        gResult = input_func(*args, **kwargs)
        print 'Output type: {}'.format(type(gResult))
        return gResult
    return decorated

@func_dbc
def test_func(a, b, c='foo'):
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
```

**output**

```bash
Design by Contract:
Input check for test_func

    Function test_func to be tested in terms of 'Design by Contract'
    decorator.
    
Number of positional arguments: 2
Names of keyword arguments: 
Inside test function
Output type: <type 'str'>
foo = 1 + 2
Design by Contract:
Input check for test_func

    Function test_func to be tested in terms of 'Design by Contract'
    decorator.
    
Number of positional arguments: 3
Names of keyword arguments: 
Inside test function
Output type: <type 'str'>
test = 1 + 2
Design by Contract:
Input check for test_func

    Function test_func to be tested in terms of 'Design by Contract'
    decorator.
    
Number of positional arguments: 2
Names of keyword arguments: c
Inside test function
Output type: <type 'str'>
test = 1 + 2
test_func

    Function test_func to be tested in terms of 'Design by Contract'
    decorator.
```

The solution to the second problem is the standard library _**inspect**_, which has two functions: **getargspecs**() and **getcallargs**(). The first one shows the function’s signature (as it is defined), and the second function shows how the passed arguments are expanded in the context of the function’s signature.

[pa002_decorators_test003.py](./pa002_decorators_test003.py)

```python
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
```

**output**

```bash
Design by Contract:
Input check for test_func

    Function test_func to be tested in terms of 'Design by Contract'
    decorator.
    
ArgSpec(args=['a', 'b', 'c'], varargs=None, keywords='kwargs', defaults=('foo',))
{'a': 1, 'c': 'foo', 'b': 2, 'kwargs': {}}
Inside test function
Output type: <type 'str'>
foo = 1 + 2
Design by Contract:
Input check for test_func

    Function test_func to be tested in terms of 'Design by Contract'
    decorator.
    
ArgSpec(args=['a', 'b', 'c'], varargs=None, keywords='kwargs', defaults=('foo',))
{'a': 1, 'c': 'test', 'b': 2, 'kwargs': {}}
Inside test function
Output type: <type 'str'>
test = 1 + 2
Design by Contract:
Input check for test_func

    Function test_func to be tested in terms of 'Design by Contract'
    decorator.
    
ArgSpec(args=['a', 'b', 'c'], varargs=None, keywords='kwargs', defaults=('foo',))
{'a': 1, 'c': 'test', 'b': 2, 'kwargs': {}}
Inside test function
Output type: <type 'str'>
test = 1 + 2
test_func

    Function test_func to be tested in terms of 'Design by Contract'
    decorator.
```

In the next example the function to be decorated has different signature to illustrate the point a bit more thoroughly.

[pa002_decorators_test004.py](./pa002_decorators_test004.py)

```python
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
def test_func(a, b, *args, **kwargs):
    """
    Function test_func to be tested in terms of 'Design by Contract'
    decorator.
    """
    print 'Inside test function'
    return '{} != {}'.format(a, b)

#test area

print test_func(1, 2)
print test_func(1, 2, "test")
print test_func(1, 2, c = "test")
print test_func.__name__
print test_func.__doc__
```

**output**

```bash
Design by Contract:
Input check for test_func

    Function test_func to be tested in terms of 'Design by Contract'
    decorator.
    
ArgSpec(args=['a', 'b'], varargs='args', keywords='kwargs', defaults=None)
{'a': 1, 'b': 2, 'args': (), 'kwargs': {}}
Inside test function
Output type: <type 'str'>
1 != 2
Design by Contract:
Input check for test_func

    Function test_func to be tested in terms of 'Design by Contract'
    decorator.
    
ArgSpec(args=['a', 'b'], varargs='args', keywords='kwargs', defaults=None)
{'a': 1, 'b': 2, 'args': ('test',), 'kwargs': {}}
Inside test function
Output type: <type 'str'>
1 != 2
Design by Contract:
Input check for test_func

    Function test_func to be tested in terms of 'Design by Contract'
    decorator.
    
ArgSpec(args=['a', 'b'], varargs='args', keywords='kwargs', defaults=None)
{'a': 1, 'b': 2, 'args': (), 'kwargs': {'c': 'test'}}
Inside test function
Output type: <type 'str'>
1 != 2
test_func

    Function test_func to be tested in terms of 'Design by Contract'
    decorator.
```

As can be seen, with the help of the functions **inspect.getargspec**s() and **inspect.getcallargs**() one can check what kind of data is passed as the argument(s) into a decorated function and how they relate to the intended signature of that function using some sort of the external look-up table. Ideally, such a look-up table should be defined per module / namespace, so we need to pass a reference to it into the decorator. In other words, we need a parametric decorator. Luckily, the solution is simple – just use a closure inside a closure. The outermost function to be the parametric decorator should be defined with a parameter, so a reference to a look-up table can be passed as an argument of the decorator. And the actual decorator function from the previous examples becomes its closure.

[pa002_decorators_test005.py](./pa002_decorators_test005.py)

```python
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
```

**output**

```bash
Design by Contract:
Input check for test_func

    Function test_func to be tested in terms of 'Design by Contract'
    decorator.
    
ArgSpec(args=['a', 'b'], varargs='args', keywords='kwargs', defaults=None)
{'a': 1, 'b': 2, 'args': ('test',), 'kwargs': {}}
Inside test function
Output type: <type 'str'>
1 != 2
test_func

    Function test_func to be tested in terms of 'Design by Contract'
    decorator.
    

test_func2 is not under Design by Contract
Inside test function
1 != 2
test_func2

    Function test_func to be tested in terms of 'Design by Contract'
    decorator.
```

Instance methods of a class in general, and the properties as their special case, are, in fact, functions bound to a specific namespace, that of the class, and the instances itself is always passed as the first argument. Therefore, the class of the instance can be always resolved, thus the Design by Contract look-up table for a class’ instance methods can be defined inside the class (in its own namespace), and there is no need to pass a reference to that look-up table explicitly.

[pa002_decorators_test006.py](./pa002_decorators_test006.py)

```python
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
```

**output**

```bash
Design by Contract:
Input check for Test_Class.test_meth

        Method test_meth to be tested in terms of 'Design by Contract'
        decorator.
        
ArgSpec(args=['self', 'a', 'b'], varargs='args', keywords='kwargs', defaults=None)
{'a': 1, 'self': <__main__.Test_Class object at 0x7f4a48c5bed0>, 'b': 2, 'args': ('test',), 'kwargs': {}}
Inside test method
Output type: <type 'str'>
1 != 2
test_meth

        Method test_meth to be tested in terms of 'Design by Contract'
        decorator.
        

Design by Contract:
Input check for Test_Class.Name

        Getter property Name. Returns class name.
        
ArgSpec(args=['self'], varargs=None, keywords=None, defaults=None)
{'self': <__main__.Test_Class object at 0x7f4a48c5bed0>}
Output type: <type 'str'>
Test_Class

Design by Contract:
Input check for Test_Class.Name

        Setter property Name. Does nothing.
        
ArgSpec(args=['self', 'strName'], varargs=None, keywords=None, defaults=None)
{'self': <__main__.Test_Class object at 0x7f4a48c5bed0>, 'strName': 'What ever'}
Output type: <type 'NoneType'>
```

Take notes of two things: 1) the order of the application of the decorators – the property decorator must be the last one, i.e. on the top; 2) **Name** getter and **Name** setter properties are two different methods with clearly different functionality and doc-string, but they share the ‘name’ - it is a point for further analysis on how to avoid confusion which this effect will cause on the Design by Contract using functions / methods look-up table approach.

Clearly, the class methods are different from the instance methods that not an instance but the class is passed as their first argument. Thus, a separate decorator should be defined, but its functionality is virtually identical except for the class resolution from an instance.

[pa002_decorators_test007.py](./pa002_decorators_test007.py)

```python
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
        data check for the instance method to be decorated.
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
```

**output**

```bash
Design by Contract:
Input check for Test_Class.test_meth

        Class method test_meth to be tested in terms of 'Design by
        Contract' decorator.
        
ArgSpec(args=['cls', 'a', 'b'], varargs='args', keywords='kwargs', defaults=None)
{'a': 1, 'kwargs': {}, 'b': 2, 'args': ('test',), 'cls': <class '__main__.Test_Class'>}
Inside test method
Output type: <type 'str'>
1 != 2
test_meth

        Class method test_meth to be tested in terms of 'Design by
        Contract' decorator.
        

Design by Contract:
Input check for Test_Class.test_meth

        Class method test_meth to be tested in terms of 'Design by
        Contract' decorator.
        
ArgSpec(args=['cls', 'a', 'b'], varargs='args', keywords='kwargs', defaults=None)
{'a': 1, 'kwargs': {}, 'b': 2, 'args': ('test',), 'cls': <class '__main__.Test_Class'>}
Inside test method
Output type: <type 'str'>
1 != 2
test_meth

        Class method test_meth to be tested in terms of 'Design by
        Contract' decorator.
```

Finally, the static methods are simply references to the external, unbound functions placed into the class’ namespace (references, not the functions themselves). Therefore, the static methods do not have direct access to the class’ namespace, i.e. its class attributes. One of the solutions is to pass a reference to a look-up table explicitly, same as with an ordinary function, although the look-up table can be defined locally in the class’ namespace.

[pa002_decorators_test008.py](./pa002_decorators_test008.py)

```python
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
```

**output**

```bash
Design by Contract:
Input check for Test_Class.test_meth

        Static method test_meth to be tested in terms of 'Design by
        Contract' decorator.
        
ArgSpec(args=['a', 'b'], varargs='args', keywords='kwargs', defaults=None)
{'a': 1, 'b': 2, 'args': ('test',), 'kwargs': {}}
Inside test method
Output type: <type 'str'>
1 != 2
test_meth

        Static method test_meth to be tested in terms of 'Design by
        Contract' decorator.
        

Design by Contract:
Input check for Test_Class.test_meth

        Static method test_meth to be tested in terms of 'Design by
        Contract' decorator.
        
ArgSpec(args=['a', 'b'], varargs='args', keywords='kwargs', defaults=None)
{'a': 1, 'b': 2, 'args': ('test',), 'kwargs': {}}
Inside test method
Output type: <type 'str'>
1 != 2
test_meth

        Static method test_meth to be tested in terms of 'Design by
        Contract' decorator.
```
Concerning the issue with the properties shown in the **pa002_decorators_test006**, the obvious solution could be to use different names of the getter and setter method, so one can define different contracts for the both methods. This approach can be taken only if the getter and setter methods are assigned to a property using the built-in function _**property**_() directly. But by using the @**property** decorator approach, the getter and setter methods must have exactly the same names.

The solution is to use two different functions as the decorators for the getter and setter methods. The decorator for the getter method should only check the output, whereas the decorator for the setter method should check the input; optionally it can also check that the setter method returns **None** value.

The getter property decorator must take a method as its argument and return an object of _**property**_ type. Basically, the closure of the decorator must be passed as the argument into the built-in function _**property**_(), and the result is returned. With this approach there is no need to chain the decorators, so the code can be like below:

```python
def propery_dbc(method):
    def closure(*args):
        #call method here
        ...
    return property(closure)
...
class SomeClass(object):
    @property_dbc
    def some_property(self):
        #some code here
    ...
```

**Note**: exactly the same approach can be taken in the case of the decorators for the static and class methods (but converting the closure into the **staticmethod**() and **classmethod**() objects respectively), thus the decorators chaining can be eliminated.

The setter property decorator requires another approach. The decorator protocol specifies that the function used as a decorator must return a callable object. The @**property** decorator, in a sense, breaks this pattern. A property object is not callable, its class doesn’t have **\_\_call\_\_**() method. Instead, it has **\_\_get\_\_**() and **\_\_set\_\_**() descriptors, which, in turn, call the bound functions referenced by the **fget** and **fset** attributes. A property is never used explicitly as a callable, rather as a data attribute, as in an assignment to it or as in its value retrieval. In such cases **setattr**() and **getattr**() calls results in the execution of the above mentioned decorators, thus there is no need for the presence of the **\_\_call\_\_**() method on the object. Note that the instantiation of a class is implemented as a method of its meta-class, thus a callable object, therefore the @**property** decorator, which creates a getter property, in the strict sense, complies with the protocol. The situation with the decorator for the setter property creation is a bit more complicated. Consider the standard syntax:

```python
class SomeClass(object):
    @property
    def some_property(self):
        ...
    @some_property.setter
    def some_property(self, value)
        ...
```

The first decorator results in **some_property** referencing not a bound function (instance method) but  an instance of the **property** class, which calls the code of the original method within its **\_\_get\_\_**() decorator. The second decorator makes the **some_property** to reference an object returned by the **setter**() method of the object the same **some_property** has referenced before that!

The simple minded approach to use the setter property decorator to simply set the **fset** attribute of an existing **property** instance and to return that instance, obviously fails, because an instance of the **property** class is not a callable object.

The solution is to return not an existing property instance, but the result of the call of the built_in function **property**() with the now anonymous method referenced by the **fget** attribute of the already existing property instance and the method to be decorated as the **fget** and **fset** arguments. In short, a new instance of the property class will be created.

But there is a catch. In order to access an attribute of the original getter only property it must be created before the corresponding setter property. It can assured, for instance, using the property instead of the actual attribute it interfaces in the initialization method **\_\_init\_\_**(). This approach, however, is not fool proof.

Alternatively, one can make own implementation / simulation of the built-in **property** class (see the official CPython documentation on the decorators HOWTO), but the easiest and the most reliable way is to simply decorate the “setter property to be” method before turning it into the setter property, like is shown below:

```python
def propery_dbc(method):
    def closure(*args):
        #call method here
        ...
    return property(closure)

def property_settter_dbc(method):
    def closure(*args):
        #call method here
        ...
    return closure
...
class SomeClass(object):
    @property_dbc
    def some_property(self):
        #some code here
    
    @some_propety.setter
    @property_setter_dbc
    def some_property(self, value):
        #some code here
    ...
```

The complete example illustrating the difference in the Design by Contract like decorators for the normal functions, getter and setter properties, instance, class and static methods is given below.

[pa002_decorators_test009.py](./pa002_decorators_test009.py)

```python
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
```

**output**

```bash
Design by Contract:
Input check for test_function function
ArgSpec(args=['a', 'b'], varargs='args', keywords='kwargs', defaults=None)
{'a': 1, 'b': 2, 'args': ('test',), 'kwargs': {}}
Inside test_function
Output type: <type 'str'>
1 != 2

test_function2 is not under Design by Contract
Inside test_function2
1 != 2

Design by Contract:
Input check for Test_Class.test_method instance method
ArgSpec(args=['self', 'a', 'b'], varargs='args', keywords='kwargs', defaults=None)
{'a': 1, 'self': <__main__.Test_Class object at 0x00000000024209B0>, 'b': 2, 'args': ('test',), 'kwargs': {}}
Inside test method
Output type: <type 'str'>
1 != 2

Design by Contract:
Output check for Test_Class.Name getter property
Output type: <type 'str'>
Who cares

Design by Contract:
Input check for Test_Class.Name setter property
ArgSpec(args=['self', 'strName'], varargs=None, keywords=None, defaults=None)
{'self': <__main__.Test_Class object at 0x00000000024209B0>, 'strName': 'What ever'}

Design by Contract:
Output check for Test_Class.Name getter property
Output type: <type 'str'>
What ever

Design by Contract:
Input check for Test_Class.test_classmethod class method
ArgSpec(args=['cls', 'a', 'b'], varargs='args', keywords='kwargs', defaults=None)
{'a': 1, 'kwargs': {}, 'b': 2, 'args': ('test',), 'cls': <class '__main__.Test_Class'>}
Inside test_classmethod method
Output type: <type 'str'>
1 != 2

Design by Contract:
Input check for Test_Class.test_classmethod class method
ArgSpec(args=['cls', 'a', 'b'], varargs='args', keywords='kwargs', defaults=None)
{'a': 1, 'kwargs': {}, 'b': 2, 'args': ('test',), 'cls': <class '__main__.Test_Class'>}
Inside test_classmethod method
Output type: <type 'str'>
1 != 2

Design by Contract:
Input check for Test_Class.test_staticmethod static method
ArgSpec(args=['a', 'b'], varargs='args', keywords='kwargs', defaults=None)
{'a': 1, 'b': 2, 'args': ('test',), 'kwargs': {}}
Inside test_staticmethod method
Output type: <type 'str'>
1 != 2

Design by Contract:
Input check for Test_Class.test_staticmethod static method
ArgSpec(args=['a', 'b'], varargs='args', keywords='kwargs', defaults=None)
{'a': 1, 'b': 2, 'args': ('test',), 'kwargs': {}}
Inside test_staticmethod method
Output type: <type 'str'>
1 != 2
```

## Conclusion

The decorators provide powerful, flexible and reliable means for the implementation of the Design by Contract paradigm. The proposed implementation scheme is:

* The function / method contract is defined outside it but in the same namespace, i.e. in the same module for the normal functions and within the class’ definition for the properties, instance, class and static methods, in the form of a look-up object, e.g. a dictionary or some user-defined class’ instance
* A function / method is taken under the Design by Contract control by decorating it with the corresponding decorator function using @ syntax
* The decorator functions return their closures as callable objects to ‘replace’ the original functions / methods – the original functions / methods become anonymous, whereas the variables / attributes that used to reference those callables now, after the decoration reference the closures returned by the decorator functions
* The closures of the decorator functions use external Design by Contract look-up objects to find the rules for the specific function / method by their names, perform the input data checks on the received arguments, call the decorated function / method, perform the output data check on the result of this call, and, if the both checks are passed, return that value
* The closures should raise specific exception(s) if either the external Design by Contract look-up object is not found, or it doesn’t contain the contract for this specific function / method – this is a case of the programming fault
* The closures should raise other specific exception(s) if either the input or output data check has failed
* Own decorator function are to be defined for the ‘fundamental’ callable types: normal function, instance method, class method, static method, getter property and setter property
* Class and static method’s decorators as well as the getter property decorators may implement ‘short-cut’ for the decorators chaining elimination by already returning the built-in functions **classmethod**(), **staticmethod**() and **property**() respectively applied to their closures
* The decorator for the setter properties should return normal callable closure, and the corresponding decorator can be chained (as the first / bottom decorator) with the standard @**some_property.setter** decorator.; in this case the getter and setter Design by Contract property decorators can be applied independently (either one or both)
* In the case of the getter and setter properties, instance and class methods decorators the reference to an instance of a class (or to the class itself in the last case) is passed explicitly as the first argument to the closure, thus the Design by Contract look-up object defined within that class can be accessed directly
* In the case of the normal function and static method decorators the reference to the look-up object must be passed, thus these decorators must be parametric; which can be implemented using nested (2-levels) closures
* The standard library _**functools**_ provides convenient function **wraps**(), which can be used as a decorator for the closure itself in order to preserve the original name and doc-string of the decorated function /method
* The standard library _**inspect**_ provides two functions – **getargspecs**() and **getcallargs**() - which can be used for the analysis of the arguments passed into the decorated function / method

## References

<a id="aref1">[1]</a> https://www.thecodeship.com/patterns/guide-to-python-function-decorators/    [&#x2B0F;](#bref1)

<a id="aref2">[2]</a> https://www.codementor.io/sheena/advanced-use-python-decorators-class-function-du107nxsv

<a id="aref3">[3]</a> https://blog.apcelent.com/python-decorator-tutorial-with-example.html