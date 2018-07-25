#usr/bin/python
"""
Module pos.tests.base_classes_descriptedabc_ut

Implements unit testing of the module base_classes concerning the class
DescriptedABC.
"""

__version__ = "0.0.1.3"
__date__ = "23-07-2018"
__status__ = "Testing"

#imports

#+ standard libraries

import sys
import unittest
import inspect

#+ my libraries

import pos.base_classes as testmodule

#helper functions

def MyAbs(gValue):
    """
    Alias for abs() built-in function
    """
    return abs(gValue)

#classes

#+ helper classes

class IntegerDescriptor(object):
    """
    Imitates an integer number
    """
    
    def __init__(self, gValue):
        """
        Stores as integer the integer part of the the passed numeric argument.
        """
        self.Value = int(gValue)
    
    def __get__(self, objInstance, clsOwner):
        """
        Simply returns the stored value.
        """
        return self.Value
    
    def __set__(self, objInstance, gValue):
        """
        Converts the second (numeric) argument into an integer and stores it.
        """
        self.Value = int(gValue)

class FloatDescriptor(object):
    """
    Imitates a floating point number
    """
    
    def __init__(self, gValue):
        """
        Stores as floating point number the passed numeric argument.
        """
        self.Value = float(gValue)
    
    def __get__(self, objInstance, clsOwner):
        """
        Simply returns the stored value.
        """
        return self.Value
    
    def __set__(self, objInstance, gValue):
        """
        Converts the second (numeric) argument into a float type and stores it.
        """
        self.Value = float(gValue)

class ConstIntegerDescriptor(IntegerDescriptor):
    """
    Imitates a constant integer number
    """
    
    def __set__(self, objInstance, gValue):
        """
        Raises AttributeError upon attempted assignment.
        """
        raise AttributeError
    
    def __delete__(self, objInstance):
        """
        Raises AttributeError upon attempted deletion.
        """
        raise AttributeError

class ConstFloatDescriptor(FloatDescriptor):
    """
    Imitates a constant floating point number
    """
    
    def __set__(self, objInstance, gValue):
        """
        Raises AttributeError upon attempted assignment.
        """
        raise AttributeError
    
    def __delete__(self, objInstance):
        """
        Raises AttributeError upon attempted deletion.
        """
        raise AttributeError

class ClassTest1(testmodule.DescriptedABC):
    """
    Abstract sub-class of pos.base_classes.DescriptedABC. Defines class fields
    with the descriptors.
    """
    
    #class fields
    
    ClassInt = IntegerDescriptor(2.5)
    
    ClassConstFloat = ConstFloatDescriptor(1)
    
    ClassSimpleInt = 2
    
    _ClassHidden = 2
    
    #properties
    
    @property
    def RO_String(self):
        """
        Read only property, returns same string
        """
        return 'test_ro'
    
    @property
    def RW_String(self):
        """
        Getter property, returns a string, which is stored in a 'private'
        instance attribute '_string1'
        """
        return self._string1
    
    @RW_String.setter
    def RW_String(self, strString):
        """
        Setter property, stores the passed string in the 'private' instance
        attribute '_string1'
        """
        self._string1 = strString
    
    @property
    def RWD_String(self):
        """
        Getter property, returns a string, which is stored in a 'private'
        instance attribute '_string2'
        """
        return self._string2
    
    @RWD_String.setter
    def RWD_String(self, strString):
        """
        Setter property, stores the passed string in the 'private' instance
        attribute '_string2'
        """
        self._string2 = strString
    
    @RWD_String.deleter
    def RWD_String(self):
        """
        Sets the 'private' instance attribute '_string2' to 'deleted' value.
        """
        self._string2 = 'deleted'
    
    #class / static methods
    
    @classmethod
    def TestClassMethod(cls):
        """
        Simply returns a string
        """
        return 'test_class_method'
    
    @classmethod
    def _TestClassHiddenMethod(cls):
        """
        Simply returns a string
        """
        return 'test_class_hidden_method'
    
    @staticmethod
    def TestStaticMethod():
        """
        Simply returns a string
        """
        return 'test_static_method'
    
    @staticmethod
    def _TestStaticHiddenMethod():
        """
        Simply returns a string
        """
        return 'test_static_hidden_method'
    
    #instance methods
    
    def TestMethod(self):
        """
        Simply returns a string
        """
        return 'test_method'
    
    def _TestHiddenMethod(self):
        """
        Simply returns a string
        """
        return 'test_hidden_method'

class ClassTest2(ClassTest1):
    """
    Sub-class of ClassTest1 -|> pos.base_classes.DescriptedABC. No longer
    abstract. Defines instance attributes as data descriptors.
    """
    
    def onInit(self, *args, **kwargs):
        """
        Overrides the abstract method of the super class. Creates the instance
        attributes.
        """
        self.InstFloat = FloatDescriptor(3)
        self.InstConstInt = ConstIntegerDescriptor(4.0)
        self.SimpleInt = 5
        self._string1 = 'test_rw'
        self._string2 = 'test_rwd'
        self.funcAbs = MyAbs
        self.funcAbsBuiltin = abs

class ClassTest3(ClassTest2):
    """
    Sub-class of ClassTest2 -|> ClassTest1 -|> pos.base_classes.DescriptedABC.
    No longer abstract. Defines instance attributes as data descriptors by
    extending the super class onInit() method, but changes its signature.
    """
    
    def onInit(self):
        """
        Simply calls the same method of the super class. However, the signature
        is changed: no positional or keyword arguments are allowed to be passed
        into the initialization method any longer.
        """
        super(ClassTest3, self).onInit()

#+ test cases

class Test_DescriptedABC(unittest.TestCase):
    """
    Test cases for the class pos.base_classes.DescriptedABC
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        cls.TestClass = testmodule.DescriptedABC
        cls.PublicClassFields = []
        cls.PublicClassMethods = list(sorted(['getClassFields',
                                                'getClassMethods',
                                                'inspectClassAttribute']))
        cls.DirList = list(sorted(cls.PublicClassMethods + cls.PublicClassFields
                                    + ['getFields', 'getMethods']))
    
    def test_IsAbstract(self):
        """
        Checks that the test class cannot be instantiated, i.e. it is abstract.
        """
        with self.assertRaises(TypeError):
            self.TestClass()
    
    def test_getClassFields(self):
        """
        Checks that the class method getClassFields() returns a sorted list of
        all 'public' class fields.
        """
        self.assertEqual(self.TestClass.getClassFields(),
                                                        self.PublicClassFields)
    
    def test_getClassMethods(self):
        """
        Checks that the class method getClassFields() returns a sorted list of
        all 'public' class methods.
        """
        self.assertEqual(self.TestClass.getClassMethods(),
                                                        self.PublicClassMethods)
    
    def test_dirClass(self):
        """
        Checks that the built-in function dir() returns the proper list of the
        names of ALL 'public' attributes visible at the class level.
        """
        strlstTest = dir(self.TestClass)
        self.assertEqual(strlstTest, self.DirList)

class Test_ClassTest1(Test_DescriptedABC):
    """
    Test cases for the class ClassTest1 derived from the
    pos.base_classes.DescriptedABC - must remain abstract, but inherit the
    support for the descriptors for the class fields.
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        cls.TestClass = ClassTest1
        cls.SecondClass = ClassTest2
        cls.ClassFields = [['ClassInt', int, IntegerDescriptor],
                           ['ClassConstFloat', float, ConstFloatDescriptor],
                           ['ClassSimpleInt', int, int],
                           ['_ClassHidden', int, int]]
        cls.ConstantClassFields = ['ClassConstFloat']
        cls.Getters = [['RO_String', 'test_ro', str, property],
                        ['RW_String', 'test_rw', str, property],
                        ['RWD_String', 'test_rwd', str, property]]
        cls.Setters = ['RW_String', 'RWD_String']
        cls.Deleters = ['RWD_String']
        cls.StaticMethods = [['TestStaticMethod', str, 'test_static_method'],
                             ['_TestStaticHiddenMethod', str,
                              'test_static_hidden_method']]
        cls.ClassMethods = [['TestClassMethod', str, 'test_class_method'],
                            ['_TestClassHiddenMethod', str,
                            'test_class_hidden_method']]
        cls.Methods = [['TestMethod', str, 'test_method'],
                       ['_TestHiddenMethod', str, 'test_hidden_method']]
        cls.PublicClassFields = list(sorted(['ClassInt', 'ClassConstFloat',
                                             'ClassSimpleInt']))
        cls.PublicClassMethods = list(sorted(['getClassFields',
                                                'getClassMethods',
                                                'inspectClassAttribute',
                                                'TestClassMethod',
                                                'TestStaticMethod']))
        cls.DirList = list(sorted(cls.PublicClassMethods + cls.PublicClassFields
                                    + ['getFields', 'getMethods', 'TestMethod']
                                    + [Item[0] for Item in cls.Getters]))
    
    def test_HasClassFields(self):
        """
        Checks that all expected class fields are present in the class.
        """
        for strAttr, _, _ in self.ClassFields:
            strError = 'Missing attribute {} in class {}'.format(strAttr,
                                                    self.TestClass.__name__)
            self.assertTrue(hasattr(self.TestClass, strAttr), strError)
        strAttr = 'foo_bar_shebang'
        strError = 'Attribute {} should not be in class {}'.format(strAttr,
                                                    self.TestClass.__name__)
        self.assertFalse(hasattr(self.TestClass, strAttr), strError)
    
    def test_TypeClassFields(self):
        """
        Checks that all expected class fields in the class are returned as the
        expected types (via descriptors protocol).
        """
        for strAttr, typType, _ in self.ClassFields:
            strError = ' '.join(['Type of attribute', strAttr, 'in class',
                                self.TestClass.__name__, 'is',
                                str(type(getattr(self.TestClass, strAttr))),
                                'instead of', str(typType)])
            self.assertIsInstance(getattr(self.TestClass, strAttr), typType,
                                                                    strError)
    
    def test_InnerTypeClassFields(self):
        """
        Checks that all expected class fields in the class are internally stored
        as references to the instances of the specific classes.
        """
        for strAttr, _, typType in self.ClassFields:
            objData = None
            for clsParent in self.TestClass.__mro__:
                if strAttr in clsParent.__dict__:
                    objData = clsParent.__dict__[strAttr]
                    break
            strError = ' '.join(['Inner type of attribute', strAttr, 'in class',
                                self.TestClass.__name__, 'is',
                                str(type(objData)), 'instead of', str(typType)])
            self.assertIsInstance(objData, typType, strError)
    
    def test_DeleteClassFields(self):
        """
        Checks that the class fields with the descriptors can be deleted unless
        they raise an AttributeError in the __set__() descriptor or they are
        not defined in this class but are inherited from its super class. The
        AttributeError should also be raised if a non-existent class attribute
        is to be deleted.
        """
        for strAttr, _, typType in self.ClassFields:
            if strAttr in self.TestClass.__dict__: #must be directly in
            #the class, not inherited!
                if not (strAttr in self.ConstantClassFields):
                    gOldValue = getattr(self.TestClass, strAttr)
                    delattr(self.TestClass, strAttr)
                    strError = ' '.join(['Attribute', strAttr, 'of class',
                                     self.TestClass.__name__, 'is not deleted'])
                    self.assertFalse(hasattr(self.TestClass, strAttr), strError)
                    #restore the class field
                    setattr(self.TestClass, strAttr, typType(gOldValue))
                    strError = ' '.join(['Attribute', strAttr, 'of class',
                                     self.TestClass.__name__, 'is not set',
                                     'to the proper value'])
                    self.assertTrue(hasattr(self.TestClass, strAttr), strError)
                    objData = self.TestClass.__dict__[strAttr]
                    strError = ' '.join(['Inner type of attribute', strAttr,
                                         'in class', self.TestClass.__name__,
                                         'is', str(type(objData)), 'instead of',
                                         str(typType)])
                    self.assertIsInstance(objData, typType, strError)
                else: #go through __delete__() descriptor
                    with self.assertRaises(AttributeError):
                        delattr(self.TestClass, strAttr)
            else: #not in the class itself, inherited!
                with self.assertRaises(AttributeError):
                    delattr(self.TestClass, strAttr)
        with self.assertRaises(AttributeError): #non-existent attribute
            delattr(self.TestClass, 'foo_bar_shebang')
    
    def test_SetClassFields(self):
        """
        Checks that the class fields with the descriptors can be set unless
        they raise an AttributeError in the __set__() descriptor
        """
        for strAttr, _, typType in self.ClassFields:
            gOldValue = getattr(self.TestClass, strAttr)
            gNewValue = gOldValue + 1
            if not (strAttr in self.ConstantClassFields):
                strErrorValue = ' '.join(['Attribute', strAttr, 'of class',
                                     self.TestClass.__name__, 'is not set',
                                     'to the proper value'])
                setattr(self.TestClass, strAttr, gNewValue)
                self.assertEqual(getattr(self.TestClass, strAttr), gNewValue,
                                    strErrorValue)
                strError = ' '.join(['Attribute', strAttr, 'is a shared',
                                     'state between super and subclass'])
                if issubclass(self.TestClass, self.SecondClass):
                    self.assertNotEqual(getattr(self.TestClass, strAttr),
                            getattr(self.SecondClass, strAttr), strError)
                    #change of the class field of the subclass should not affect
                    #the same field of the super class - otherwise, the behavior
                    #is not defined - depends on the events sequence
                objData = None
                for clsParent in self.TestClass.__mro__:
                    if strAttr in clsParent.__dict__:
                        objData = clsParent.__dict__[strAttr]
                        break
                strError = ' '.join(['Inner type of attribute', strAttr,
                                         'in class', self.TestClass.__name__,
                                         'is', str(type(objData)), 'instead of',
                                         str(typType)])
                self.assertIsInstance(objData, typType, strError)
                #change back
                strErrorValue = ' '.join(['Attribute', strAttr, 'of class',
                                     self.TestClass.__name__, 'is not set',
                                     'to the proper value'])
                setattr(self.TestClass, strAttr, gOldValue)
                self.assertEqual(getattr(self.TestClass, strAttr), gOldValue,
                                    strErrorValue)
                objData = None
                for clsParent in self.TestClass.__mro__:
                    if strAttr in clsParent.__dict__:
                        objData = clsParent.__dict__[strAttr]
                        break
                strError = ' '.join(['Inner type of attribute', strAttr,
                                         'in class', self.TestClass.__name__,
                                         'is', str(type(objData)), 'instead of',
                                         str(typType)])
                self.assertIsInstance(objData, typType, strError)
            else:
                with self.assertRaises(AttributeError):
                    setattr(self.TestClass, strAttr, gNewValue)
    
    def test_GetClassFields(self):
        """
        Checks that all class fields are accessible from the class without
        instantiation.
        """
        for strAttr, _, _ in self.ClassFields:
            getattr(self.TestClass, strAttr) #must be ok
        with self.assertRaises(AttributeError): #non-existent attribute
            getattr(self.TestClass, 'foo_bar_shebang')
    
    def test_HasProperties(self):
        """
        Checks that the test class defines the required properties
        """
        for strAttr, _, _, typType in self.Getters:
            strError = 'Class {} has no attribute {}'.format(
                                            self.TestClass.__name__, strAttr)
            self.assertTrue(hasattr(self.TestClass, strAttr), strError)
            strError = '{}.{} is not a property'.format(
                                            self.TestClass.__name__, strAttr)
            objData = None
            for clsParent in self.TestClass.__mro__:
                if strAttr in clsParent.__dict__:
                    objData = clsParent.__dict__[strAttr]
                    break
            self.assertIsInstance(objData, typType, strError)
    
    def test_CheckMethods(self):
        """
        Checks that the class inherits all defined extra methods (class, static
        and instance - but not the introspection ones), as well as that the
        class and static methods return the expected values.  Introspection
        methods are tested separately.
        """
        for strAttr, typType, gValue in self.ClassMethods:
            strError = 'Class {} has no attribute {}'.format(
                                            self.TestClass.__name__, strAttr)
            self.assertTrue(hasattr(self.TestClass, strAttr), strError)
            strError = 'Attribute {} of class {} is not a class method'.format(
                                            strAttr, self.TestClass.__name__)
            self.assertTrue(inspect.ismethod(getattr(self.TestClass, strAttr)),
                                                                    strError)
            objCheck = None
            for clBase in self.TestClass.__mro__:
                if strAttr in clBase.__dict__:
                    objCheck = clBase.__dict__[strAttr]
                    break
            self.assertIsInstance(objCheck, classmethod, strError)
            objReturn = getattr(self.TestClass, strAttr)()
            strError = 'Class method {}.{} returns wrong type'.format(
                                            self.TestClass.__name__, strAttr)
            self.assertIsInstance(objReturn, typType, strError)
            strError = 'Class method {}.{} returns wrong value'.format(
                                            self.TestClass.__name__, strAttr)
            self.assertEqual(objReturn, gValue, strError)
        for strAttr, typType, gValue in self.StaticMethods:
            strError = 'Class {} has no attribute {}'.format(
                                            self.TestClass.__name__, strAttr)
            self.assertTrue(hasattr(self.TestClass, strAttr), strError)
            strError = 'Attribute {} of class {} is not a static method'.format(
                                            strAttr, self.TestClass.__name__)
            self.assertTrue(inspect.isfunction(
                                    getattr(self.TestClass, strAttr)), strError)
            objCheck = None
            for clBase in self.TestClass.__mro__:
                if strAttr in clBase.__dict__:
                    objCheck = clBase.__dict__[strAttr]
                    break
            self.assertIsInstance(objCheck, staticmethod, strError)
            objReturn = getattr(self.TestClass, strAttr)()
            strError = 'Static method {}.{} returns wrong type'.format(
                                            self.TestClass.__name__, strAttr)
            self.assertIsInstance(objReturn, typType, strError)
            strError = 'Static method {}.{} returns wrong value'.format(
                                            self.TestClass.__name__, strAttr)
            self.assertEqual(objReturn, gValue, strError)
        for strAttr, typType, gValue in self.Methods:
            strError = 'Class {} has no attribute {}'.format(
                                            self.TestClass.__name__, strAttr)
            self.assertTrue(hasattr(self.TestClass, strAttr), strError)
            strError = 'Attribute {} of class {} is not a method'.format(
                                            strAttr, self.TestClass.__name__)
            self.assertTrue(inspect.ismethod(getattr(self.TestClass, strAttr)),
                                                                    strError)
            objCheck = None
            for clBase in self.TestClass.__mro__:
                if strAttr in clBase.__dict__:
                    objCheck = clBase.__dict__[strAttr]
                    break
            self.assertTrue(inspect.isfunction(objCheck), strError)

class Test_ClassTest2(Test_ClassTest1):
    """
    Test cases for the class ClassTest2 derived from the ClassTest1 derived from
    pos.base_classes.DescriptedABC - no longer abstract, but inherit the
    support for the descriptors for the class fields.
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        super(Test_ClassTest2, cls).setUpClass()
        cls.TestClass = ClassTest2
        cls.SecondClass = ClassTest1
        cls.InstanceFields = [['InstFloat', float, FloatDescriptor],
                              ['InstConstInt', int, ConstIntegerDescriptor],
                              ['SimpleInt', int, int],
                              ['_string1', str, str],
                              ['_string2', str, str]]
        cls.ConstantInstanceFields = ['InstConstInt']
        cls.PublicMethods = list(sorted(['getClassFields','getClassMethods',
                                        'inspectClassAttribute',
                                        'TestClassMethod', 'TestStaticMethod',
                                        'getFields', 'getMethods',
                                        'TestMethod', 'funcAbs',
                                        'funcAbsBuiltin']))
        cls.PublicFields = list(sorted(['ClassInt', 'ClassConstFloat',
                                        'ClassSimpleInt', 'RO_String',
                                        'RW_String', 'RWD_String', 'SimpleInt',
                                        'InstFloat', 'InstConstInt']))
    
    def test_IsAbstract(self):
        """
        Checks that the test class can be instantiated, i.e. it is not abstract.
        """
        objTest = self.TestClass()
        del objTest
    
    def test_HasInstanceFields(self):
        """
        Checks that all expected class fields are present in the class.
        """
        objTest = self.TestClass()
        for strAttr, _, _ in self.ClassFields:
            strError = 'Missing attribute {} in instance of class {}'.format(
                                            strAttr, self.TestClass.__name__)
            self.assertTrue(hasattr(objTest, strAttr), strError)
        for strAttr, _, _ in self.InstanceFields:
            strError = 'Missing attribute {} in instance of class {}'.format(
                                            strAttr, self.TestClass.__name__)
            self.assertTrue(hasattr(objTest, strAttr), strError)
        strAttr = 'foo_bar_shebang'
        strError = '{} should not be in instance of class {}'.format(strAttr,
                                                    self.TestClass.__name__)
        self.assertFalse(hasattr(objTest, strAttr), strError)
        del objTest
    
    def test_TypeInstanceFields(self):
        """
        Checks that all expected class and instance fields in the class'
        instance are returned as the expected types (via descriptors protocol).
        """
        objTest = self.TestClass()
        for strAttr, typType, _ in self.ClassFields:
            strError = ' '.join(['Type of attribute', strAttr, 'in instance of',
                                'class', self.TestClass.__name__, 'is',
                                str(type(getattr(objTest, strAttr))),
                                'instead of', str(typType)])
            self.assertIsInstance(getattr(objTest, strAttr), typType, strError)
        for strAttr, typType, _ in self.InstanceFields:
            strError = ' '.join(['Type of attribute', strAttr, 'in instance of',
                                'class', self.TestClass.__name__, 'is',
                                str(type(getattr(objTest, strAttr))),
                                'instead of', str(typType)])
            self.assertIsInstance(getattr(objTest, strAttr), typType, strError)
        del objTest
    
    def test_InnerTypeInstanceFields(self):
        """
        Checks that all expected instance fields in the class are internally
        stored as references to the instances of the specific classes.
        """
        objTest = self.TestClass()
        for strAttr, _, typType in self.InstanceFields:
            objData = objTest.__dict__[strAttr]
            strError = ' '.join(['Inner type of attribute', strAttr, 'in'
                                 'instance of the class',
                                 self.TestClass.__name__, 'is',
                                str(type(objData)), 'instead of', str(typType)])
            self.assertIsInstance(objData, typType, strError)
        del objTest
    
    def test_SetInstanceFields(self):
        """
        Checks that the class and instance fields with the descriptors can be
        set from an instance unless they raise an AttributeError in the
        __set__() descriptor.
        """
        objTest = self.TestClass()
        for strAttr, _, typType in self.ClassFields:
            gOldValue = getattr(objTest, strAttr)
            gNewValue = gOldValue + 1
            if not (strAttr in self.ConstantClassFields):
                strErrorValue = ' '.join(['Attribute', strAttr, 'of instance',
                                          'of the class',
                                          self.TestClass.__name__, 'is not set',
                                          'to the proper value'])
                setattr(objTest, strAttr, gNewValue)
                self.assertEqual(getattr(objTest, strAttr), gNewValue,
                                                                strErrorValue)
                strError = ' '.join(['Attribute', strAttr, 'is not a shared',
                                     'state'])
                self.assertEqual(getattr(objTest, strAttr),
                            getattr(self.TestClass, strAttr), strError)
                strError = ' '.join(['Attribute', strAttr, 'is a shared',
                                     'state between super and subclass'])
                if issubclass(self.TestClass, self.SecondClass):
                    self.assertNotEqual(getattr(self.TestClass, strAttr),
                            getattr(self.SecondClass, strAttr), strError)
                    #change of the class field of the subclass should not affect
                    #the same field of the super class - otherwise, the behavior
                    #is not defined - depends on the events sequence
                objData = None
                for clsParent in self.TestClass.__mro__:
                    if strAttr in clsParent.__dict__:
                        objData = clsParent.__dict__[strAttr]
                        break
                strError = ' '.join(['Inner type of attribute', strAttr,
                                         'in class', self.TestClass.__name__,
                                         'is', str(type(objData)), 'instead of',
                                         str(typType)])
                self.assertIsInstance(objData, typType, strError)
                #change back
                strErrorValue = ' '.join(['Attribute', strAttr, 'of instance',
                                          'of the class',
                                          self.TestClass.__name__, 'is not set',
                                          'to the proper value'])
                setattr(objTest, strAttr, gOldValue)
                self.assertEqual(getattr(self.TestClass, strAttr), gOldValue,
                                    strErrorValue)
                strError = ' '.join(['Attribute', strAttr, 'is not a shared',
                                     'state'])
                self.assertEqual(getattr(objTest, strAttr),
                            getattr(self.TestClass, strAttr), strError)
                objData = None
                for clsParent in self.TestClass.__mro__:
                    if strAttr in clsParent.__dict__:
                        objData = clsParent.__dict__[strAttr]
                        break
                strError = ' '.join(['Inner type of attribute', strAttr,
                                         'in class', self.TestClass.__name__,
                                         'is', str(type(objData)), 'instead of',
                                         str(typType)])
                self.assertIsInstance(objData, typType, strError)
            else:
                with self.assertRaises(AttributeError):
                    setattr(objTest, strAttr, gNewValue)
        for strAttr, _, typType in self.InstanceFields:
            gOldValue = getattr(objTest, strAttr)
            if isinstance(gOldValue, basestring):
                gNewValue = gOldValue + "1"
            else:
                gNewValue = gOldValue + 1
            if not (strAttr in self.ConstantInstanceFields):
                strErrorValue = ' '.join(['Attribute', strAttr, 'of instance',
                                          'of the class',
                                          self.TestClass.__name__, 'is not set',
                                          'to the proper value'])
                setattr(objTest, strAttr, gNewValue)
                self.assertEqual(getattr(objTest, strAttr), gNewValue,
                                                                strErrorValue)
                objData = objTest.__dict__[strAttr]
                strError = ' '.join(['Inner type of attribute', strAttr,
                                         'in instance of class',
                                         self.TestClass.__name__, 'is',
                                         str(type(objData)), 'instead of',
                                         str(typType)])
                self.assertIsInstance(objData, typType, strError)
                #change back
                strErrorValue = ' '.join(['Attribute', strAttr, 'of instance',
                                          'of the class',
                                          self.TestClass.__name__, 'is not set',
                                          'to the proper value'])
                setattr(objTest, strAttr, gOldValue)
                self.assertEqual(getattr(objTest, strAttr), gOldValue,
                                                                strErrorValue)
                objData = objTest.__dict__[strAttr]
                strError = ' '.join(['Inner type of attribute', strAttr,
                                         'in instance of class',
                                         self.TestClass.__name__, 'is',
                                         str(type(objData)), 'instead of',
                                         str(typType)])
                self.assertIsInstance(objData, typType, strError)
            else:
                with self.assertRaises(AttributeError):
                    setattr(objTest, strAttr, gNewValue)
        del objTest
    
    def test_DeleteInstanceFields(self):
        """
        Checks that the class and instance fields with the descriptors can be
        deleted unless they raise an AttributeError in the __set__() descriptor
        or they are not at all find in the instance, its class or super classes.
        The AttributeError should also be raised if a non-existent class or
        instance attribute is to be deleted.
        """
        objTest = self.TestClass()
        for strAttr, _, typType in self.ClassFields:
            if strAttr in self.TestClass.__dict__: #must be directly in
            #the class, not inherited!
                if not (strAttr in self.ConstantClassFields):
                    gOldValue = getattr(objTest, strAttr)
                    delattr(objTest, strAttr)
                    strError = ' '.join(['Attribute', strAttr, 'of class',
                                     self.TestClass.__name__, 'is not deleted'])
                    self.assertFalse(hasattr(objTest, strAttr), strError)
                    #restore the class field
                    setattr(objTest.__class__, strAttr, typType(gOldValue))
                    strError = ' '.join(['Attribute', strAttr, 'of class',
                                     self.TestClass.__name__, 'is not set',
                                     'to the proper value'])
                    self.assertTrue(hasattr(objTest, strAttr), strError)
                    strError = ' '.join(['Attribute', strAttr,
                                         'is not a shared', 'state'])
                    self.assertEqual(getattr(objTest, strAttr),
                            getattr(self.TestClass, strAttr), strError)
                    objData = self.TestClass.__dict__[strAttr]
                    strError = ' '.join(['Inner type of attribute', strAttr,
                                         'in class', self.TestClass.__name__,
                                         'is', str(type(objData)), 'instead of',
                                         str(typType)])
                    self.assertIsInstance(objData, typType, strError)
                else: #go through __delete__() descriptor
                    with self.assertRaises(AttributeError):
                        delattr(objTest, strAttr)
            else: #not in the class itself, inherited!
                with self.assertRaises(AttributeError):
                    delattr(objTest, strAttr)
        for strAttr, _, typType in self.InstanceFields:
            if not (strAttr in self.ConstantInstanceFields):
                gOldValue = getattr(objTest, strAttr)
                delattr(objTest, strAttr)
                strError = ' '.join(['Attribute', strAttr, 'of class',
                                     self.TestClass.__name__, 'is not deleted'])
                self.assertFalse(hasattr(objTest, strAttr), strError)
                #restore the instance field
                setattr(objTest, strAttr, typType(gOldValue))
                strError = ' '.join(['Attribute', strAttr, 'of class',
                                     self.TestClass.__name__, 'is not set',
                                     'to the proper value'])
                self.assertTrue(hasattr(objTest, strAttr), strError)
                objData = objTest.__dict__[strAttr]
                strError = ' '.join(['Inner type of attribute', strAttr,
                                         'in class', self.TestClass.__name__,
                                         'is', str(type(objData)), 'instead of',
                                         str(typType)])
                self.assertIsInstance(objData, typType, strError)
            else: #go through __delete__() descriptor
                with self.assertRaises(AttributeError):
                    delattr(objTest, strAttr)
        with self.assertRaises(AttributeError): #non-existent attribute
            delattr(objTest, 'foo_bar_shebang')
        del objTest
    
    def test_GetInstanceFields(self):
        """
        Checks that all required instance and class fields are accessible from
        the class instance.
        """
        objTest = self.TestClass()
        for strAttr, _, _ in self.ClassFields:
            getattr(objTest, strAttr) #must be ok
        for strAttr, _, _ in self.InstanceFields:
            getattr(objTest, strAttr) #must be ok
        with self.assertRaises(AttributeError): #non-existent attribute
            getattr(objTest, 'foo_bar_shebang')
        del objTest
    
    def test_init(self):
        """
        Checks that the class can be instantiated with any number of the
        positional and / or keyword arguments, since the onInit() method accepts
        any such combination.
        """
        #should be ok in all cases
        objTest = self.TestClass()
        del objTest
        objTest = self.TestClass(1)
        del objTest
        objTest = self.TestClass(1, 2)
        del objTest
        objTest = self.TestClass(a = 1)
        del objTest
        objTest = self.TestClass(a = 1, b =2)
        del objTest
        objTest = self.TestClass(1, 2, a = 1, b =2)
        del objTest
    
    def test_HasProperties(self):
        """
        Checks that the test class defines the required properties, and they are
        accessible for its instance.
        """
        super(Test_ClassTest2, self).test_HasProperties()
        objTest = self.TestClass()
        for strAttr, _, _, _ in self.Getters:
            strError = 'Instance of class {} has no attribute {}'.format(
                                            self.TestClass.__name__, strAttr)
            self.assertTrue(hasattr(objTest, strAttr), strError)
        del objTest
    
    def test_GetProperties(self):
        """
        Checks that the properties are accessed as properties, i.e. return
        strings of the expected values.
        """
        objTest = self.TestClass()
        for strAttr, strValue, typType, _ in self.Getters:
            strError = ' '.join(['Property', strAttr, 'of instance of class',
                                self.TestClass.__name__, 'returns wrong type'])
            self.assertIsInstance(getattr(objTest, strAttr), typType, strError)
            strError = ' '.join(['Property', strAttr, 'of instance of class',
                                self.TestClass.__name__, 'returns wrong value'])
            self.assertEqual(getattr(objTest, strAttr), strValue, strError)
        del objTest
    
    def test_SetProperties(self):
        """
        Checks that only the properties with the setter descriptor methods can
        be assigned, but this assignment goes as expected.
        """
        objTest = self.TestClass()
        for strAttr, strValue, typType, _ in self.Getters:
            if strAttr in self.Setters:
                setattr(objTest, strAttr, 'foo-bar')
                strError =' '.join(['Property', strAttr, 'of instance of class',
                                self.TestClass.__name__, 'returns wrong type'])
                self.assertIsInstance(getattr(objTest, strAttr), typType,
                                                                    strError)
                strError =' '.join(['Property', strAttr, 'of instance of class',
                                self.TestClass.__name__, 'returns wrong value'])
                self.assertEqual(getattr(objTest, strAttr), 'foo-bar',
                                                                    strError)
                #set back
                setattr(objTest, strAttr, strValue)
                strError =' '.join(['Property', strAttr, 'of instance of class',
                                self.TestClass.__name__, 'returns wrong type'])
                self.assertIsInstance(getattr(objTest, strAttr), typType,
                                                                    strError)
                strError =' '.join(['Property', strAttr, 'of instance of class',
                                self.TestClass.__name__, 'returns wrong value'])
                self.assertEqual(getattr(objTest, strAttr), strValue, strError)
            else:
                with self.assertRaises(AttributeError):
                    setattr(objTest, strAttr, 'foo-bar')
        del objTest
    
    def test_DeleteProperties(self):
        """
        Checks that only the properties with the deleter descriptor methods can
        be used in 'del' statement.
        """
        objTest = self.TestClass()
        for strAttr, strValue, typType, _ in self.Getters:
            if strAttr in self.Deleters:
                delattr(objTest, strAttr)
                strError =' '.join(['Property', strAttr, 'of instance of class',
                                self.TestClass.__name__, 'returns wrong type'])
                self.assertIsInstance(getattr(objTest, strAttr), typType,
                                                                    strError)
                strError =' '.join(['Property', strAttr, 'of instance of class',
                                self.TestClass.__name__, 'returns wrong value'])
                self.assertEqual(getattr(objTest, strAttr), 'deleted',
                                                                    strError)
                #set back
                setattr(objTest, strAttr, strValue)
                strError =' '.join(['Property', strAttr, 'of instance of class',
                                self.TestClass.__name__, 'returns wrong type'])
                self.assertIsInstance(getattr(objTest, strAttr), typType,
                                                                    strError)
                strError =' '.join(['Property', strAttr, 'of instance of class',
                                self.TestClass.__name__, 'returns wrong value'])
                self.assertEqual(getattr(objTest, strAttr), strValue, strError)
            else:
                with self.assertRaises(AttributeError):
                    delattr(objTest, strAttr)
        del objTest
    
    def test_CheckMethods(self):
        """
        Extends the super class' method to perform the same checks on an
        instance of the class.
        """
        super(Test_ClassTest2, self).test_CheckMethods()
        objTest = self.TestClass()
        for Names in [self.ClassMethods, self.StaticMethods, self.Methods]:
            for strAttr, typType, gValue in Names:
                strError = 'Class {} instance has no attribute {}'.format(
                                            self.TestClass.__name__, strAttr)
                self.assertTrue(hasattr(objTest, strAttr), strError)
                strError = '{}.{} is not a method on instance'.format(
                                            self.TestClass.__name__, strAttr)
                if Names is self.StaticMethods:
                    self.assertTrue(inspect.isfunction(
                                        getattr(objTest, strAttr)), strError)
                else:
                    self.assertTrue(inspect.ismethod(getattr(objTest, strAttr)),
                                                                    strError)
                objReturn = getattr(objTest, strAttr)()
                strError = 'Method {}.{} returns wrong type'.format(
                                            self.TestClass.__name__, strAttr)
                self.assertIsInstance(objReturn, typType, strError)
                strError = 'Method {}.{} returns wrong value'.format(
                                            self.TestClass.__name__, strAttr)
                self.assertEqual(objReturn, gValue, strError)
        del objTest
    
    def test_getClassFields(self):
        """
        Checks that the class method getClassFields() returns a sorted list of
        all 'public' class fields when called on the class itself as well as on
        its instance
        """
        super(Test_ClassTest2, self).test_getClassFields()
        objTest = self.TestClass()
        self.assertEqual(objTest.getClassFields(), self.PublicClassFields)
        del objTest

    def test_getFields(self):
        """
        Checks that the instance method getFields() returns a sorted list of
        all 'public' fields when called on an instance of this class. Must
        include all 'public' class data attributes, real 'public' instance data
        attributes and properties.
        """
        objTest = self.TestClass()
        self.assertEqual(objTest.getFields(), self.PublicFields)
        del objTest
    
    def test_getClassMethods(self):
        """
        Checks that the class method getClassMethods() returns a sorted list of
        all 'public' class methods when called on the class itself as well as on
        its instance
        """
        super(Test_ClassTest2, self).test_getClassMethods()
        objTest = self.TestClass()
        self.assertEqual(objTest.getClassMethods(), self.PublicClassMethods)
        del objTest

    def test_getMethods(self):
        """
        Checks that the instance method getMethods() returns a sorted list of
        all 'public' methods when called on an instance of this class. Must
        include all 'public' class/ static methods, real 'public' instance
        methods as well as foreign class methods / simple functions references
        stored in the 'public' instance attributes.
        """
        objTest = self.TestClass()
        self.assertEqual(objTest.getMethods(), self.PublicMethods)
        del objTest
    
    def test_dir(self):
        """
        Checks that the built-in function dir() returns the proper list of the
        names of ALL 'public' attributes visible at the instance level.
        """
        objTest = self.TestClass()
        strlstTest = dir(objTest)
        strlstExpected = sorted(self.PublicMethods + self.PublicFields)
        self.assertEqual(strlstTest, strlstExpected)
        del objTest

class Test_ClassTest3(Test_ClassTest2):
    """
    Test cases for the class ClassTest3 -|> ClassTest2 -|>ClassTest1 -|>
    pos.base_classes.DescriptedABC - no longer abstract, but inherit the
    support for the descriptors for the class fields.
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        super(Test_ClassTest2, cls).setUpClass()
        cls.TestClass = ClassTest3
        cls.SecondClass = ClassTest2
    
    def test_init(self):
        """
        Checks that the onInit() method is properly overridden - neither
        positional nor keyword arguments are allowed. Therefore, the class can
        be instantiated only without arguments.
        """
        objTest = self.TestClass() #should be ok
        del objTest
        with self.assertRaises(TypeError):
            self.TestClass(1) #should be wrong
        with self.assertRaises(TypeError):
            self.TestClass(a = 1) #should be wrong

#+ test suites

TestSuite1 = unittest.TestLoader().loadTestsFromTestCase(Test_DescriptedABC)
TestSuite2 = unittest.TestLoader().loadTestsFromTestCase(Test_ClassTest1)
TestSuite3 = unittest.TestLoader().loadTestsFromTestCase(Test_ClassTest2)
TestSuite4 = unittest.TestLoader().loadTestsFromTestCase(Test_ClassTest3)

TestSuite = unittest.TestSuite()
TestSuite.addTests([TestSuite1, TestSuite2, TestSuite3, TestSuite4])

if __name__ == "__main__":
    sys.stdout.write("Conducting pos.base_classes.DescriptedABC tests...\n")
    sys.stdout.flush()
    unittest.TextTestRunner(verbosity = 2).run(TestSuite)