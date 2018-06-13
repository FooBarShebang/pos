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
