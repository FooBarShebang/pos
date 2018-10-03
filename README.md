# pos Library

as in Python on Steroids / Python of Steel - working title

## Description

Hacking of the Python programming language in its original MIT / UC Berkeley sense, not as in the computer security breaching.

## Goal

Python is a dynamic though strong typed language with all its benefits and beauty. In some cases though, especially for the "big data" processing of production quality with unpredictable input source, static typing has its merits.
Secondly, the object model of Python is fully open and transparent, whereas sometimes data encapsulation is also beneficial.

Finally, callback tracing system of Python is ok for the debugging but quite quite cumbersome for the analysis of the origin of an intercepted exception.

Thus the goal of the project is to build a framework of objects (as classes) providing 'data sanity checks' measures:

* Partial data encapsulation in object model
* Simpler objects` introspection
* Simpler call chain tracing
* Partial 'Design by Contract' paradigm implementation
* Custom data types more resembling those available in the 'classic' static typed languages, including but not limited to unsigned integer numbers, constants and enumeration types
* Unified structure of custom exceptions to separate the wrong / unexpected input data from the errors in the source code

Extra components can and will be build based on these base objects.

## Rationale

None of these goals is new; there are already many projects / libraries implementing these features, for instance, in the case of the Design by Contract:

* [andreacensi @ GitHub](https://andreacensi.github.io/contracts/)
* [PyContract @ Wayforward](http://www.wayforward.net/pycontract/)
* [PyDBC @ NonGNU](http://www.nongnu.org/pydbc/)
* [DeadPixi @ GitHub](https://github.com/deadpixi/contracts)

But the fun is to do it yourself and in the same, consistent manner.

Besides, I have some personal grudges with these implementations and my own wishes:

* I do not like:
  - decorators', functions' or methods' in general definitions crowded with parameters
  - obscure DSL
  - doc-strings loaded with contract definitions (as well as doc-tests!); the doc-string should explain WHAT function does and how to use it in a human readable form
* I want to be able to:
  - define contracts in a verbose and flexible manner using external objects (with respect to the function / method), e.g. dictionary like, which can be either a part of the code, or being stored outside the module in some sort of a configuration file (JSON, for instance)
  - enable, disable or alter (if required) the contract per function / method at the run-time
  - use any data type, including the user defined classes without necessity to register them somehow
  - be sure that the scheme works as expected even if the attributes resolution scheme is altered (for the data encapsulation)
  - seamlessly integrate the functionality into the unified framework / eco-system, including the exceptions convention

## Documentation

All documentation is placed in the sub-folder 'Docs' and is grouped by topics and types. All documents are written as text files using Markdown formatting.

### Design and Requirements

* [DE001 Core Features](./Docs/Design_and_Requirements/DE001_Core_Features.md)

### Problem Analysis

* [PA001 Descriptors](./Docs/Problem_Analysis/PA001_Descriptors/PA001_Descriptors.md)
* [PA001 Decorators](./Docs/Problem_Analysis/PA002_Decorators/PA002_Decorators.md)
* [PA001 Virtual Inheritance](./Docs/Problem_Analysis/PA003_Virtual_Inheritance_Exceptions/PA003_Virtual_Inheritance_Exceptions.md)
* [PA001 Traceback](./Docs/Problem_Analysis/PA004_Traceback/PA004_Traceback_of_Exceptions.md)

### User Documentation

Here the documents are grouped according to the file structure, althoug they are all stored in a single sub-folder.

* **utils**
  - docstring_parsers module [UD003](./Docs/User_Documentation/UD003_pos.utils.docstring_parsers_Reference.md)
  - dynamic_import module [UD004](./Docs/User_Documentation/UD004_pos.utils.dynamic_import_Reference.md)
  - loggers module [UD005](./Docs/User_Documentation/UD005_pos.utils.loggers_Reference.md)
  - traceback module [UD001](./Docs/User_Documentation/UD001_pos.utils.traceback_Reference.md)
* exceptions module [UD002](./Docs/User_Documentation/UD002_pos.exceptions_Reference.md)

## Structure

* package **utils**
  - module [**attr_info**](./utils/attr_info.py)
    * class AttributeInfo
    * class FieldInfo
    * class MethodInfo(AttributeInfo):
  - module [**docstring_parsers**](./utils/docstring_parsers.py)
    * class GenericParser
    * class EpytextParser
    * class reSTParser
    * class GoogleParser
    * class AAParser
    * class NumPydocParser
    * function guess_docstyle()
    * function indent_docstring()
  - module [**dynamic_import**](./utils/dynamic_import.py)
    * function import_module()
    * function import_from_module()
  - module [**loggers**](./utils/loggers.py)
    * class ConsoleLogger
    * class DualLogger
  - module [**traceback**](./utils/traceback.py)
    * class StackTraceback
    * class ExceptionTraceback
* module [**base_classes**](./base_classes.py)
  - class DescriptedABC_Meta
  - class DescriptedABC
* module [**exceptions**](./exceptions.py)
  - class ErrorMixin
  - class CustomError
  - class DesignContractError
  - class ConstantAssignment
  - class CustomAttributeError
  - class ConstantAttributeAssignment
  - class NotExistingAttribute
  - class PrivateAttributeAccess
  - class NotInDCError
  - class CustomTypeError
  - class DCArgumentType
  - class DCReturnType
  - class CustomValueError
  - class DCArgumentValue
  - class DCReturnValue

## Functionality

### Core

#### Module exceptions

Custom exceptions with the added functionality for the analysis of the exception traceback, which are integrated into the standard exceptions tree like branches originated from TypeError, ValueError, AttributeError, etc. Virtual subclass relations are also used in order to enable 'umbrella' catching of the custom exceptions closely related by their meaning / situations to be raised in but belonging to the different branches.

These exceptions can be raised with the optional arguments, which allow substitution of the actual traceback of that particular exception by the traceback of another exception (handy if raised as a part of handling of another one) as well as 'hiding' of the specified number of the innermost call frames in the traceback.

Apart from the standard exceptions' arguments **message** and **args** these custom exceptions provide read-only properties **CallChain** and **Info**, which can be used for the analysis of the traceback of a caught exception. The first property returns a list of strings - the fully qualified names of the callers, whereas the second property returns a single string containing multiple lines ('\n' separated) human-readable representation of the traceback frames records.

### Additional

### Utilities - package utils

#### Module traceback

Provides two classes - **StackTraceback** and **ExceptionTraceback** which are useful for the analysis of the the call stack and of the exception traceback. In fact, the added functionality of the custom exceptions is based on the class **ExceptionTraceback**. Both classes have identical API - read-only properties **CallChain** and **Info**, which can be used for the analysis of the traceback of a caught exception. The first property returns a list of strings - the fully qualified names of the callers, whereas the second property returns a single string containing multiple lines ('\n' separated) human-readable representation of the traceback frames records.

The **StackTraceback** provides the traceback in the inverse order with respect to **inspect.stack**() call - the outermost (the first) call is the first element, whereas the innermost (last) call frame is the last element. The traceback starts at the top level of the interpreter's loop (as module '__main__') and ends in the frame where this class has been instantiated.

The **ExceptionTraceback** provides the traceback in the same order as **inspect.trace**() call - the first element is the frame where an exception is being handled, the last element - the frame, where it has been raised.

With the both classes a specified number of the last elements can be 'hidden' / removed from the traceback.

#### Module docstring_parsers

Provides 6 classes: **GenericParser** - prototype class for the specific docstring style parsers, **EpytextParser** - specific parser for the Epytext style (similar to javadoc), **reSTParser** - specific parser for the reStructured Text format of the docstrings, **GoogleParser** - specific parser for the Google style of the docstrings, **AAParser** - specific parser for the 'extended' version of the Google style with the extra tokens and explicit signature recognition as well as with the recognition of the optional arguments, **NumPydocParser** - specific parser for the NumPy docstring style.

All these classes are Singleton-like, i.e. there is no need for their instantiation, since all defined methods are class methods. All these classes have the same set of methods

- trimDocstring(): removes extra indentation, heading and tailing empty lines, tailing whitespaces in each line
- reduceDocstring(): same as above plus removal of all lines related to the auto-generation of the documentation, according to the defined standard tokens
- extractSignature(): extracts the explicitly defined signature of the method / function; currently is meaningful only for the AA docstyle (extended Google style); for other formats returns None
- extractArguments(): extracts the names (as a list of strings) of all explicitly defined arguments in the docstring; in the case of the AA docstyle also recognizes the optional arguments, those names are escaped with '/'.

Implements the function **guess_docstyle**(), which 'guesses' the most suitable parser (returns a class) by the most efficient removal of the lines related to the auto-generation of the documentation; AAParser class is the default option, when none of the parsers is able to remove any line.

Provides the function **indent_docstring**(), which adds the required number (times 4) of the spaces in front of each line.

#### Module dynamic_import

Provides 2 functions to perform dynamic, i.e. 'on demand' at the runtime import of an entire module (**import_module**()) or of a single object like class or function from a module (**import\_from\_module**()). Both functions are based upon the built-in function **importlib.import_module**(). They return reference to the imported object (module, class, function, etc.) and can, optionally, use arbitrary alias string (passed as an optional argument) as the reference name instead of the actual name of the imported object. The global symbols table (dictionary) of the 'caller' module (see built-in function **globals**()) can be passed as another optional argument; so a reference can also be placed directly into it. If such a dictionary is not provided, the reference is placed into the global symbols table of the module **utils.dynamic_import** itself.

#### Module loggers

Provides 2 classes - derived from the **logging.Logger** class in the standard library - with the added functionality of the dynamic disabling and enabling of the logging at all severity levels and simultaneous logging into different streams using separate handlers.
The class **ConsoleLogger** has two handlers: NULL ('black hole') and stdout output (console), whereas the second handler can be dynamically enabled or disabled.
The class **DualLogger** also adds the third - file logging handler, with the ability to enable or disable the console and / or file logging independently.
These classes emulate 'virtual inheritance' from the class logging.Logger by modifying the attributes resolution scheme; all attributes of an instance of logging.Logger class (which is stored by reference in the 'private' attribute \_logger) are accessible at the 'top' level of the instance, thus self.info() is the same as self._logger.info(). Furthermore, the loggers hierarchical relation implemented by the standard library is preserved; the logger created with the name 'parent.child' is a descendant of the logger created with the name 'parent'. The standard upward propagation of the message model is applied.
The enabling / disabling of the console logging has an effect only on the the 'root' of the current hierarchy, and it affects all its descendants, because only the 'root' logger of the hierarchy actually created text stream handler. Thus a message issued by a descendant is printed (if enabled) into the console by its ultimate ascendant.
The file logging enabling / disabling is independent for each logger (assuming separate log files). Thus, if both the parent and the child have file logging enabled into separate files, a message issued by the child will be logged in the both files.
