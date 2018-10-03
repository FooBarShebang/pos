# PA004 Problem Analysis on the Exceptions Call Chain Traceback

## Introduction

Standard Python Library provides multiple tools to trace the call chain that has led to an exception <a id="bref1">[<sup>^1, ^2, ^3</sup>](#aref1)</a>. The goal of this analysis is to define a method based on these tools, which can be used for the implementation of the required functionality, as it is listed below.

* A custom exception should behave exactly as its parent class, except for possibly different signature of its initialization method if not intercepted (on the top level of the Python interpreter loop)
* If intercepted, a custom exception must provide methods or properties for the analysis of the call chain
  - a list of fully qualified (module and function name or module, class and method name) names of the functions / methods call chain, which ended in this exception being raised
  - a nicely formatted single string representation of the corresponding frames, each including the fully qualified name of the function / method, path to the corresponding module’s file, code surrounding the corresponding call and the position of the call within it
* There should be an ability to hide a specified amount of the deepest level frames, for instance, in order to ‘hide’ some implementation details, which can only hinder the analysis of the problem. For example, several methods / functions can rely on a specific helper method / function, which does some mundane calculations or checks. In such situation it is much more important, that a specific outer / interface function or method’s call resulted in an exception rather than that the exception is raised in the helper function / method
* There should be an ability to replace the call traceback of an exception when needed. For instance, an exception can be caught in the handler and when re-raised or another, more generic or more specific exception is raised instead of it. It is desired that the traceback must show the call chain of the original exception
* The implementation should be compatible with the design proposed within [PA003](../PA003_Virtual_Inheritance_Exceptions/PA003_Virtual_Inheritance_Exceptions.md) analysis, i.e. it can be made into a mix-in class

## Method and Results

The first example demonstrates the basics of the traceback information retrieval using **sys.exec_info**(), **traceback.extract_tb**() and **traceback.extract_stack**() functions <a id="bref2">[<sup>^1, ^2</sup>](#aref2)</a>.

[pa004_traceback_test001.py](./pa004_traceback_test001.py)

```python
import sys
import traceback

class CustomError(StandardError):
    
    def printTraceback(self):
        print self.message
        print self.args
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print exc_type, exc_value
        print repr(traceback.extract_tb(exc_traceback))
        print repr(traceback.extract_stack())

def inner():
    raise CustomError('testing')

def middle():
    inner()

def outer():
    middle()

if __name__ == '__main__':
    try:
        outer()
    except CustomError as err:
        err.printTraceback()
```

**output**

```bash
testing
('testing',)
<class '__main__.CustomError'> testing
[('/home/anton/eclipse-workspace/Python2_7/pos/Docs/Problem Analysis/PA004 Traceback/pa004_traceback_test001.py', 27, '<module>', 'outer()'), ('/home/anton/eclipse-workspace/Python2_7/pos/Docs/Problem Analysis/PA004 Traceback/pa004_traceback_test001.py', 23, 'outer', 'middle()'), ('/home/anton/eclipse-workspace/Python2_7/pos/Docs/Problem Analysis/PA004 Traceback/pa004_traceback_test001.py', 20, 'middle', 'inner()'), ('/home/anton/eclipse-workspace/Python2_7/pos/Docs/Problem Analysis/PA004 Traceback/pa004_traceback_test001.py', 17, 'inner', "raise CustomError('testing')")]
[('/home/anton/eclipse-workspace/Python2_7/pos/Docs/Problem Analysis/PA004 Traceback/pa004_traceback_test001.py', 29, '<module>', 'err.printTraceback()'), ('/home/anton/eclipse-workspace/Python2_7/pos/Docs/Problem Analysis/PA004 Traceback/pa004_traceback_test001.py', 14, 'printTraceback', 'print repr(traceback.extract_stack())')]
```

As it should be according to the documentation, the function **traceback.exctract_stack**() returns the call stack representation from the top level to its own call within the method **CustomError.printTraceback**(). The method **traceback.extract_tb**() returns the call stack representation from the frame handling the exception (i.e. executing or having executed an except clause) to the point, where the last exception has been raised. In this particular example the results are identical, because the call that ends in an exception originates in the same frame where the exception is handled, i.e. in the top frame of the module. It may not be the case in all situation, but it is sufficient for the current analysis.

The last method requires a traceback object as its argument, which is obtained as the third element of the tuple returned by the function **sys.exec_info**(). On the other hand, when raised an instance of the exception class is created. Therefore, it is possible to move the call of the function **traceback.exctract_stack**() into the initialization method and remember its result; the **sys** module is not needed in such a case.

[pa004_traceback_test002.py](./pa004_traceback_test002.py)

```python
import traceback

class CustomError(StandardError):
    
    def __init__(self, strMessage):
        self._traceback = traceback.extract_stack()
        super(CustomError, self).__init__(strMessage)
    
    def printTraceback(self):
        print self.message
        print self.args
        print repr(self._traceback)

def inner():
    raise CustomError('testing')

def middle():
    inner()

def outer():
    middle()

if __name__ == '__main__':
    try:
        outer()
    except CustomError as err:
        err.printTraceback()
```

**output**

```bash
testing
('testing',)
[('/home/anton/eclipse-workspace/Python2_7/pos/Docs/Problem Analysis/PA004 Traceback/pa004_traceback_test002.py', 27, '<module>', 'outer()'), ('/home/anton/eclipse-workspace/Python2_7/pos/Docs/Problem Analysis/PA004 Traceback/pa004_traceback_test002.py', 23, 'outer', 'middle()'), ('/home/anton/eclipse-workspace/Python2_7/pos/Docs/Problem Analysis/PA004 Traceback/pa004_traceback_test002.py', 20, 'middle', 'inner()'), ('/home/anton/eclipse-workspace/Python2_7/pos/Docs/Problem Analysis/PA004 Traceback/pa004_traceback_test002.py', 17, 'inner', "raise CustomError('testing')"), ('/home/anton/eclipse-workspace/Python2_7/pos/Docs/Problem Analysis/PA004 Traceback/pa004_traceback_test002.py', 8, '__init__', 'self._traceback = traceback.extract_stack()')]
```

The order in which the traceback and the initialization method of the super class are called is not important, see example below.

[pa004_traceback_test003.py](./pa004_traceback_test003.py)

```python
import traceback

class CustomError(StandardError):
    
    def __init__(self, strMessage):
        super(CustomError, self).__init__(strMessage)
        self._traceback = traceback.extract_stack()
    
    def printTraceback(self):
        print self.message
        print self.args
        print repr(self._traceback)

def inner():
    raise CustomError('testing')

def middle():
    inner()

def outer():
    middle()

if __name__ == '__main__':
    try:
        outer()
    except CustomError as err:
        err.printTraceback()
```

**output**

```bash
testing
('testing',)
[('/home/anton/eclipse-workspace/Python2_7/pos/Docs/Problem Analysis/PA004 Traceback/pa004_traceback_test003.py', 27, '<module>', 'outer()'), ('/home/anton/eclipse-workspace/Python2_7/pos/Docs/Problem Analysis/PA004 Traceback/pa004_traceback_test003.py', 23, 'outer', 'middle()'), ('/home/anton/eclipse-workspace/Python2_7/pos/Docs/Problem Analysis/PA004 Traceback/pa004_traceback_test003.py', 20, 'middle', 'inner()'), ('/home/anton/eclipse-workspace/Python2_7/pos/Docs/Problem Analysis/PA004 Traceback/pa004_traceback_test003.py', 17, 'inner', "raise CustomError('testing')"), ('/home/anton/eclipse-workspace/Python2_7/pos/Docs/Problem Analysis/PA004 Traceback/pa004_traceback_test003.py', 9, '__init__', 'self._traceback = traceback.extract_stack()')]
```

Both the creation and the printing of an exception’s traceback can be moved into another class, from which multiple exception classes can inherit as well as from their exception class parents. Note, that it is not a *pure mix-in* like Java *interface*, since it changes the state of the sub-class. Furthermore, it must precede the parent exception in the MRO. Therefore, it can be artificially labeled as *left mix-in*.

[pa004_traceback_test004.py](./pa004_traceback_test004.py)

```python
import traceback

class ErrorMixin(object):
    
    def __init__(self, *args, **kwargs):
        super(ErrorMixin, self).__init__(*args, **kwargs)
        self._traceback = traceback.extract_stack()
    
    def printTraceback(self):
        print self.message
        print self.args
        print repr(self._traceback)

class CustomError(ErrorMixin, StandardError):
    
    def __init__(self, strMessage):
        super(CustomError, self).__init__(strMessage)


def inner():
    raise CustomError('testing')

def middle():
    inner()

def outer():
    middle()

if __name__ == '__main__':
    try:
        outer()
    except CustomError as err:
        err.printTraceback()
```

**output**

```bash
testing
('testing',)
[('/home/anton/eclipse-workspace/Python2_7/pos/Docs/Problem Analysis/PA004 Traceback/pa004_traceback_test004.py', 33, '<module>', 'outer()'), ('/home/anton/eclipse-workspace/Python2_7/pos/Docs/Problem Analysis/PA004 Traceback/pa004_traceback_test004.py', 29, 'outer', 'middle()'), ('/home/anton/eclipse-workspace/Python2_7/pos/Docs/Problem Analysis/PA004 Traceback/pa004_traceback_test004.py', 26, 'middle', 'inner()'), ('/home/anton/eclipse-workspace/Python2_7/pos/Docs/Problem Analysis/PA004 Traceback/pa004_traceback_test004.py', 23, 'inner', "raise CustomError('testing')"), ('/home/anton/eclipse-workspace/Python2_7/pos/Docs/Problem Analysis/PA004 Traceback/pa004_traceback_test004.py', 19, '__init__', 'super(CustomError, self).__init__(strMessage)'), ('/home/anton/eclipse-workspace/Python2_7/pos/Docs/Problem Analysis/PA004 Traceback/pa004_traceback_test004.py', 9, '__init__', 'self._traceback = traceback.extract_stack()')]
```

There are three apparent problems with this implementation which invalidate all its benefits:

* Such *left mix-ins* are intended to be included into the inheritance tree only once – at the top of the customized classes sub-tree. It is possible inherit them as many times as possible, but this will result in the unnecessary overhead, or the chain of the calls of the super class initialization method may go not the way intended by the programmer. Real, *pure mix-ins* are free from that limitation
* Deep sub-classing will increase the number of ‘helper‘ stack frames at the bottom (initialization methods chain), which should be, technically speaking, from the traceback of the exception
* The entire call stack is extracted, which is not the same, in general, as the traceback between the frame handling the exception and the frame where it has been raised

So, the alternative is to retrieve the last exception traceback from the system in the formating / printing method of the external class. So, this external class becomes a *pure mix-in*. Theoretically, *pure mix-in* class can be inherited before (left) or after (right) the main parent. Since the initialization of the custom exception class relies on the call of the initialization method of its parent exception, in our case it is imperative that the mix-in class is inherited after the main parent.

[pa004_traceback_test005.py](./pa004_traceback_test005.py)

```python
import sys
import traceback

class ErrorMixin(object):
    
    def printTraceback(self):
        print self.message
        print self.args
        _, _, exc_traceback = sys.exc_info()
        print repr(traceback.extract_tb(exc_traceback))

class CustomError(StandardError, ErrorMixin):
    
    def __init__(self, strMessage):
        super(CustomError, self).__init__(strMessage)

def inner():
    raise CustomError('testing')

def middle():
    inner()

def outer():
    middle()

if __name__ == '__main__':
    try:
        outer()
    except CustomError as err:
        err.printTraceback()
```

**output**

```bash
testing
('testing',)
[('/home/anton/eclipse-workspace/Python2_7/pos/Docs/Problem Analysis/PA004 Traceback/pa004_traceback_test005.py', 30, '<module>', 'outer()'), ('/home/anton/eclipse-workspace/Python2_7/pos/Docs/Problem Analysis/PA004 Traceback/pa004_traceback_test005.py', 26, 'outer', 'middle()'), ('/home/anton/eclipse-workspace/Python2_7/pos/Docs/Problem Analysis/PA004 Traceback/pa004_traceback_test005.py', 23, 'middle', 'inner()'), ('/home/anton/eclipse-workspace/Python2_7/pos/Docs/Problem Analysis/PA004 Traceback/pa004_traceback_test005.py', 20, 'inner', "raise CustomError('testing')")]
```

Apparently, the code does what we want. Now, let’s see what happens in the case of the methods not simple functions call.

[pa004_traceback_test006.py](./pa004_traceback_test006.py)

```python
import sys
import traceback

class ErrorMixin(object):
    
    def printTraceback(self):
        print self.message
        print self.args
        _, _, exc_traceback = sys.exc_info()
        print repr(traceback.extract_tb(exc_traceback))

class CustomError(StandardError, ErrorMixin):
    
    def __init__(self, strMessage):
        super(CustomError, self).__init__(strMessage)

class TestClass(object):
    def inner(self):
        raise CustomError('testing')

    def middle(self):
        self.inner()

    def outer(self):
        self.middle()

if __name__ == '__main__':
    try:
        TestObject = TestClass()
        TestObject.outer()
    except CustomError as err:
        err.printTraceback()
```

**output**

```bash
testing
('testing',)
[('/home/anton/eclipse-workspace/Python2_7/pos/Docs/Problem Analysis/PA004 Traceback/pa004_traceback_test006.py', 32, '<module>', 'TestObject.outer()'), ('/home/anton/eclipse-workspace/Python2_7/pos/Docs/Problem Analysis/PA004 Traceback/pa004_traceback_test006.py', 27, 'outer', 'self.middle()'), ('/home/anton/eclipse-workspace/Python2_7/pos/Docs/Problem Analysis/PA004 Traceback/pa004_traceback_test006.py', 24, 'middle', 'self.inner()'), ('/home/anton/eclipse-workspace/Python2_7/pos/Docs/Problem Analysis/PA004 Traceback/pa004_traceback_test006.py', 21, 'inner', "raise CustomError('testing')")]
```

The problem is that from the call stack of view the call of a method of a class is the same as a call of a usual function. Thus, one needs to perform some deeper analysis of the frames of the traceback of the call stack. Unfortunately, there is not much that can be done with the return value of the function **traceback.extract_tb**(), since it simply returns a list of tuples of strings, not the references to the frame objects, as is shown in the next example.

[pa004_traceback_test007.py](./pa004_traceback_test007.py)

```python
import sys
import traceback

class ErrorMixin(object):
    
    def printTraceback(self):
        _, _, exc_traceback = sys.exc_info()
        extracted = traceback.extract_tb(exc_traceback)
        print type(exc_traceback)
        print type(extracted)
        for Item in extracted:
            print type(Item),
        print
        for Item in extracted[0]:
            print type(Item),
        print
        print repr(extracted)

class CustomError(StandardError, ErrorMixin):
    
    def __init__(self, strMessage):
        super(CustomError, self).__init__(strMessage)

class TestClass(object):
    def inner(self):
        raise CustomError('testing')

    def middle(self):
        self.inner()

    def outer(self):
        self.middle()

if __name__ == '__main__':
    try:
        TestObject = TestClass()
        TestObject.outer()
    except CustomError as err:
        err.printTraceback()
```

**output**

```bash
<type 'traceback'>
<type 'list'>
<type 'tuple'> <type 'tuple'> <type 'tuple'> <type 'tuple'>
<type 'str'> <type 'int'> <type 'str'> <type 'str'>
[('/home/anton/eclipse-workspace/Python2_7/pos/Docs/Problem Analysis/PA004 Traceback/pa004_traceback_test007.py', 39, '<module>', 'TestObject.outer()'), ('/home/anton/eclipse-workspace/Python2_7/pos/Docs/Problem Analysis/PA004 Traceback/pa004_traceback_test007.py', 34, 'outer', 'self.middle()'), ('/home/anton/eclipse-workspace/Python2_7/pos/Docs/Problem Analysis/PA004 Traceback/pa004_traceback_test007.py', 31, 'middle', 'self.inner()'), ('/home/anton/eclipse-workspace/Python2_7/pos/Docs/Problem Analysis/PA004 Traceback/pa004_traceback_test007.py', 28, 'inner', "raise CustomError('testing')")]
```

The function **sys.exec_info**(), on the other hand, returns a reference to a real traceback object as its third element, as can be seen in the example above. A **traceback** object holds a reference to a **frame** object (which can be analyzed) and a reference to the next **traceback** object referring to another **frame**, etc. as in a linked list. It is not a difficult task to walk through such a linked list, but there is a ready function in the Standard Library, which does exactly this job – **inspect.trace**() <a id="bref3">[<sup>^3</sup>](#aref3)</a>. It also wraps the **sys.exec_info**() call, thus the interface becomes dead simple.

[pa004_traceback_test008.py](./pa004_traceback_test008.py)

```python
import inspect

class ErrorMixin(object):
    
    def printTraceback(self):
        print inspect.trace()

class CustomError(StandardError, ErrorMixin):
    
    def __init__(self, strMessage):
        super(CustomError, self).__init__(strMessage)

class TestClass(object):
    def inner(self):
        raise CustomError('testing')

    def middle(self):
        self.inner()

    def outer(self):
        self.middle()

if __name__ == '__main__':
    try:
        TestObject = TestClass()
        TestObject.outer()
    except CustomError as err:
        err.printTraceback()
```

**output**

```bash
[(<frame object at 0x7f958c803938>, '/home/anton/eclipse-workspace/Python2_7/pos/Docs/Problem Analysis/PA004 Traceback/pa004_traceback_test008.py', 28, '<module>', ['        TestObject.outer()\n'], 0), (<frame object at 0x7f958b2ea050>, '/home/anton/eclipse-workspace/Python2_7/pos/Docs/Problem Analysis/PA004 Traceback/pa004_traceback_test008.py', 23, 'outer', ['        self.middle()\n'], 0), (<frame object at 0x7f958b2ea200>, '/home/anton/eclipse-workspace/Python2_7/pos/Docs/Problem Analysis/PA004 Traceback/pa004_traceback_test008.py', 20, 'middle', ['        self.inner()\n'], 0), (<frame object at 0x7f958c77b208>, '/home/anton/eclipse-workspace/Python2_7/pos/Docs/Problem Analysis/PA004 Traceback/pa004_traceback_test008.py', 17, 'inner', ["        raise CustomError('testing')\n"], 0)]
```

In order to extract the data from a **frame** object there is a convenient function **inspect.getframeinfo**(), and one can even specify how many lines of the source code to extract.

[pa004_traceback_test009.py](./pa004_traceback_test009.py)

```python
import inspect

class ErrorMixin(object):
    
    def printTraceback(self):
        for Item in inspect.trace():
            Frame = Item[0]
            print inspect.getframeinfo(Frame, 3)

class CustomError(StandardError, ErrorMixin):
    
    def __init__(self, strMessage):
        super(CustomError, self).__init__(strMessage)

class TestClass(object):
    def inner(self):
        raise CustomError('testing')

    def middle(self):
        self.inner()

    def outer(self):
        self.middle()

if __name__ == '__main__':
    try:
        TestObject = TestClass()
        TestObject.outer()
    except CustomError as err:
        err.printTraceback()
```

**output**

```bash
Traceback(filename='/home/anton/eclipse-workspace/Python2_7/pos/Docs/Problem Analysis/PA004 Traceback/pa004_traceback_test009.py', lineno=32, function='<module>', code_context=['        TestObject.outer()\n', '    except CustomError as err:\n', '        err.printTraceback()\n'], index=2)
Traceback(filename='/home/anton/eclipse-workspace/Python2_7/pos/Docs/Problem Analysis/PA004 Traceback/pa004_traceback_test009.py', lineno=25, function='outer', code_context=['    def outer(self):\n', '        self.middle()\n', '\n'], index=1)
Traceback(filename='/home/anton/eclipse-workspace/Python2_7/pos/Docs/Problem Analysis/PA004 Traceback/pa004_traceback_test009.py', lineno=22, function='middle', code_context=['    def middle(self):\n', '        self.inner()\n', '\n'], index=1)
Traceback(filename='/home/anton/eclipse-workspace/Python2_7/pos/Docs/Problem Analysis/PA004 Traceback/pa004_traceback_test009.py', lineno=19, function='inner', code_context=['    def inner(self):\n', "        raise CustomError('testing')\n", '\n'], index=1)
```

**Frame** objects do not contain all the information required for the unambiguous distinction between the usual functions and class / instance methods calls without deeper analysis of the execution environment within the frame. On the other hand, they can provide enough data to make a good ‘educated guess’, which should be enough in the majority of the situations, as long as the code adheres to the general conventions. The trick lays in the simple ‘has a’ analysis of the dictionary of the frame’s local variables. The idea is taken from <a id="bref4">[<sup>^4</sup>](#aref4)</a>.

At first, there is a convenient standard library’s function **inspect.getmodule**(), which is quite accurate at ‘guessing’ in which module an object is defined. Secondly, when a class or instance method is called, a reference to an instance of the class (usually named ‘self’) or to the class as a type itself (usually named ‘cls’) must be present in the local variables. So, one can look-up the local variables dictionary for each frame (its attribute **f_locals**) in order to detect a method call as well as to which class / class instance it is belongs. Apparently, this approach fails with the static methods, which do not have such a reference, or if a programmer ignores the usual conventions.
Let’s just illustrate the said above.

[pa004_traceback_test010.py](./pa004_traceback_test010.py)

```python
import inspect

class ErrorMixin(object):
    
    def printTraceback(self):
        for Item in inspect.trace():
            print Item
            print len(Item)
            Frame = Item[0]
            print inspect.getframeinfo(Frame, 3)
            Module = inspect.getmodule(Frame)
            print Module.__name__
            print Frame.f_locals

class CustomError(StandardError, ErrorMixin):
    
    def __init__(self, strMessage):
        super(CustomError, self).__init__(strMessage)

class TestClass(object):
    def inner(self):
        raise CustomError('testing')

    def middle(self):
        self.inner()

    def outer(self):
        self.middle()

if __name__ == '__main__':
    try:
        TestObject = TestClass()
        TestObject.outer()
    except CustomError as err:
        err.printTraceback()
```

**output**

```bash
(<frame object at 0x7f3681090938>, '/home/anton/eclipse-workspace/Python2_7/pos/Docs/Problem Analysis/PA004 Traceback/pa004_traceback_test010.py', 35, '<module>', ['        TestObject.outer()\n'], 0)
6
Traceback(filename='/home/anton/eclipse-workspace/Python2_7/pos/Docs/Problem Analysis/PA004 Traceback/pa004_traceback_test010.py', lineno=37, function='<module>', code_context=['        TestObject.outer()\n', '    except CustomError as err:\n', '        err.printTraceback()\n'], index=2)
__main__
{'TestObject': <__main__.TestClass object at 0x7f36810593d0>, 'CustomError': <class '__main__.CustomError'>, 'err': CustomError('testing',), '__builtins__': <module '__builtin__' (built-in)>, '__file__': '/home/anton/eclipse-workspace/Python2_7/pos/Docs/Problem Analysis/PA004 Traceback/pa004_traceback_test010.py', 'inspect': <module 'inspect' from '/usr/lib/python2.7/inspect.pyc'>, 'TestClass': <class '__main__.TestClass'>, '__package__': None, '__name__': '__main__', 'ErrorMixin': <class '__main__.ErrorMixin'>, '__doc__': None}
(<frame object at 0x7f367fb77050>, '/home/anton/eclipse-workspace/Python2_7/pos/Docs/Problem Analysis/PA004 Traceback/pa004_traceback_test010.py', 30, 'outer', ['        self.middle()\n'], 0)
6
Traceback(filename='/home/anton/eclipse-workspace/Python2_7/pos/Docs/Problem Analysis/PA004 Traceback/pa004_traceback_test010.py', lineno=30, function='outer', code_context=['    def outer(self):\n', '        self.middle()\n', '\n'], index=1)
__main__
{'self': <__main__.TestClass object at 0x7f36810593d0>}
(<frame object at 0x7f367fb77200>, '/home/anton/eclipse-workspace/Python2_7/pos/Docs/Problem Analysis/PA004 Traceback/pa004_traceback_test010.py', 27, 'middle', ['        self.inner()\n'], 0)
6
Traceback(filename='/home/anton/eclipse-workspace/Python2_7/pos/Docs/Problem Analysis/PA004 Traceback/pa004_traceback_test010.py', lineno=27, function='middle', code_context=['    def middle(self):\n', '        self.inner()\n', '\n'], index=1)
__main__
{'self': <__main__.TestClass object at 0x7f36810593d0>}
(<frame object at 0x7f3681008208>, '/home/anton/eclipse-workspace/Python2_7/pos/Docs/Problem Analysis/PA004 Traceback/pa004_traceback_test010.py', 24, 'inner', ["        raise CustomError('testing')\n"], 0)
6
Traceback(filename='/home/anton/eclipse-workspace/Python2_7/pos/Docs/Problem Analysis/PA004 Traceback/pa004_traceback_test010.py', lineno=24, function='inner', code_context=['    def inner(self):\n', "        raise CustomError('testing')\n", '\n'], index=1)
__main__
{'self': <__main__.TestClass object at 0x7f36810593d0>}
```

When a object is defined within the ‘main’ module, which is executed, not imported, the module’s name is ‘\_\_main\_\_’, as in the output of the example above. But it is replaced by the actual module’s name, if it is imported; see the next example.

[pa004_traceback_test011.py](./pa004_traceback_test011.py)

```python
from pa004_traceback_test010 import TestClass, CustomError

if __name__ == '__main__':
    try:
        TestObject = TestClass()
        TestObject.outer()
    except CustomError as err:
        err.printTraceback()
```

**output**

```bash
(<frame object at 0x7f9a020dd938>, '/home/anton/eclipse-workspace/Python2_7/pos/Docs/Problem Analysis/PA004 Traceback/pa004_traceback_test011.py', 8, '<module>', ['        TestObject.outer()\n'], 0)
6
Traceback(filename='/home/anton/eclipse-workspace/Python2_7/pos/Docs/Problem Analysis/PA004 Traceback/pa004_traceback_test011.py', lineno=10, function='<module>', code_context=['        TestObject.outer()\n', '    except CustomError as err:\n', '        err.printTraceback()\n'], index=2)
__main__
{'CustomError': <class 'pa004_traceback_test010.CustomError'>, 'err': CustomError('testing',), '__builtins__': <module '__builtin__' (built-in)>, '__file__': '/home/anton/eclipse-workspace/Python2_7/pos/Docs/Problem Analysis/PA004 Traceback/pa004_traceback_test011.py', 'TestClass': <class 'pa004_traceback_test010.TestClass'>, '__package__': None, '__name__': '__main__', 'TestObject': <pa004_traceback_test010.TestClass object at 0x7f9a020a6490>, '__doc__': None}
(<frame object at 0x7f9a00bdf050>, '/home/anton/eclipse-workspace/Python2_7/pos/Docs/Problem Analysis/PA004 Traceback/pa004_traceback_test010.py', 30, 'outer', ['        self.middle()\n'], 0)
6
Traceback(filename='/home/anton/eclipse-workspace/Python2_7/pos/Docs/Problem Analysis/PA004 Traceback/pa004_traceback_test010.py', lineno=30, function='outer', code_context=['    def outer(self):\n', '        self.middle()\n', '\n'], index=1)
pa004_traceback_test010
{'self': <pa004_traceback_test010.TestClass object at 0x7f9a020a6490>}
(<frame object at 0x7f9a00bdf200>, '/home/anton/eclipse-workspace/Python2_7/pos/Docs/Problem Analysis/PA004 Traceback/pa004_traceback_test010.py', 27, 'middle', ['        self.inner()\n'], 0)
6
Traceback(filename='/home/anton/eclipse-workspace/Python2_7/pos/Docs/Problem Analysis/PA004 Traceback/pa004_traceback_test010.py', lineno=27, function='middle', code_context=['    def middle(self):\n', '        self.inner()\n', '\n'], index=1)
pa004_traceback_test010
{'self': <pa004_traceback_test010.TestClass object at 0x7f9a020a6490>}
(<frame object at 0x7f9a02055208>, '/home/anton/eclipse-workspace/Python2_7/pos/Docs/Problem Analysis/PA004 Traceback/pa004_traceback_test010.py', 24, 'inner', ["        raise CustomError('testing')\n"], 0)
6
Traceback(filename='/home/anton/eclipse-workspace/Python2_7/pos/Docs/Problem Analysis/PA004 Traceback/pa004_traceback_test010.py', lineno=24, function='inner', code_context=['    def inner(self):\n', "        raise CustomError('testing')\n", '\n'], index=1)
pa004_traceback_test010
{'self': <pa004_traceback_test010.TestClass object at 0x7f9a020a6490>}
```

And now we have reached the culmination of the analysis. Let’s create a class responsible for the creation of an exception traceback object upon own instantiation, its storage and analysis.

[pa004_traceback_test012.py](./pa004_traceback_test012.py)

```python
import inspect

class TraceBack(object):
    
    ConsoleWidth = 72
    
    ContextLenght = 3
    
    def __init__(self, iSkipLastEntries = None):
        try:
            tblstTemp = inspect.trace(self.ContextLenght)
            if (isinstance(iSkipLastEntries, (int, long))
                                        and iSkipLastEntries > 0
                                        and iSkipLastEntries < len(tblstTemp)):
                self._tblstTraceback = tblstTemp[ : -iSkipLastEntries]
            else:
                self._tblstTraceback = tblstTemp
        except:
            self._tblstTraceback = None
    
    def __del__(self):
        if not (self._tblstTraceback is None):
            iLen = len(self._tblstTraceback)
            try:
                for iIdx in range(iLen):
                    for iOtherIdx in range(6):
                        del self._tblstTraceback[iIdx][iOtherIdx]
                del self._tblstTraceback
                self._tblstTraceback = None
            except:
                del self._tblstTraceback
                self._tblstTraceback = None
    
    @property
    def CallChain(self):
        strlstCallers = []
        if not (self._tblstTraceback is None):
            for tupItem in self._tblstTraceback:
                objFrame = tupItem[0]
                strModule = inspect.getmodule(objFrame).__name__
                strCaller = tupItem[3]
                if strCaller == '<module>':
                    strlstCallers.append(strModule)
                else:
                    dictLocals = objFrame.f_locals
                    if 'self' in dictLocals:
                        strClass = dictLocals['self'].__class__.__name__
                        strlstCallers.append('.'.join([strModule, strClass,
                                                                    strCaller]))
                    elif 'cls' in dictLocals:
                        strClass = dictLocals['cls'].__name__
                        strlstCallers.append('.'.join([strModule, strClass,
                                                                    strCaller]))
                    else:
                        strlstCallers.append('.'.join([strModule, strCaller]))
        return strlstCallers
    
    @property
    def FullInfo(self):
        strInfo = ''
        strlstCallers = self.CallChain
        if len(strlstCallers):
            for iIdx, tupItem in enumerate(self._tblstTraceback):
                strFilePath = tupItem[1]
                iLineNum = tupItem[2]
                strCaller = tupItem[3]
                strFullCaller = strlstCallers[iIdx]
                strlstCodeLines = tupItem[4]
                iLineIndex = tupItem[5]
                iMaxDigits = len(str(iLineNum + iLineIndex))
                if strCaller == '<module>':
                    strCallerInfo = 'In module {}'.format(strFullCaller)
                else:
                    strCallerInfo = 'Caller {}()'.format(strFullCaller)
                strFileInfo = 'Line {} in {}'.format(iLineNum, strFilePath)
                strlstCodeInfo = []
                for iLineIdx, _strLine in enumerate(strlstCodeLines):
                    strLine = _strLine.rstrip()
                    iRealLineNum = iLineNum - iLineIndex + iLineIdx
                    strLineNum = str(iRealLineNum)
                    while len(strLineNum) < iMaxDigits:
                        strLineNum = '0{}'.format(strLineNum)
                    if iRealLineNum == iLineNum:
                        strLineNum = '>{} '.format(strLineNum)
                    else:
                        strLineNum = ' {} '.format(strLineNum)
                    if len(strLine) > (self.ConsoleWidth - 2 - iMaxDigits):
                        strFullLine = '{}{}...'.format(strLineNum,
                                strLine[ : self.ConsoleWidth - 5 - iMaxDigits])
                    else:
                        strFullLine = '{}{}'.format(strLineNum, strLine)
                    strlstCodeInfo.append(strFullLine)
                strCodeInfo = '\n'.join(strlstCodeInfo)
                strInfo = '\n'.join([strInfo, strCallerInfo, strFileInfo,
                                                                strCodeInfo])
        if len(strInfo):
            strInfo = strInfo.lstrip()
        return strInfo
```

The class data attribute (field) **ConsoleWidth** defines the maximum length in ASCII characters of the source code’s line to be shown in the output. Note that each line will be prefixed with its number surrounded by two extra characters. If the of the code’s line including the indentation and its added number line exceeds the value stored in the **ConsoleWidth** attribute, the line will be truncated and three dots (**…**) will be added to the end. The value of this class attribute can be changed at any time and it will affect all already existing instances as well as all new instances to be created.

The second class data attribute **ContextLength** defines how many lines of the source code to retrieve within each frame with the ‘error’ line being centered. It can also be changed at any time, but it will affect only the new instances created afterwards.

This class can be instantiated with an optional argument defining how many of the last (deepest from the top level of the interpreter loop) frames should be hidden. This argument, if passed, should be a non-negative integer, however its value should not exceed the length of the call stack. Otherwise this argument is ignored. Basically, the instantiation method retrieves the exception call traceback, optionally removes the specified number of the deepest frames and stores the result in the own instance attribute. The result is stored in a ‘private’ instance attribute **_tblstTraceback**. If any exception has been raised in the process, the None value is stored instead.

The special method **\_\_del\_\_**() - actually, a descriptor, ensures the proper deletion of the retrieved data, especially of the frame references in order to avoid memory leakage. Eventually, the garbage collection will delete all old and unused frames, but the unwanted and abandoned frames’ references can delay this process causing performance deterioration.

The property **CallChain** returns a list of fully qualified names of the functions / methods in the call chain, unless the ‘private’ attribute **_tblstTraceback** (defined in the initialization method) is None, in which case an empty list is returned. For each traceback entry the frame object is extracted, and the name of the module is requested for it. Then the name of the caller is analyzed (the fourth element of a traceback entry). Unless it is ‘&lt;module&gt;’ the **f_locals** attribute of the corresponding frame is analyzed. If that dictionary contains the key ‘self’, the value of that key (reference to a class instance) is taken, and the name of the class is defined by its nested attribute **\_\_class\_\_.\_\_name\_\_**. If the key ‘cls’ is present – it refers to a class, which name is defined by the key value’s attribute **\_\_name\_\_**. Otherwise, the caller is supposed to be a usual function within that module. Finally, if the caller is ‘&lt;module&gt;’ the corresponding module’s name is taken as the fully qualified name of the caller.

The property **FullInfo** returns the full traceback dump (similar to these seen in the top level of the interpreter loop) packed as multiple lines within a single string object. It loops through the stored traceback entries and the list of the fully qualified names of the callers (as returned by the previous property). For each traceback entry several lines of the text are added: the fully qualified name of the caller as the first line, the second line containing the path to the corresponding module and the line’s number (index), where the call has occurred, and as many lines of the source code as there were obtained during instantiation (defined by the class attribute **ContextLength**). Each line of the code is prefixed by its number, using left zero padding if required in order to ensure the constant length of such a prefix for each line. For the line where the call has occurred the number is prefixed by ‘>’ symbol and a single whitespace is added between the number and the actual code. For other lines the line number is surrounded by single whitespace characters on the both sides. The original indentation of each source code’s line is preserved. However, if the combined length (in ASCII characters) of the source code’s line and its prefix (number) exceeds the value stored in the class attribute ConsoleWidth, the original code’s line is truncated and ‘**...**’ is added at the end.

The custom exceptions and the traceback mix-in classes are defined in another module.

[pa004_traceback_test013.py](./pa004_traceback_test013.py)

```python
from pa004_traceback_test012 import TraceBack

class ErrorMixin(object):
    
    @property
    def Traceback(self):
        if ((not hasattr(self, '_traceback')) or
                                (not isinstance(self._traceback, TraceBack))):
            if not hasattr(self, '_skip') or (self._skip is None):
                self._traceback = TraceBack()
            else:
                self._traceback = TraceBack(self._skip)
        return self._traceback
    
    @property
    def FullInfo(self):
        strInfo = '\n'.join([
                        '{}: {}'.format(self.__class__.__name__, self.message),
                        self.Traceback.FullInfo])
        return strInfo

class CustomError(StandardError, ErrorMixin):
    
    def __init__(self, strMessage, Traceback = None, SkipLast = None):
        if isinstance(Traceback, TraceBack):
            self._traceback = Traceback
            self._skip = None
        else:
            self._traceback = None
            if isinstance(SkipLast, (int, long)) and SkipLast > 0:
                self._skip = SkipLast
            else:
                self._skip = None
        super(CustomError, self).__init__(strMessage)

class UnawareError(StandardError, ErrorMixin):
    pass
```

The mix-in class **ErrorMixin** simply defines two properties. The first one – **Traceback** – simply returns the instance attribute _traceback if it is already defined and is an instance of the **TraceBack** class. Otherwise, a new instance of that class is created, stored in the corresponding instance attribute, and its reference is returned. In the second case it is also checked if there is an instance attribute **_skip**, and that its value is not None, in which case the value of that attribute is used during the instantiation of the **TraceBack** class to define how many of the deepest inner frames are to be hidden.

The second property – **FullInfo** – is a short-cut, syntax sugar for the **TraceBack.FullInfo** with respect to the instance attribute **_traceback**.

The custom exception class **CustomError** uses the **ErrorMixin** class as its second parent. Note that either another instance of the **TraceBack** class or a positive integer number of the deepest frames to hide can be passed as the optional keyword arguments into the instantiation method.

If an instance of the **TraceBack** class is passed, it is simply referenced by the instance attribute **_traceback**, and the second optional keyword argument is simply ignored. In this case, when the properties **Traceback** or **FullInfo** are accessed, a new traceback object is not created, but the one passed during the instantiation is used.

If an instance  of the **TraceBack** class is not passed, the value of the second optional keyword argument is stored in the instance attribute **_skip** only if it is a positive integer. An instance of the **TraceBack** class is created and stored in the instance attribute **_traceback** only on demand – upon the first access to the inherited property **Traceback** (directly) or **FullInfo** property (indirectly).

The second custom exception **UnawareError** simply inherits from the built-in **StandardError** and the mix-in **ErrorMixin**, and doesn nothing else.

Finally, the test objects are defined in the third module. It contains two usual functions – one raising an exception, and another – simply calling the first one – and a class with 2 class methods and 3 instance methods. The class methods also implement the call chain of calling a method that raises an exception from another class method. With the instance methods the call chain consists of 3 methods, but the inner-most raises **CustomException** with an instruction to hide the last call, so the traceback analysis should ignore the inner-most call.

[pa004_traceback_test014.py](./pa004_traceback_test014.py)

```python
from pa004_traceback_test013 import CustomError, UnawareError

class TestClass(object):
    
    @classmethod
    def inner_class(cls):
        raise CustomError('testing in class method')
    
    @classmethod
    def outer_class(cls):
        cls.inner_class()
    
    @classmethod
    def call_outside(cls):
        outer_func()
    
    def inner(self):
        raise CustomError('testing in instance method', SkipLast = 1)

    def middle(self):
        self.inner()

    def outer(self):
        self.middle()

def inner_func():
    raise CustomError('testing in function')

def outer_func():
    inner_func()

if __name__ == '__main__':
    TestObject = TestClass()
    try:
        TestObject.outer()
    except CustomError as err:
        print err.FullInfo, '\n'
    try:
        TestClass.outer_class()
    except CustomError as err:
        print err.FullInfo, '\n'
    try:
        TestObject.call_outside()
    except CustomError as err:
        print err.FullInfo, '\n'
    try:
        TestObject.outer_class()
    except CustomError as err:
        try:
            raise CustomError('Caught and raised simple')
        except CustomError as err_inner:
            print err_inner.FullInfo, '\n'
    try:
        TestObject.outer_class()
    except CustomError as err:
        try:
            objTraceback = err.Traceback
            raise CustomError('Caught and raised smart', Traceback=objTraceback)
        except CustomError as err_inner:
            print err_inner.FullInfo, '\n'
    try:
        raise UnawareError('some generic error')
    except UnawareError as err:
        print err.FullInfo
```

**output**

```bash
CustomError: testing in instance method
In module __main__
Line 37 in /home/anton/eclipse-workspace/Python2_7/pos/Docs/Problem Analysis/PA004 Traceback/pa004_traceback_test014.py
 36     try:
>37         TestObject.outer()
 38     except CustomError as err:
Caller __main__.TestClass.outer()
Line 26 in /home/anton/eclipse-workspace/Python2_7/pos/Docs/Problem Analysis/PA004 Traceback/pa004_traceback_test014.py
 25     def outer(self):
>26         self.middle()
 27 
Caller __main__.TestClass.middle()
Line 23 in /home/anton/eclipse-workspace/Python2_7/pos/Docs/Problem Analysis/PA004 Traceback/pa004_traceback_test014.py
 22     def middle(self):
>23         self.inner()
 24  

CustomError: testing in class method
In module __main__
Line 41 in /home/anton/eclipse-workspace/Python2_7/pos/Docs/Problem Analysis/PA004 Traceback/pa004_traceback_test014.py
 40     try:
>41         TestClass.outer_class()
 42     except CustomError as err:
Caller __main__.TestClass.outer_class()
Line 13 in /home/anton/eclipse-workspace/Python2_7/pos/Docs/Problem Analysis/PA004 Traceback/pa004_traceback_test014.py
 12     def outer_class(cls):
>13         cls.inner_class()
 14 
Caller __main__.TestClass.inner_class()
Line 9 in /home/anton/eclipse-workspace/Python2_7/pos/Docs/Problem Analysis/PA004 Traceback/pa004_traceback_test014.py
 08     def inner_class(cls):
>09         raise CustomError('testing in class method')
 10  

CustomError: testing in function
In module __main__
Line 45 in /home/anton/eclipse-workspace/Python2_7/pos/Docs/Problem Analysis/PA004 Traceback/pa004_traceback_test014.py
 44     try:
>45         TestObject.call_outside()
 46     except CustomError as err:
Caller __main__.TestClass.call_outside()
Line 17 in /home/anton/eclipse-workspace/Python2_7/pos/Docs/Problem Analysis/PA004 Traceback/pa004_traceback_test014.py
 16     def call_outside(cls):
>17         outer_func()
 18 
Caller __main__.outer_func()
Line 32 in /home/anton/eclipse-workspace/Python2_7/pos/Docs/Problem Analysis/PA004 Traceback/pa004_traceback_test014.py
 31 def outer_func():
>32     inner_func()
 33 
Caller __main__.inner_func()
Line 29 in /home/anton/eclipse-workspace/Python2_7/pos/Docs/Problem Analysis/PA004 Traceback/pa004_traceback_test014.py
 28 def inner_func():
>29     raise CustomError('testing in function')
 30  

CustomError: Caught and raised simple
In module __main__
Line 52 in /home/anton/eclipse-workspace/Python2_7/pos/Docs/Problem Analysis/PA004 Traceback/pa004_traceback_test014.py
 51         try:
>52             raise CustomError('Caught and raised simple')
 53         except CustomError as err_inner: 

CustomError: Caught and raised smart
In module __main__
Line 56 in /home/anton/eclipse-workspace/Python2_7/pos/Docs/Problem Analysis/PA004 Traceback/pa004_traceback_test014.py
 55     try:
>56         TestObject.outer_class()
 57     except CustomError as err:
Caller __main__.TestClass.outer_class()
Line 13 in /home/anton/eclipse-workspace/Python2_7/pos/Docs/Problem Analysis/PA004 Traceback/pa004_traceback_test014.py
 12     def outer_class(cls):
>13         cls.inner_class()
 14 
Caller __main__.TestClass.inner_class()
Line 9 in /home/anton/eclipse-workspace/Python2_7/pos/Docs/Problem Analysis/PA004 Traceback/pa004_traceback_test014.py
 08     def inner_class(cls):
>09         raise CustomError('testing in class method')
 10  

UnawareError: some generic error
In module __main__
Line 64 in /home/anton/eclipse-workspace/Python2_7/pos/Docs/Problem Analysis/PA004 Traceback/pa004_traceback_test014.py
 63     try:
>64         raise UnawareError('some generic error')
 65     except UnawareError as err:
```

Note the following:

* the fully qualified names are properly resolved: as from the module itself (top level), from a class’ method (class or instance methods), and from a usual function within a module; even when a usual function is called from a class’ method (second case)
* the frame corresponding to the exception raise within the instance method **inner**() is not shown, as is requested – the first case
* when an exception is caught and another exception is raised with the traceback of the first one (the next to the last case), the traceback information of the second exception indeed refers to the call chain of the first one, as required
* the **UnawareError**’s exception call chain is shown properly, even though the exception class itself cares nothing about the tracing, but all the ‘magic’ comes from the mix-in class

As the final example these test objects re imported into another module and the same **try...except** constructs are re-used.

[pa004_traceback_test015.py](./pa004_traceback_test015.py)

```python
from pa004_traceback_test013 import CustomError, UnawareError
from pa004_traceback_test014 import TestClass, outer_func

if __name__ == '__main__':
    TestObject = TestClass()
    try:
        TestObject.outer()
    except CustomError as err:
        print err.FullInfo, '\n'
    try:
        TestClass.outer_class()
    except CustomError as err:
        print err.FullInfo, '\n'
    try:
        TestObject.call_outside()
    except CustomError as err:
        print err.FullInfo, '\n'
    try:
        TestObject.outer_class()
    except CustomError as err:
        try:
            raise CustomError('Caught and raised simple')
        except CustomError as err_inner:
            print err_inner.FullInfo, '\n'
    try:
        TestObject.outer_class()
    except CustomError as err:
        try:
            objTraceback = err.Traceback
            raise CustomError('Caught and raised smart', Traceback=objTraceback)
        except CustomError as err_inner:
            print err_inner.FullInfo, '\n'
    try:
        raise UnawareError('some generic error')
    except UnawareError as err:
        print err.FullInfo
```

**output**

```bash
CustomError: testing in instance method
In module __main__
Line 9 in /home/anton/eclipse-workspace/Python2_7/pos/Docs/Problem Analysis/PA004 Traceback/pa004_traceback_test015.py
 08     try:
>09         TestObject.outer()
 10     except CustomError as err:
Caller pa004_traceback_test014.TestClass.outer()
Line 26 in /home/anton/eclipse-workspace/Python2_7/pos/Docs/Problem Analysis/PA004 Traceback/pa004_traceback_test014.py
 25     def outer(self):
>26         self.middle()
 27 
Caller pa004_traceback_test014.TestClass.middle()
Line 23 in /home/anton/eclipse-workspace/Python2_7/pos/Docs/Problem Analysis/PA004 Traceback/pa004_traceback_test014.py
 22     def middle(self):
>23         self.inner()
 24  

CustomError: testing in class method
In module __main__
Line 13 in /home/anton/eclipse-workspace/Python2_7/pos/Docs/Problem Analysis/PA004 Traceback/pa004_traceback_test015.py
 12     try:
>13         TestClass.outer_class()
 14     except CustomError as err:
Caller pa004_traceback_test014.TestClass.outer_class()
Line 13 in /home/anton/eclipse-workspace/Python2_7/pos/Docs/Problem Analysis/PA004 Traceback/pa004_traceback_test014.py
 12     def outer_class(cls):
>13         cls.inner_class()
 14 
Caller pa004_traceback_test014.TestClass.inner_class()
Line 9 in /home/anton/eclipse-workspace/Python2_7/pos/Docs/Problem Analysis/PA004 Traceback/pa004_traceback_test014.py
 08     def inner_class(cls):
>09         raise CustomError('testing in class method')
 10  

CustomError: testing in function
In module __main__
Line 17 in /home/anton/eclipse-workspace/Python2_7/pos/Docs/Problem Analysis/PA004 Traceback/pa004_traceback_test015.py
 16     try:
>17         TestObject.call_outside()
 18     except CustomError as err:
Caller pa004_traceback_test014.TestClass.call_outside()
Line 17 in /home/anton/eclipse-workspace/Python2_7/pos/Docs/Problem Analysis/PA004 Traceback/pa004_traceback_test014.py
 16     def call_outside(cls):
>17         outer_func()
 18 
Caller pa004_traceback_test014.outer_func()
Line 32 in /home/anton/eclipse-workspace/Python2_7/pos/Docs/Problem Analysis/PA004 Traceback/pa004_traceback_test014.py
 31 def outer_func():
>32     inner_func()
 33 
Caller pa004_traceback_test014.inner_func()
Line 29 in /home/anton/eclipse-workspace/Python2_7/pos/Docs/Problem Analysis/PA004 Traceback/pa004_traceback_test014.py
 28 def inner_func():
>29     raise CustomError('testing in function')
 30  

CustomError: Caught and raised simple
In module __main__
Line 24 in /home/anton/eclipse-workspace/Python2_7/pos/Docs/Problem Analysis/PA004 Traceback/pa004_traceback_test015.py
 23         try:
>24             raise CustomError('Caught and raised simple')
 25         except CustomError as err_inner: 

CustomError: Caught and raised smart
In module __main__
Line 28 in /home/anton/eclipse-workspace/Python2_7/pos/Docs/Problem Analysis/PA004 Traceback/pa004_traceback_test015.py
 27     try:
>28         TestObject.outer_class()
 29     except CustomError as err:
Caller pa004_traceback_test014.TestClass.outer_class()
Line 13 in /home/anton/eclipse-workspace/Python2_7/pos/Docs/Problem Analysis/PA004 Traceback/pa004_traceback_test014.py
 12     def outer_class(cls):
>13         cls.inner_class()
 14 
Caller pa004_traceback_test014.TestClass.inner_class()
Line 9 in /home/anton/eclipse-workspace/Python2_7/pos/Docs/Problem Analysis/PA004 Traceback/pa004_traceback_test014.py
 08     def inner_class(cls):
>09         raise CustomError('testing in class method')
 10  

UnawareError: some generic error
In module __main__
Line 36 in /home/anton/eclipse-workspace/Python2_7/pos/Docs/Problem Analysis/PA004 Traceback/pa004_traceback_test015.py
 35     try:
>36         raise UnawareError('some generic error')
 37     except UnawareError as e
```
As can be seen, the module’s name is resolved properly.

## Conclusion

The proposed method of the traceback of the call chain that has led to an exception is based on the Standard Python Library module **inspect**, namely its function **trace**().

* A dedicated class will be used to retrieve the traceback of the last exception from the system in the form of the named tuple, which is also responsible for the analysis of the traceback, extraction of the call chain with the fully qualified names of the usual functions and class or instance methods
* Upon instantiation of that traceback analysis class as an optional argument a number of the deepest frames to hide can be defined
* A mix-in class for the custom exceptions is responsible for the interfacing that traceback inspection class instance and creation on demand of such an instance if it is not already present in the custom exception class
* A custom exception class can simply inherit from that mix-in class, or, optionally, also create an instance of the traceback analysis class during own instantiation (optionally skipping a defined number of the deepest frames), or even use another instance of such a class as a substitution
* In order to ensure the proper class and instance methods resolution, all class definitions must adhere to the common convention of ‘self’ and ‘cls’ references to an instance or a class itself in the signatures of all their methods
    
With the replacement of the **inspect.trace**() call by the call to **inspect.stack**() a generic stack traceback analysis can be implemented instead of the specific case of the exception’s traceback.

## References

<a id="aref1">[^1]</a> https://docs.python.org/2/library/sys.html   [&#x2B0F;](#bref1)

<a id="aref2">[^2]</a> https://docs.python.org/2/library/traceback.html     [&#x2B0F;](#bref2)

<a id="aref3">[^3]</a> https://docs.python.org/2/library/inspect.html     [&#x2B0F;](#bref3)

<a id="aref4">[^4]</a> https://www.programcreek.com/python/example/1190/inspect.currentframe      [&#x2B0F;](#bref4)