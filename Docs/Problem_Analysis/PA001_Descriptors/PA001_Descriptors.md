# PA001 Problem Analysis on Usage of Descriptors for Implementation of Design by Contract

## Introduction

The input data sanity checks (as in type, range, etc.) as a part of Design by Contract can be easily implemented within the body of functions thus class / instance methods. In the case of the data attributes (as fields) the same effect can be achieved by hooking the attribute access, namely the special methods **\_\_getattribute\_\_**() and **\_\_setattr\_\_**(). The drawback of such approach is that the class must be aware of the expected types and ranges of values of all relevant data attributes, for instance, by maintaining some sort of ‘template’, as it is done with the Standard Python Library module _**ctypes**_.

On the other hand, the task of the input data sanity check can be delegated to the objects themselves, stored as attributes of their ‘parent’ object, provided that the data retrieval and update happen through the special getter / setter methods of the said classes. Since release 2.2 Python provides descriptors protocol, which serves exactly this purpose.
Unfortunately, use of descriptors is not the universal way of the attributes resolution, and it has its own ‘underwater stones’, and I do not have any prior experience with them. Although there are many ‘guides’ available on-line, the majority of them is simply re-written in mostly own words ‘Descriptors HOWTO’ page from the CPython documentation <a id="bref1">[<sup>^1</sup>](#aref1)</a>. Therefore this problem analysis research is performed.

## Method and Results

We begin with the slightly modified ‘text-book’ example from the ‘Descriptors HOWTO’ [<sup>^1</sup>](#aref1). Thus, a class implementing the getter and setter descriptors (**DescriptorClass**) and its user class (**TestClass**) are created, see below.

[pa001_descriptors_test01.py](./pa001_descriptors_test01.py)

```python
#!/usr/bin/python

class DescriptorClass(object):
    
    def __init__(self, strName, gValue):
        print 'Initializing {} with {} value'.format(strName, gValue)
        self.Name = strName
        self.Value = gValue
    
    def __get__(self, obj, objType = None):
        if obj is None:
            strName = 'not an instance (None)'
        else:
            strName = 'instance id = {}'.format(id(obj))
        print 'Read access to {} by {} of {}'.format(self.Name, strName,
                                                            objType.__name__)
        return self.Value
    
    def __set__(self, obj, gValue):
        if obj is None:
            strName = 'not an instance (None)'
        else:
            strName = 'instance id = {}'.format(id(obj))
        print 'Updating {} with value {} requested by {} of {}'.format(
                            self.Name, gValue, strName, obj.__class__.__name__)
        self.Value = gValue

class TestClass(object):
    
    #class attributes
    
    A = DescriptorClass('class attribute', 1)

#testing area

objTest1 = TestClass()
objTest2 = TestClass()
print objTest1.A
print objTest2.A
objTest1.A = 2
print objTest1.A
print objTest2.A
```

**output**

```bash
Initializing class attribute with 1 value
Read access to class attribute by instance id = 37453384 of TestClass
1
Read access to class attribute by instance id = 37499512 of TestClass
1
Updating class attribute with value 2 requested by instance id = 37453384 of TestClass
Read access to class attribute by instance id = 37453384 of TestClass
2
Read access to class attribute by instance id = 37499512 of TestClass
2
```

Two instances of the user class are created and used in the test. Only a single instance of the **DescriptorClass** is created, as it should be for a class attribute **TestClass.A**, access to which from the instances of the **TestClass** is indeed occur through the defined getter and setter descriptors. Furthermore, the change of the state of the class attribute made by one instance is visible to the second instance, as it should be.

However, the instance data attributes are usually more often used, since they keep the state of an individual object, not their collective / common state as the class data attributes do. So, in the next test the initialization method is added to the user class **TestClass**, which creates an instance attribute as an instance of the **DescriptorClass**. In the listing below only the changes in the code are shown.

[pa001_descriptors_test02.py](./pa001_descriptors_test02.py)

```python
…
class TestClass(object):
    
    #class attributes
    
    A = DescriptorClass('class attribute', 1)
    
    def __init__(self):
        self.B = DescriptorClass('instance attribute', 1)

#testing area

objTest1 = TestClass()
objTest2 = TestClass()
print objTest1.A
print objTest2.A
print objTest1.B
print objTest2.B
objTest1.A = 2
print objTest1.A
print objTest2.A
objTest1.B = 2
print objTest1.B
print objTest2.B
```

**output**

```bash
Initializing class attribute with 1 value
Initializing instance attribute with 1 value
Initializing instance attribute with 1 value
Read access to class attribute by instance id = 37322312 of TestClass
1
Read access to class attribute by instance id = 37368664 of TestClass
1
<__main__.DescriptorClass object at 0x00000000023A3278>
<__main__.DescriptorClass object at 0x00000000023A3390>
Updating class attribute with value 2 requested by instance id = 37322312 of TestClass
Read access to class attribute by instance id = 37322312 of TestClass
2
Read access to class attribute by instance id = 37368664 of TestClass
2
2
<__main__.DescriptorClass object at 0x00000000023A3390>
```

Apparently, the getter and setter methods of the descriptor class are not called on the instance attributes **objTest1.B** and **objTest2.B**. Furthermore, the last assignment clearly overwrites the reference stored as **objTest1.B** instance attribute.
In fact, this effect is briefly mentioned in the official ‘HOWTO’ during the discussion of the resolution order, something about that instance dictionary overrules the descriptors.

So, the solution is to hook the attributes resolution on the instance of the user class level, i.e. the special methods **\_\_getattribute\_\_**() and **\_\_setattr\_\_**().

The trick is to, at first, get the reference to an instance of the descriptor class stored as an instance data attribute using the ‘original’ **\_\_getattribute\_\_**() version of the super class (in this example, the direct call to the corresponding method of the super class **object** is made instead of using **super**() function). Secondly, to check if the found object provides descriptors interface. If the required descriptor is present, the data retrieval or state update proceed through the corresponding descriptor methods, otherwise the found object is returned directly or the value is assigned to it directly. The last trick implemented in the **\_\_setattr\_\_**() method is to create the instance attribute with the passed  name if it is not yet present. Thanks to this approach there is no need to change the initialization method, otherwise meddling with the instance dictionary is required.

Again, in the listing below only the changes in the code are shown.

[pa001_descriptors_test03.py](./pa001_descriptors_test03.py)

```python
…
class TestClass(object):
…
def __getattribute__(self, strAttr):
        objOwner = object.__getattribute__(self, '__class__')
        objTemp = object.__getattribute__(self, strAttr)
        print 'In instance __getattribute__() getting {}'.format(strAttr)
        if hasattr(objTemp, '__get__'):
            print 'via descriptor'
            objResult = objTemp.__get__(self, objOwner)
        else:
            print 'directly'
            objResult = objTemp
        return objResult
    
    def __setattr__(self, strAttr, gValue):
        objOwner = object.__getattribute__(self, '__class__')
        print 'In instance __setattr__() setting {}'.format(strAttr)
        try:
            objTemp = object.__getattribute__(self, strAttr)
            if hasattr(objTemp, '__set__'):
                print 'via descriptor'
                objTemp.__set__(self, gValue)
            else:
                print 'directly'
                objTemp = gValue
        except AttributeError:
            # doesn't exist yet
            print 'creating instance attribute {}'.format(strAttr)
            object.__setattr__(self, strAttr, gValue)
```

**output**

```bash
Initializing class attribute with 1 value
Initializing instance attribute with 3 value
In instance __setattr__() setting B
creating instance attribute B
Read access to class attribute by instance id = 37892952 of TestClass
In instance __getattribute__() getting A
directly
1
In instance __getattribute__() getting B
via descriptor
Read access to instance attribute by instance id = 37892952 of TestClass
3
In instance __setattr__() setting A
Read access to class attribute by instance id = 37892952 of TestClass
directly
Read access to class attribute by instance id = 37892952 of TestClass
In instance __getattribute__() getting A
directly
1
In instance __setattr__() setting B
via descriptor
In instance __getattribute__() getting __class__
directly
Updating instance attribute with value 4 requested by instance id = 37892952 of TestClass
In instance __getattribute__() getting B
via descriptor
Read access to instance attribute by instance id = 37892952 of TestClass
4
```

The implemented patch does work with a single instance. The next test checks if the shared (class data attributes) and the individual states (instance data attributes) are preserved and function as expected with several instances of the user class. (Only few lines are added in the testing area, as given in the listing below.)

[pa001_descriptors_test04.py](./pa001_descriptors_test04.py)

```python
…
#testing area

objTest1 = TestClass()
objTest2 = TestClass()
print objTest1.A
print objTest1.B
print objTest2.A
print objTest2.B
objTest1.A = 2
print objTest1.A
objTest1.B = 4
print objTest1.B
print objTest2.A
print objTest2.B
```

**output**

```bash
Initializing class attribute with 1 value
Initializing instance attribute with 3 value
In instance __setattr__() setting B
creating instance attribute B
Initializing instance attribute with 3 value
In instance __setattr__() setting B
creating instance attribute B
Read access to class attribute by instance id = 37630584 of TestClass
In instance __getattribute__() getting A
directly
1
In instance __getattribute__() getting B
via descriptor
Read access to instance attribute by instance id = 37630584 of TestClass
3
Read access to class attribute by instance id = 37630864 of TestClass
In instance __getattribute__() getting A
directly
1
In instance __getattribute__() getting B
via descriptor
Read access to instance attribute by instance id = 37630864 of TestClass
3
In instance __setattr__() setting A
Read access to class attribute by instance id = 37630584 of TestClass
directly
Read access to class attribute by instance id = 37630584 of TestClass
In instance __getattribute__() getting A
directly
1
In instance __setattr__() setting B
via descriptor
In instance __getattribute__() getting __class__
directly
Updating instance attribute with value 4 requested by instance id = 37630584 of TestClass
In instance __getattribute__() getting B
via descriptor
Read access to instance attribute by instance id = 37630584 of TestClass
4
Read access to class attribute by instance id = 37630864 of TestClass
In instance __getattribute__() getting A
directly
1
In instance __getattribute__() getting B
via descriptor
Read access to instance attribute by instance id = 37630864 of TestClass
3
```

As can be seen from the output, this patch does fix the descriptor class instance as an instance attribute of another class issue without breaking the shared and individual objects states paradigm.

Now, what happens when one accesses such descriptor class instance as a class attribute of another class without instantiation of the user class? (Only few lines are added in the testing area, as given in the listing below; only the new part of the output is provided as well.)

[pa001_descriptors_test05.py](./pa001_descriptors_test05.py)

```python
…
print TestClass.A
TestClass.A = 6
print TestClass.A
```

**output**

```bash
…
Read access to class attribute by not an instance (None) of TestClass
1
6
```

The result is that without instantiation the getter descriptor (**\_\_get\_\_**()) is called, whereas the getter descriptor is not called. Also note that the calling object (second attribute of the **\_\_get\_\_**() descriptor) is None.

In order to fix this issue a metaclass **TestClassMeta** is added for the user class **TestClass**, which hooks the assignment attribute resolution on the user class without its instantiation. See the changes in the code given in the listing below. The **\_\_setattr\_\_**() method of the metaclass is implemented almost identically to the same named method of the user class except for calling the methods of the **type** instead of **object**.

[pa001_descriptors_test06.py](./pa001_descriptors_test06.py)

```python
…
class TestClassMeta(type):
    
    def __setattr__(self, strAttr, gValue):
        objOwner = type.__getattribute__(self, '__class__')
        print 'In metaclass __setattr__() setting {}'.format(strAttr)
        try:
            objTemp = type.__getattribute__(self, strAttr)
            if hasattr(objTemp, '__set__'):
                print 'via descriptor'
                objTemp.__set__(self, gValue)
            else:
                print 'directly'
                objTemp = gValue
        except AttributeError:
            # doesn't exist yet
            print 'creating class attribute {}'.format(strAttr)
            type.__setattr__(self, strAttr, gValue)

class TestClass(object):
    
    #class attributes
    
    __metaclass__ = TestClassMeta
…
```

**output**

```bash
…
Read access to class attribute by not an instance (None) of TestClass
1
In metaclass __setattr__() setting A
Read access to class attribute by not an instance (None) of TestClass
directly
Read access to class attribute by not an instance (None) of TestClass
1
```

Clearly, the assignment is hooked but the corresponding setter descriptor method is not called. The problem is with the **type.\_\_getattribute\_\_**() method, which works differently from the **object.\_\_getattribute\_\_**() method (also mentioned in the official ‘HOWTO’, although without an explanation). The solution is to look-up the reference to the descriptor class stored in the call attribute directly in the class dictionary instead of relying upon the **type.\_\_getattribute\_\_**() method. Again, only the relevant changes are given in the listing below.

[pa001_descriptors_test07.py](./pa001_descriptors_test07.py)

```python
…
class TestClassMeta(type):
    
    def __setattr__(self, strAttr, gValue):
        objOwner = type.__getattribute__(self, '__class__')
        dictVars = type.__getattribute__(self, '__dict__')
        print 'In metaclass __setattr__() setting {}'.format(strAttr)
        if strAttr in dictVars.keys():
            objTemp = dictVars[strAttr]
            if hasattr(objTemp, '__set__'):
                print 'via descriptor'
                objTemp.__set__(self, gValue)
            else:
                print 'directly'
                objTemp = gValue
        else:
            # doesn't exist yet
            print 'creating class attribute {}'.format(strAttr)
            type.__setattr__(self, strAttr, gValue)
```

**output**

```bash
…
Read access to class attribute by not an instance (None) of TestClass
1
In metaclass __setattr__() setting A
via descriptor
Updating class attribute with value 6 requested by instance id = 38813352 of TestClassMeta
Read access to class attribute by not an instance (None) of TestClass
6
```

The fix definitely works, but it uses the lookup in the dictionary of the current class. Therefore this fix will break for the children (derived classes) of the user class. The final fix is to look up the reference in all super (parent) classes along the MRO route of a class and to stop as soon as the required attribute is found. If such attribute is not found in any of the classes along the MRO route, it must be created in the dictionary of the calling class. This approach insures proper assignment resolution of the inherited data attrbutes.

Note, the listing below is the full test script!

[pa001_descriptors_test08.py](./pa001_descriptors_test08.py) - final version!

```python
#!/usr/bin/python

class DescriptorClass(object):
    
    def __init__(self, strName, gValue):
        print 'Initializing {} with {} value'.format(strName, gValue)
        self.Name = strName
        self.Value = gValue
    
    def __get__(self, obj, objType = None):
        if obj is None:
            strName = 'not an instance (None)'
        else:
            strName = 'instance id = {}'.format(id(obj))
        print 'Read access to {} by {} of {}'.format(self.Name, strName,
                                                            objType.__name__)
        return self.Value
    
    def __set__(self, obj, gValue):
        if obj is None:
            strName = 'not an instance (None)'
        else:
            strName = 'instance id = {}'.format(id(obj))
        print 'Updating {} with value {} requested by {} of {}'.format(
                            self.Name, gValue, strName, obj.__class__.__name__)
        self.Value = gValue

class TestClassMeta(type):
    
    def __setattr__(self, strAttr, gValue):
        objOwner = type.__getattribute__(self, '__class__')
        lstMRO = type.__getattribute__(self, '__mro__')
        print 'In metaclass __setattr__() setting {}'.format(strAttr)
        for objTemp in lstMRO:
            dictVars = type.__getattribute__(objTemp, '__dict__')
            if strAttr in dictVars.keys():
                objTemp = dictVars[strAttr]
                if hasattr(objTemp, '__set__'):
                    print 'via descriptor'
                    objTemp.__set__(self, gValue)
                else:
                    print 'directly'
                    objTemp = gValue
                break
        else:
            # doesn't exist yet
            print 'creating class attribute {}'.format(strAttr)
            type.__setattr__(self, strAttr, gValue)

class TestClass(object):
    
    #class attributes
    
    __metaclass__ = TestClassMeta
    
    A = DescriptorClass('class attribute', 1)
    
    def __init__(self):
        self.B = DescriptorClass('instance attribute', 3)
    
    def __getattribute__(self, strAttr):
        objOwner = object.__getattribute__(self, '__class__')
        objTemp = object.__getattribute__(self, strAttr)
        print 'In instance __getattribute__() getting {}'.format(strAttr)
        if hasattr(objTemp, '__get__'):
            print 'via descriptor'
            objResult = objTemp.__get__(self, objOwner)
        else:
            print 'directly'
            objResult = objTemp
        return objResult
    
    def __setattr__(self, strAttr, gValue):
        objOwner = object.__getattribute__(self, '__class__')
        print 'In instance __setattr__() setting {}'.format(strAttr)
        try:
            objTemp = object.__getattribute__(self, strAttr)
            if hasattr(objTemp, '__set__'):
                print 'via descriptor'
                objTemp.__set__(self, gValue)
            else:
                print 'directly'
                objTemp = gValue
        except AttributeError:
            # doesn't exist yet
            print 'creating instance attribute {}'.format(strAttr)
            object.__setattr__(self, strAttr, gValue)

class ChildTestClass(TestClass):
    
    #simple inheritance
    
    pass

#testing area

objTest1 = TestClass()
objTest2 = ChildTestClass()
print objTest1.A
print objTest1.B
print objTest2.A
print objTest2.B
objTest1.A = 2
print objTest1.A
objTest1.B = 4
print objTest1.B
print objTest2.A
print objTest2.B
print TestClass.A
TestClass.A = 6
print TestClass.A
print ChildTestClass.A
ChildTestClass.A = 8
print ChildTestClass.A
print objTest1.A
print objTest1.B
print objTest2.A
print objTest2.B
```

**output**

```bash
Initializing class attribute with 1 value
Initializing instance attribute with 3 value
In instance __setattr__() setting B
creating instance attribute B
Initializing instance attribute with 3 value
In instance __setattr__() setting B
creating instance attribute B
Read access to class attribute by instance id = 37237648 of TestClass
In instance __getattribute__() getting A
directly
1
In instance __getattribute__() getting B
via descriptor
Read access to instance attribute by instance id = 37237648 of TestClass
3
Read access to class attribute by instance id = 37237872 of ChildTestClass
In instance __getattribute__() getting A
directly
1
In instance __getattribute__() getting B
via descriptor
Read access to instance attribute by instance id = 37237872 of ChildTestClass
3
In instance __setattr__() setting A
Read access to class attribute by instance id = 37237648 of TestClass
directly
Read access to class attribute by instance id = 37237648 of TestClass
In instance __getattribute__() getting A
directly
1
In instance __setattr__() setting B
via descriptor
In instance __getattribute__() getting __class__
directly
Updating instance attribute with value 4 requested by instance id = 37237648 of TestClass
In instance __getattribute__() getting B
via descriptor
Read access to instance attribute by instance id = 37237648 of TestClass
4
Read access to class attribute by instance id = 37237872 of ChildTestClass
In instance __getattribute__() getting A
directly
1
In instance __getattribute__() getting B
via descriptor
Read access to instance attribute by instance id = 37237872 of ChildTestClass
3
Read access to class attribute by not an instance (None) of TestClass
1
In metaclass __setattr__() setting A
via descriptor
Updating class attribute with value 6 requested by instance id = 36998408 of TestClassMeta
Read access to class attribute by not an instance (None) of TestClass
6
Read access to class attribute by not an instance (None) of ChildTestClass
6
In metaclass __setattr__() setting A
via descriptor
Updating class attribute with value 8 requested by instance id = 36999352 of TestClassMeta
Read access to class attribute by not an instance (None) of ChildTestClass
8
Read access to class attribute by instance id = 37237648 of TestClass
In instance __getattribute__() getting A
directly
8
In instance __getattribute__() getting B
via descriptor
Read access to instance attribute by instance id = 37237648 of TestClass
4
Read access to class attribute by instance id = 37237872 of ChildTestClass
In instance __getattribute__() getting A
directly
8
In instance __getattribute__() getting B
via descriptor
Read access to instance attribute by instance id = 37237872 of ChildTestClass
3
```

As can be seen from the output, the entire scope of the implemented functionality matches the expected / desired behaviour pattern.

## Conclusion

In order to ensure the usage of the defined getter and setter descriptors by the user class with or without its instantiation as well as on the instance and class attributes of an instance of the user class the following measures are required:

* Hooking into the attributes resolution by an instance of the user class by means of the custom special methods **\_\_getattribute\_\_**() and **\_\_setattr\_\_**() - fixes the descriptors usage on the instance attributes
* Hooking into attributes resolution during assignment to the class attribute without instantiation of the user class – custom special method **\_\_setattr\_\_**() of the metaclass of the user class – fixes assignment to a class attribute without instantiation of the user class
* The method above must perform direct look-up of the required class attribute in the class dictionaries of the user class and its super classes (if the attribute is inherited) using the MRO instead of using the ‘original’ **type.\_\_getattribute\_\_**() method – fixes inheritance issue

## References

<a id="aref1">[^1]</a> https://docs.python.org/2/howto/descriptor.html      [&#x2B0F;](#bref1)