# pos
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

None of these goals is new; there are already many projects / libraries implementing these features, but the fun is to do it yourself and in the same, consistent manner.
Extra components can and will be build based on these base objects.