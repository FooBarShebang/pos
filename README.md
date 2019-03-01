# pos Library

as in Python on Steroids / Python of Steel - working title

## Table of Content

* [Description](#Description)
* [Installation](#Installation)
* [Goal](#Goal)
* [Rationale](#Rationale)
* [Functionality and Intended Use](#Functionality-and-Intended-Use)
* [Documentation](#Documentation)
* [Structure](#Structure)

## Description

Hacking of the Python programming language in its original MIT / UC Berkeley sense, not as in the computer security breaching.

## Installation

Clone the official repository into your local workspace / project folder:

```bash
$ git clone <repository_path> "your project folder"
```

Initialize the UML templates submodule

```bash
$ cd "your project folder"/pos/Docs/UML/Templates
$ git submodule init
```

Download the content of the UML templates submodule

```bash
$ git submodule update --recursive --remote
```

<<<<<<< HEAD
**Note**: You do not have to intialize and download the UML templates submodule if you do not plan to update the library's documentation. They are not required for the functionality of the library iteself. 

=======
>>>>>>> e04daec429afc23a0283867c49b055b7594a91e9
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

## Functionality and Intended Use

This section gives a brief overview of the functionality and intended use of the packages and modules implemented within the library. The links to the detailed documentation on the modules are provided in the [index.md](./Docs/index.md) file. The detailed packages and modules structure of the library is given in the [Structure section](#structure).

### Module exceptions

Custom exceptions with the added functionality for the analysis of the exception traceback, which are integrated into the standard exceptions tree like branches originated from **TypeError**, **ValueError**, **AttributeError**, etc. Virtual subclass relations are also used in order to enable 'umbrella' catching of the custom exceptions closely related by their meaning / situations to be raised in but belonging to the different branches.

These exceptions can be raised with the optional arguments, which allow substitution of the actual traceback of that particular exception by the traceback of another exception (handy if raised as a part of handling of another one) as well as 'hiding' of the specified number of the innermost call frames in the traceback.

### Package utils

#### Module traceback

Provides two classes with identical API, which can be used for the analysis of the function or method call chain or of the traceback of a caught exception respectively. With the both classes a specified number of the last elements (stack frames) can be 'hidden' / removed from the traceback.

#### Module docstring_parsers

Provides classes for parsing of the docstring using different styles or formats for the automated generation of the documentation:

* Epytext style (similar to javadoc)
* reStructured Text format (reST)
* Google style
* NumPy style

These classes are originally designed for removal of such specific technical data, thus showing the doc-strings in more compact and human readable form. They can also be used for the reversed purpose - extraction of the expected arguments, returned types (or entire signature), exceptions as defined in the doc-strings of the functions / methods, etc.

#### Module dynamic_import

Provides two functions to perform dynamic, i.e. 'on demand' at the runtime import of an entire module or of a single object like class or function from a module. Both functions return reference to the imported object (module, class, function, etc.) and can, optionally, use arbitrary alias string as the reference name instead of the actual name of the imported object. The global symbols table (dictionary) of the 'caller' module can be passed as another optional argument; so a reference can also be placed directly into it.

#### Module loggers

Provides two classes - derived from the **logging.Logger** class in the standard library - with the added functionality of the dynamic disabling and enabling of the logging at all severity levels and simultaneous logging into different streams using separate handlers. These classes preserve the loggers hierarchical relation implemented by the standard library; the logger created with the name 'parent.child' is a descendant of the logger created with the name 'parent'. The standard upward propagation of the message model is applied.

## Documentation

All documentation is placed in the sub-folder 'Docs' and is grouped by topics and types. All documents are written as text files using Markdown formatting. The [index.md](./Docs/index.md) file provides the structured list of the available documents.

## Structure

* package **utils**
  - module **attr_info** [source](./utils/attr_info.py), [documentation]
  - module **docstring_parsers** [source](./utils/docstring_parsers.py), [documentation](./Docs/User_Documentation/UD003_pos.utils.docstring_parsers_Reference.md)
  - module **dynamic_import** [source](./utils/dynamic_import.py), [documentation](./Docs/User_Documentation/UD004_pos.utils.dynamic_import_Reference.md)
  - module **loggers** [source](./utils/loggers.py), [documentation](./Docs/User_Documentation/UD005_pos.utils.loggers_Reference.md)
  - module **traceback** [source](./utils/traceback.py), [documentation](./Docs/User_Documentation/UD001_pos.utils.traceback_Reference.md)
* module **base_classes** [source](./base_classes.py), [documentation]
* module **exceptions** [source](./exceptions.py), [documentation](./Docs/User_Documentation/UD002_pos.exceptions_Reference.md)

More detailed overview, including implemented classes and functions per module is given in [pos Components Structure](./Docs/pos_components_structure.md) document.