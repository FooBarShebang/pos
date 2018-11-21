# DE001 Core Features

## Scope

This document defines the core features of the library and their functional requirements. It does not define the details of the implementation of the required functionality but states the intended design patterns / paradigms.

## Features to Implement

### Design by Contract for Functions and Methods

The goal is to minimize the amount of repetitive / ‘boiler plate’ coding in terms of the data sanity checks, especially in the case of critical functions / methods or those involved in the processing of the unpredictable user data input.

The idea is to emulate a static typing within the dynamically typed language (Python) in terms that a function / method is guaranteed by its contract to return a value of a specific type (or on of the specific types) and, optionally, within specific set / range of values if the input satisfies specific conditions; and a specific error / exception is raised when either the preconditions or postconditions checks failed. Thus, such a contract is an extension of the static typing (polymorphic) function / method signature. But a function / method’s contract can also be analysed by another function / method at the run-time, therefore a function doesn’t have to assume but can know for sure what kind of data another function requires or what kind of data it returns.

This library should implement only part of the features of the actual software pattern known as Design by Contract <a id="bref1">[<sup>1</sup>](#aref1)</a> and some additional features, namely:

* A contract for a function / method is defined as a set of formal, precise and verifiable interface specifications, like: ‘requires {so many} arguments’, ‘requires argument {name} to be an instance of sub-class of {class}’, ‘returns {data type} with value in the {range}’, etc.
* A contract directly concerns only the preconditions and / or postconditions of a function / method with the both types of checks being optional
* A contract doesn’t concern the side effects of the function / method at all
* There is no generic invariants support, except for those invariants that can be formulated as a combination of the pre- and postconditions
* A failed contract results in ‘hard fail’, i.e. a specific exception being raised
* A contract of a function / method is available for inspection by another function / method
* The checks implied by the contract can be enabled / disabled and even modified (if required) at the run-time

References for the baseline implementation via decorators are: <a id="bref2">[<sup>2</sup>](#aref2)</a>, <a id="bref3">[<sup>3</sup>](#aref3)</a> and <a id="bref4">[<sup>4</sup>](#aref4)</a>.

#### Functional Requirements

* A contract is defined by a programmer outside the function / method in the form of a dictionary or even in a configuration file (e.g. JSON format), which can be easily turned into a dictionary Python object
* A contract for a single function / method may include either or both of the preconditions (‘requires’) and postconditions (‘returns)
* The preconditions check is constructed from the checks on the individual arguments passed into the function, if there is a rule for the corresponding parameter. The preconditions check fails if any of the individual arguments checks has failed.
* The preconditions check concerns only those arguments that are mapped to the function’s parameters with the existing rules / restrictions. For instance, a function may be defined as having three parameters _**f(a, b, c)**_, but the rules are defined only for the parameters a and c. In this case the check must be successful as long as the restrictions on the first and the last arguments are met regardless of the type / value of the second argument of the function’s call.
* The check rules for the mandatory arguments, arguments with the default value and keyword arguments mapped onto the ** placeholder are defined by the parameter’s name
* The check rules for the optional positional arguments (mapped onto the * placeholder) are defined by their position; it should be possible to define (optional) specific number of such arguments expected or min and / or max allowed number of such arguments, as well as a generic / default check for all such arguments (specific rule by the positional order should override the generic rule).
* The postconditions check should be implemented as a single parameter check, since the idiom _**return x, y**_ is nothing more than a syntax sugar for _**return (x, y)**_, therefore there is no need for a name for this parameter.
* A rule for a single parameter check can be combined from several simple (type) checks of the same type with the logical OR relation – i.e. the parameter check passes if any of the simple checks passes.
* The simple checks types are:
  - parameter being a sub-class of a specific class / data type
  - parameter being an instance of a specific class / data type but not of a sequence type, with optional checks on its value:
    + not being equal a specific value
    + being greater than / greater than or equal to a specific value
    + being less than / less than or equal to a specific value
    + these optional checks, if defined, are joined with logical AND
  - parameter being of a sequence type (not a string) with the optional checks on
    + minimum or maximum (inclusively) number of the elements (length) or the length being exactly a specific value
    + specific type checks on the elements with the specified indexes
    + type check that must be applied to all elements, except those which are covered by the type checks on the elements with the specified indexes
  - parameter being a mapping type with the optional checks on
    + the values of the specified keys – specific type checks
    + type checks on the key and on the value applied to all key – value pairs except those key covered by the specific tests (previous point)
  - the value of the parameter being in the specific set of values
  - the parameter being a reference to a callable object with optional check on its signature
  - the simple type checks can be nested, e.g. in the case of the sequence / mapping / callable types checks
* Individual function / method contracts are grouped in the look-up tables using the function / method names as the keys
* The look-up contracts tables are defined at the module level for usual functions and within a class for its methods
* These look-up tables are converted into objects (as class instances), which are responsible for the acquisition of a specific contract by the function / method name, performance of the preconditions and postconditions checks (separately, returning boolean True / False values) and generation of the human readable contract information
* DbC should be implemented for the usual functions / static methods, class methods, properties and usual instance methods

### Forced Data Type / Value Checks for Instance / Class Data Attributes (Fields)

There are three basic methods to ensure the data checks during the assignment to a data attribute (field) as well as of the data retrieved from it:
* use of the **\_\_set\_\_**() and **\_\_get\_\_**() descriptors <a id="bref5">[<sup>5,</sup>](#aref5)</a><a id="bref6">[<sup>6</sup>](#aref6)</a> for the custom defined data types
* ‘hiding’ of the actual attribute and interfacing it via the public getter and setter properties
* hooking the attribute resolution methods and use of a look-up table / object defining type check rules, same as the DbC rules but applied on the attributes not methods

#### Functional Requirements

* For the approach using descriptors
  - Implemented not for all classes, but only the sub classes of a specific class
  - use of the descriptors with the instance attributes
  - use of the descriptors with the class attributes on the instances of the class
  -  use of the descriptors with the class attributes on the class itself (without instantiation)
* For the approach using properties
  - Can be applied to any class which has a DbC look-up table / object using properties decorators
  - Properties use the same DbC rules as ordinary instance methods and do not require an additional look-up table / object
  - Getter properties perform only postconditions checks
  - Setter properties perform the preconditions checks as well as check that the None value is returned
* For the approach using attributes resolution methods hooking:
  - Implemented only for the sub-classes of a specific class, not for all classes
  - Such classes must define a class data attribute as a look-up table for the creation of the instance attributes, which specifies their types and limitation on their values in the same way as DbC rules for the functions’ parameters; the same table is to be used by the attribute access methods

### Data Encapsulation by Class Instances

On the basic level the classes that implement data encapsulation must deny read and write access to any class or instance attribute (field of method) which is considered to be ‘private’, i.e. with its name starting with a single underscore. In the case of the class fields and class methods the scheme should work on the instances and the classes themselves (without instantiation). On the more advanced level the classes can define (via ‘private’ class fields as look-up tables) names of the instance fields to be created upon instantiation and to be considered either ‘private’ (neither read nor write access) or ‘protected’ instance attributes (read-only access). Of course, the encapsulation is not absolute, it can be circumvented by using the original attributes resolution methods of the **object** or **type** built-in classes.

#### Functional Requirements

* Applicable only to the sub classes of a specific class implementing the data encapsulation
* On the basic level only attributes with names starting with a single underscore (‘_’) are considered to be inherently ‘private’, ‘magic’ fields / methods (with starting and tailing double underscores) are considered to be ‘public’
* On the more advanced level implemented in a sub class of the basic encapsulation class instance data attributes (fields) mentioned by their name in the specific look-up class attributes are considered ‘private’ or ‘protected’ or ‘public’ regardless of their names
* Any access to the ‘private’ attributes must be denied either using the dot notation of the built-in **getattr**() and **setattr**() functions
* For the ‘protected’ attributes only the read access must be allowed
* On that advanced level the ‘private’, ‘protected’ and ‘public’ look-up attributes can define either a name of an attribute to be taken under access control or also the limitations on the values / data type allowed, i.e. combined with the forced data check

### Simplified Call Chain Traceback

The idea is to obtain a snapshot of the call stack from the top level of the interpreter loop to the point when the call stack is obtained. This traceback is to be stored in an instance of a special class, which provides methods or properties to analyse the traceback: 1) list of the fully qualified named of the callers along the call chain, and 2) human readable representation of the entire traceback including the source code fragments. The traceback of an exception is a specialized sub-class of that one, which obtains the traceback of the call chain ended in the last raised exception instead as a list of frame records between the exception handling frame and the frame, where it has been raised.

References for the baseline of the implementation are: <a id="bref7">[<sup>7</sup>](#aref7)</a>, <a id="bref8">[<sup>8</sup>](#aref8)</a>, <a id="bref9">[<sup>9</sup>](#aref9)</a> and <a id="bref10">[<sup>10</sup>](#aref10)</a>

#### Functional Requirements

* The traceback of the current stack or the traceback of the last raised exception are stored as instances of the special classes, which are responsible for the analysis of the corresponding traceback
* These classes should allow removal of the specified number of the deepest (inner) frames from the traceback
* These classes should allow specification on how many lines of the source code is to obtain and show around the one, where a call is made
* These classes must resolve the fully qualified names of the callers, i.e. including the corresponding module’s name and the class’ name in the case of the methods
* These classes must implement functionality for the retrieval of the caller’s chain as a list of the fully qualified names as well as the human-readable string representation of the entire traceback, including fully qualified name of the caller, path to the module and line number where the call has occurred as well as a portion of the source code around that line with a clear indication of the position of that line

### Unified Custom Exceptions Scheme

The custom defined exceptions are to be raised in the cases when either the input or output data of a function / method doesn’t satisfy the DbC limitations, or a contract is wrongly defined, or an attribute access violates the data encapsulation – basically, the restrictions applied by the new functionality are violated even though the code or data may be perfectly valid in the ‘vanilla’ Python. Thus those exceptions must be clearly distinguishable from the standard error. On the other hand, their intended use cases are specialized case of the standard error situation, therefore they must be consider sub-classes of the corresponding standard errors. Finally, they must provide simple interface for the analysis of their traceback.

#### Functional Requirements

* The custom exceptions must be sub-classes (direct or indirect) of the specific standard exceptions
* These classes must resolve the fully qualified names of the callers, i.e. including the corresponding module’s name and the class’ name in the case of the methods
* These classes must implement functionality for the retrieval of the caller’s chain as a list of the fully qualified names as well as the human-readable string representation of the entire traceback, including fully qualified name of the caller, path to the module and line number where the call has occurred as well as a portion of the source code around that line with a clear indication of the position of that line
* These classes should allow removal of the specified number of the deepest (inner) frames from the traceback
* These classes should allow replacement of their actual traceback by another traceback object, thus the exception may be re-raised or another exception may be raised instead within the exception handler after some processing preserving the traceback of the original exception
* These exception classes must support virtual sub-classes concept, so some more generic exceptions can be used as an ‘umbrella’ term for a group of more specialized exceptions even if these specialized exceptions are not direct or indirect sub classes of those generic ones
* The relation between the built-in and custom defined exceptions show be as given in [Illustration 1](#ill1), with the real sub-classes (direct or indirect) shown in bold with a star symbol, and the virtual sub-classes are given in italic with a link symbol. Reference for the implementaion - virtual inheritance <a id="bref11">[<sup>11</sup>](#aref11)</a>.

<a id="ill1">**Illustration 1**</a>

![Illustration 1](../UML/Miscellaneous/custom_exceptions_tree.png)

## References

<a id="aref1">[1]</a> https://en.wikipedia.org/wiki/Design_by_contract     [&#x2B0F;](#bref1)

<a id="aref2">[2]</a> https://www.thecodeship.com/patterns/guide-to-python-function-decorators/    [&#x2B0F;](#bref2)

<a id="aref3">[3]</a> https://www.codementor.io/sheena/advanced-use-python-decorators-class-function-du107nxsv     [&#x2B0F;](#bref3)

<a id="aref4">[4]</a> https://blog.apcelent.com/python-decorator-tutorial-with-example.html    [&#x2B0F;](#bref4)

<a id="aref5">[5]</a> https://docs.python.org/2/howto/descriptor.html      [&#x2B0F;](#bref5)

<a id="aref6">[6]</a> https://docs.python.org/2/reference/datamodel.html   [&#x2B0F;](#bref6)

<a id="aref7">[7]</a> https://docs.python.org/2/library/sys.html   [&#x2B0F;](#bref7)

<a id="aref8">[8]</a> https://docs.python.org/2/library/traceback.html     [&#x2B0F;](#bref8)

<a id="aref9">[9]</a> https://docs.python.org/2/library/inspect.html     [&#x2B0F;](#bref9)

<a id="aref10">[10]</a> https://www.programcreek.com/python/example/1190/inspect.currentframe      [&#x2B0F;](#bref10)

<a id="aref11">[11]</a> https://docs.python.org/2/library/abc.html   [&#x2B0F;](#bref11)