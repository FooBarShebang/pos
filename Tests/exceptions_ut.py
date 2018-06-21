#usr/bin/python
"""
Module pos.tests.exceptions_ut

Implements unit testing of the module pos.exceptions.
"""

__version__ = "0.0.1.0"
__date__ = "21-06-2018"
__status__ = "Testing"

#imports

#+ standard libraries

import sys
import unittest

#+ my libraries

import pos.exceptions as testmodule

from pos.utils.traceback import ExceptionTraceback as tb

#helper functions

def inner(clsException, *args, **kwargs):
    """
    The innermost function in the chain, which raises the specified exception
    with the given arguments.
    """
    raise clsException(*args, **kwargs)

def middle(clsException, *args, **kwargs):
    """
    Middle function in the functions chain called from a test case to raise a
    specific exception with the given arguments. 
    """
    inner(clsException, *args, **kwargs)

def outer(clsException, *args, **kwargs):
    """
    The outermost function in the functions chain called from a test case to
    raise a specific exception with the given arguments. This fucntion is called
    directly in the test case.
    """
    middle(clsException, *args, **kwargs)

#classes

#+ test cases

class Test_CustomError(unittest.TestCase):
    """
    Test cases for the class pos.exceptions.CustomError
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        cls.TestClass = testmodule.CustomError
        cls.SuperClasses = [Exception, StandardError]
        #True upwards
        cls.NotRelatedClasses = [AttributeError, SyntaxError, TypeError,
                                 ValueError]
        #False upwards and downwards
        cls.SubClasses = [testmodule.CustomAttributeError,
                            testmodule.ConstantAttributeAssignment,
                            testmodule.NotExistingAttribute,
                            testmodule.PrivateAttributeAccess,
                            testmodule.DesignContractError,
                            testmodule.ConstantAssignment,
                            testmodule.NotInDCError,
                            testmodule.CustomTypeError,
                            testmodule.DCArgumentType,
                            testmodule.DCReturnType,
                            testmodule.CustomValueError,
                            testmodule.DCArgumentValue,
                            testmodule.DCReturnValue
                            ]
        #True downwards
        cls.Properties = {'Traceback' : tb,
                          'CallChain' : list,
                          'Info' : str}
        cls.Attributes = {'message' : 'test',
                          'args' : ('test', )}
    
    def test_IsSubclass(self):
        """
        Checks ascending 'IS A' relations of this class including the virtual
        sub classes as well as 'HAS A' checks (composition). This test ensures
        that the exception can be caught as a subclass of its real direct and
        indirect super classes as well as its 'virtual' sub-classes.
        """
        #check super classes - 'parents' and above
        strErr = '{} is not a sub-class of itself'.format(
                                                        self.TestClass.__name__)
        self.assertTrue(issubclass(self.TestClass, self.TestClass), strErr)
        for clsReference in self.SuperClasses:
            strErr = '{} is not a sub-class of {}'.format(
                                self.TestClass.__name__, clsReference.__name__)
            self.assertTrue(issubclass(self.TestClass, clsReference), strErr)
        #check not super classes - either descendant or not related
        for clsReference in self.NotRelatedClasses:
            strErr = '{} is a sub-class of {}'.format(
                                self.TestClass.__name__, clsReference.__name__)
            self.assertFalse(issubclass(self.TestClass, clsReference), strErr)
        for clsReference in self.SubClasses:
            strErr = '{} is a sub-class of {}'.format(
                                self.TestClass.__name__, clsReference.__name__)
            self.assertFalse(issubclass(self.TestClass, clsReference), strErr)
    
    def test_HasSubclass(self):
        """
        Checks descending 'IS A' relations of this class including the virtual
        sub classes as well as 'HAS A' checks (composition). This test ensures
        that the exception can be used to catch its direct and indirect
        subclasses as well the exceptions registered as its virtual subclasses.
        """
        #check super classes - 'parents' and above
        for clsReference in self.SuperClasses:
            strErr = '{} is a sub-class of {}'.format(
                                clsReference.__name__, self.TestClass.__name__)
            self.assertFalse(issubclass(clsReference, self.TestClass), strErr)
        #check not super classes - either descendant or not related
        for clsReference in self.NotRelatedClasses:
            strErr = '{} is a sub-class of {}'.format(
                                clsReference.__name__, self.TestClass.__name__)
            self.assertFalse(issubclass(clsReference, self.TestClass), strErr)
        for clsReference in self.SubClasses:
            strErr = '{} is not a sub-class of {}'.format(
                                clsReference.__name__, self.TestClass.__name__)
            self.assertTrue(issubclass(clsReference, self.TestClass), strErr)
    
    def test_HasProperty(self):
        """
        This test ensures that the exception class defines attributes required
        for a custom exception with the built-in traceback functionality without
        instantiation of the exception class.
        """
        for strAttr in self.Properties.keys():
            strErr = '{} doesn`t have property {}'.format(
                                            self.TestClass.__name__, strAttr)
            self.assertTrue(hasattr(self.TestClass, strAttr), strErr)
        strErr = "{} doesn't have method __del__()".format(self.TestClass)
        self.assertTrue(hasattr(self.TestClass, '__del__'), strErr)
    
    def test_Raise(self):
        """
        Tests that the initialization method accepts / requires the specified
        number of the arguments, and the attributes and properties of the
        instance of the raised exception are of the proper types and values.
        See the test class set-up method. Basically, checks the normal usage.
        """
        #raise from outside
        try:
            outer(self.TestClass, *(self.Attributes['args']))
        except self.TestClass as errTest:
            for strAttr, gValue in self.Properties.items():
                strErr = 'instance of {} doesn`t have property {}'.format(
                                            self.TestClass.__name__, strAttr)
                self.assertTrue(hasattr(errTest, strAttr), strErr)
                gTestValue = getattr(errTest, strAttr)
                strErr = '{} of the instance property {} - must be {}'.format(
                                    type(gTestValue), strAttr, gValue.__name__)
                self.assertIsInstance(gTestValue, gValue, strErr)
            for strAttr, gValue in self.Attributes.items():
                strErr = 'instance of {} doesn`t have attribute {}'.format(
                                            self.TestClass.__name__, strAttr)
                self.assertTrue(hasattr(errTest, strAttr), strErr)
                strErr = 'value of {}.{} is {} - should be {}'.format(
                                            self.TestClass.__name__, strAttr,
                                            getattr(errTest, strAttr), gValue)
                self.assertEqual(getattr(errTest, strAttr), gValue, strErr)
            #check correctness of the callers chain list directly
            lstCallChain = errTest.CallChain
            #must contain exactly 4 elements
            self.assertEqual(len(lstCallChain), 4,
                'traceback size must be 4 not {}'.format(len(lstCallChain)))
            #must start always in this method
            self.assertEqual(lstCallChain[0],
                '{}.{}.test_Raise'.format(__name__, self.__class__.__name__),
                    'top of the traceback - {} not this method'.format(
                                                            lstCallChain[0]))
        
            # second element must point to the outer() function
            self.assertEqual(lstCallChain[1],
                    '{}.outer'.format(__name__),
                        'second element - {} not "{}.outer"'.format(
                                                    lstCallChain[1], __name__))
            # third element must point to the middle() function
            self.assertEqual(lstCallChain[2],
                    '{}.middle'.format(__name__),
                        'third element - {} not "{}.middle"'.format(
                                                    lstCallChain[2], __name__))
            # last element must point to the inner() function
            self.assertEqual(lstCallChain[3],
                    '{}.inner'.format(__name__),
                        'forth element - {} not "{}.inner"'.format(
                                                    lstCallChain[3], __name__))
            #check the correctness of the Info - indirectly
            strInfoText = errTest.Traceback.Info
            strFullInfo = '\n'.join([
                '{}: {}'.format(self.TestClass.__name__,
                                    self.Attributes['message']), strInfoText])
            self.assertEqual(strFullInfo, errTest.Info, 'error tracebace info')
            del errTest
        #raise from inside - simplified check
        try:
            raise self.TestClass(*(self.Attributes['args']))
        except self.TestClass as errTest:
            #check correctness of the callers chain list directly
            lstCallChain = errTest.CallChain
            #must contain exactly 4 elements
            self.assertEqual(len(lstCallChain), 1,
                'traceback size must be 1 not {}'.format(len(lstCallChain)))
            #must start always in this method
            self.assertEqual(lstCallChain[0],
                '{}.{}.test_Raise'.format(__name__, self.__class__.__name__),
                    'top of the traceback - {} not this method'.format(
                                                            lstCallChain[0]))
        
            #check the correctness of the Info - indirectly
            strInfoText = errTest.Traceback.Info
            strFullInfo = '\n'.join([
                '{}: {}'.format(self.TestClass.__name__,
                                    self.Attributes['message']), strInfoText])
            self.assertEqual(strFullInfo, errTest.Info, 'error tracebace info')
            del errTest
    
    def test_RaiseHide(self):
        """
        Tests that the exception provides the desired truncated traceback when
        it is raised with the optional skipping of the specified number of the
        innermost call frames.
        """
        #raise from outside
        try:
            outer(self.TestClass, *(self.Attributes['args']), iSkipFrames = 2)
        except self.TestClass as errTest:
            #check correctness of the callers chain list directly
            lstCallChain = errTest.CallChain
            #must contain exactly 4 elements
            self.assertEqual(len(lstCallChain), 2,
                'traceback size must be 2 not {}'.format(len(lstCallChain)))
            #must start always in this method
            self.assertEqual(lstCallChain[0],
                '{}.{}.test_RaiseHide'.format(__name__,
                                                self.__class__.__name__),
                    'top of the traceback - {} not this method'.format(
                                                            lstCallChain[0]))
        
            # second = last element must point to the outer() function
            self.assertEqual(lstCallChain[1],
                    '{}.outer'.format(__name__),
                        'second element - {} not "{}.outer"'.format(
                                                    lstCallChain[1], __name__))
            #check the correctness of the Info - indirectly
            strInfoText = errTest.Traceback.Info
            strFullInfo = '\n'.join([
                '{}: {}'.format(self.TestClass.__name__,
                                    self.Attributes['message']), strInfoText])
            self.assertEqual(strFullInfo, errTest.Info, 'error tracebace info')
            del errTest
        #raise with too large number of frames to hide - must be ignored
        try:
            outer(self.TestClass, *(self.Attributes['args']), iSkipFrames = 6)
        except self.TestClass as errTest:
            #check correctness of the callers chain list directly
            lstCallChain = errTest.CallChain
            #must contain exactly 4 elements
            self.assertEqual(len(lstCallChain), 4,
                'traceback size must be 4 not {}'.format(len(lstCallChain)))
            del errTest
        #raise with negative number of frames to hide - must be ignored
        try:
            outer(self.TestClass, *(self.Attributes['args']), iSkipFrames = -6)
        except self.TestClass as errTest:
            #check correctness of the callers chain list directly
            lstCallChain = errTest.CallChain
            #must contain exactly 4 elements
            self.assertEqual(len(lstCallChain), 4,
                'traceback size must be 4 not {}'.format(len(lstCallChain)))
            del errTest
        #raise with zero number of frames to hide - must be ignored
        try:
            outer(self.TestClass, *(self.Attributes['args']), iSkipFrames = 0)
        except self.TestClass as errTest:
            #check correctness of the callers chain list directly
            lstCallChain = errTest.CallChain
            #must contain exactly 4 elements
            self.assertEqual(len(lstCallChain), 4,
                'traceback size must be 4 not {}'.format(len(lstCallChain)))
            del errTest
        #raise with not integer number of frames to hide - must be ignored
        try:
            outer(self.TestClass, *(self.Attributes['args']), iSkipFrames = 1.0)
        except self.TestClass as errTest:
            #check correctness of the callers chain list directly
            lstCallChain = errTest.CallChain
            #must contain exactly 4 elements
            self.assertEqual(len(lstCallChain), 4,
                'traceback size must be 4 not {}'.format(len(lstCallChain)))
            del errTest
    
    def test_Reraise(self):
        """
        Tests that the exception preserves the traceback information when it is
        re-raised with the traceback of another exception - i.e. the situation
        when the exception type is replaced during the handling.
        """
        #raise from outside
        try:
            outer(self.TestClass, *(self.Attributes['args']))
        except self.TestClass as errTest:
            #proper
            try:
                raise self.TestClass(*(self.Attributes['args']),
                                            objTraceback = errTest.Traceback)
            except self.TestClass as errTestNew:
                self.assertListEqual(errTest.CallChain, errTestNew.CallChain,
                                     'CallChain is not preserved')
                self.assertEqual(errTest.Info, errTestNew.Info,
                                     'Info is not preserved')
                del errTestNew
            #wrong type of the traceback argument - must be ignored - i.e. as
            #+ raised inside
            try:
                raise self.TestClass(*(self.Attributes['args']),
                                            objTraceback = 1)
            except self.TestClass as errTestNew:
                self.assertEqual(len(errTestNew.CallChain), 1,
                                     'CallChain is wrong')
                del errTestNew
            del errTest
    
    def test_ReraiseHide(self):
        """
        Tests that the exception properly truncates the traceback information
        when it is re-raised with the traceback of another exception - i.e. the
        situation when the exception type is replaced during the handling and
        some innermost call frames must be hidden.
        """
        #raise from outside
        try:
            outer(self.TestClass, *(self.Attributes['args']))
        except self.TestClass as errTest:
            try:
                raise self.TestClass(*(self.Attributes['args']),
                                            objTraceback = errTest.Traceback,
                                            iSkipFrames = 2)
            except self.TestClass as errTestNew:
                self.assertListEqual(errTest.CallChain[ : -2],
                                     errTestNew.CallChain,
                                     'CallChain is not properly truncated')
                strInfoText = errTestNew.Traceback.Info
                strFullInfo = '\n'.join([
                '{}: {}'.format(self.TestClass.__name__,
                                    self.Attributes['message']), strInfoText])
                self.assertEqual(strFullInfo, errTestNew.Info,
                                     'Info is not properly truncated')
                del errTestNew
            del errTest

class Test_DesignContractError(Test_CustomError):
    """
    Test cases for the class pos.exceptions.DesignContractError
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        cls.TestClass = testmodule.DesignContractError
        cls.SuperClasses = [Exception, StandardError, testmodule.CustomError]
        #True upwards
        cls.NotRelatedClasses = [AttributeError, SyntaxError,
                                 ValueError, TypeError,
                                 testmodule.CustomAttributeError,
                                 testmodule.ConstantAttributeAssignment,
                                 testmodule.NotExistingAttribute,
                                 testmodule.PrivateAttributeAccess,
                                 testmodule.ConstantAssignment,
                                 testmodule.CustomTypeError,
                                 testmodule.CustomValueError
                                 ]
        #False upwards and downwards
        cls.SubClasses = [testmodule.NotInDCError,
                            testmodule.DCArgumentType,
                            testmodule.DCReturnType,
                            testmodule.DCArgumentValue,
                            testmodule.DCReturnValue
                            ]
        #True downwards
        cls.Properties = {'Traceback' : tb,
                          'CallChain' : list,
                          'Info' : str}
        cls.Attributes = {'message' : 'test',
                          'args' : ('test', )}

class Test_ConstantAssignment(Test_CustomError):
    """
    Test cases for the class pos.exceptions.ConstantAssignment
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        cls.TestClass = testmodule.ConstantAssignment
        cls.SuperClasses = [Exception, StandardError, testmodule.CustomError]
        #True upwards
        cls.NotRelatedClasses = [AttributeError, SyntaxError,
                                 ValueError, TypeError,
                                 testmodule.DesignContractError,
                                 testmodule.CustomAttributeError,
                                 testmodule.NotExistingAttribute,
                                 testmodule.PrivateAttributeAccess,
                                 testmodule.CustomTypeError,
                                 testmodule.CustomValueError,
                                 testmodule.NotInDCError,
                                 testmodule.DCArgumentType,
                                 testmodule.DCReturnType,
                                 testmodule.DCArgumentValue,
                                 testmodule.DCReturnValue
                                 ]
        #False upwards and downwards
        cls.SubClasses = [testmodule.ConstantAttributeAssignment
                            ]
        #True downwards
        cls.Properties = {'Traceback' : tb,
                          'CallChain' : list,
                          'Info' : str}
        strValue = 'Attr'
        strMessage = "Cannot change value of the constant {}".format(strValue)
        cls.Attributes = {'message' : strMessage,
                          'args' : (strValue, )}

class Test_NotInDCError(Test_CustomError):
    """
    Test cases for the class pos.exceptions.NotInDCError
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        cls.TestClass = testmodule.NotInDCError
        cls.SuperClasses = [Exception, StandardError, SyntaxError,
                            testmodule.CustomError,
                            testmodule.DesignContractError]
        #True upwards
        cls.NotRelatedClasses = [AttributeError, ValueError, TypeError,
                                 testmodule.ConstantAssignment,
                                 testmodule.CustomAttributeError,
                                 testmodule.NotExistingAttribute,
                                 testmodule.PrivateAttributeAccess,
                                 testmodule.CustomTypeError,
                                 testmodule.CustomValueError,
                                 testmodule.DCArgumentType,
                                 testmodule.DCReturnType,
                                 testmodule.DCArgumentValue,
                                 testmodule.DCReturnValue,
                                 testmodule.ConstantAttributeAssignment
                                 ]
        #False upwards and downwards
        cls.SubClasses = []
        #True downwards
        cls.Properties = {'Traceback' : tb,
                          'CallChain' : list,
                          'Info' : str}
        strValue = 'Attr'
        strMessage = "Design Contract is not found for {}".format(strValue)
        cls.Attributes = {'message' : strMessage,
                          'args' : (strValue, )}

class Test_CustomAttributeError(Test_CustomError):
    """
    Test cases for the class pos.exceptions.CustomAttributeError
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        cls.TestClass = testmodule.CustomAttributeError
        cls.SuperClasses = [Exception, StandardError, AttributeError,
                            testmodule.CustomError]
        #True upwards
        cls.NotRelatedClasses = [SyntaxError, ValueError, TypeError,
                                 testmodule.ConstantAssignment,
                                 testmodule.NotInDCError,
                                 testmodule.CustomTypeError,
                                 testmodule.CustomValueError,
                                 testmodule.DCArgumentType,
                                 testmodule.DCReturnType,
                                 testmodule.DCArgumentValue,
                                 testmodule.DCReturnValue,
                                 testmodule.DesignContractError
                                 ]
        #False upwards and downwards
        cls.SubClasses = [testmodule.ConstantAttributeAssignment,
                            testmodule.NotExistingAttribute,
                            testmodule.PrivateAttributeAccess]
        #True downwards
        cls.Properties = {'Traceback' : tb,
                          'CallChain' : list,
                          'Info' : str}
        strMessage = 'Attribute "{}" of class {}.{}'.format(
                                            'Attr', cls.TestClass.__module__,
                                            cls.TestClass.__name__)
        cls.Attributes = {'message' : strMessage,
                          'args' : ('Attr', cls.TestClass)}

class Test_ConstantAttributeAssignment(Test_CustomError):
    """
    Test cases for the class pos.exceptions.ConstantAttributeAssignment
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        cls.TestClass = testmodule.ConstantAttributeAssignment
        cls.SuperClasses = [Exception, StandardError, AttributeError,
                            testmodule.CustomError,
                            testmodule.CustomAttributeError,
                            testmodule.ConstantAssignment]
        #True upwards
        cls.NotRelatedClasses = [SyntaxError, ValueError, TypeError,
                                 testmodule.NotInDCError,
                                 testmodule.CustomTypeError,
                                 testmodule.CustomValueError,
                                 testmodule.DCArgumentType,
                                 testmodule.DCReturnType,
                                 testmodule.DCArgumentValue,
                                 testmodule.DCReturnValue,
                                 testmodule.DesignContractError,
                                 testmodule.NotExistingAttribute,
                                 testmodule.PrivateAttributeAccess
                                 ]
        #False upwards and downwards
        cls.SubClasses = []
        #True downwards
        cls.Properties = {'Traceback' : tb,
                          'CallChain' : list,
                          'Info' : str}
        strMessage = 'Attribute "{}" of class {}.{}'.format(
                                            'Attr', cls.TestClass.__module__,
                                            cls.TestClass.__name__)
        cls.Attributes = {'message' : strMessage,
                          'args' : ('Attr', cls.TestClass)}

class Test_NotExistingAttribute(Test_CustomError):
    """
    Test cases for the class pos.exceptions.NotExistingAttribute
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        cls.TestClass = testmodule.NotExistingAttribute
        cls.SuperClasses = [Exception, StandardError, AttributeError,
                            testmodule.CustomError,
                            testmodule.CustomAttributeError]
        #True upwards
        cls.NotRelatedClasses = [SyntaxError, ValueError, TypeError,
                                 testmodule.NotInDCError,
                                 testmodule.CustomTypeError,
                                 testmodule.CustomValueError,
                                 testmodule.DCArgumentType,
                                 testmodule.DCReturnType,
                                 testmodule.DCArgumentValue,
                                 testmodule.DCReturnValue,
                                 testmodule.DesignContractError,
                                 testmodule.PrivateAttributeAccess,
                                 testmodule.ConstantAttributeAssignment,
                                 testmodule.ConstantAssignment
                                 ]
        #False upwards and downwards
        cls.SubClasses = []
        #True downwards
        cls.Properties = {'Traceback' : tb,
                          'CallChain' : list,
                          'Info' : str}
        strMessage = 'Attribute "{}" of class {}.{}'.format(
                                            'Attr', cls.TestClass.__module__,
                                            cls.TestClass.__name__)
        cls.Attributes = {'message' : strMessage,
                          'args' : ('Attr', cls.TestClass)}

class Test_PrivateAttributeAccess(Test_CustomError):
    """
    Test cases for the class pos.exceptions.PrivateAttributeAccess
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        cls.TestClass = testmodule.PrivateAttributeAccess
        cls.SuperClasses = [Exception, StandardError, AttributeError,
                            testmodule.CustomError,
                            testmodule.CustomAttributeError]
        #True upwards
        cls.NotRelatedClasses = [SyntaxError, ValueError, TypeError,
                                 testmodule.NotInDCError,
                                 testmodule.CustomTypeError,
                                 testmodule.CustomValueError,
                                 testmodule.DCArgumentType,
                                 testmodule.DCReturnType,
                                 testmodule.DCArgumentValue,
                                 testmodule.DCReturnValue,
                                 testmodule.DesignContractError,
                                 testmodule.ConstantAttributeAssignment,
                                 testmodule.ConstantAssignment,
                                 testmodule.NotExistingAttribute
                                 ]
        #False upwards and downwards
        cls.SubClasses = []
        #True downwards
        cls.Properties = {'Traceback' : tb,
                          'CallChain' : list,
                          'Info' : str}
        strMessage = 'Attribute "{}" of class {}.{}'.format(
                                            'Attr', cls.TestClass.__module__,
                                            cls.TestClass.__name__)
        cls.Attributes = {'message' : strMessage,
                          'args' : ('Attr', cls.TestClass)}

class Test_CustomTypeError(Test_CustomError):
    """
    Test cases for the class pos.exceptions.CustomTypeError
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        cls.TestClass = testmodule.CustomTypeError
        cls.SuperClasses = [Exception, StandardError, TypeError,
                            testmodule.CustomError
                            ]
        #True upwards
        cls.NotRelatedClasses = [SyntaxError, ValueError, AttributeError,
                                 testmodule.NotInDCError,
                                 testmodule.CustomValueError,
                                 testmodule.DCArgumentValue,
                                 testmodule.DCReturnValue,
                                 testmodule.DesignContractError,
                                 testmodule.ConstantAttributeAssignment,
                                 testmodule.ConstantAssignment,
                                 testmodule.NotExistingAttribute,
                                 testmodule.PrivateAttributeAccess,
                                 testmodule.CustomAttributeError
                                 ]
        #False upwards and downwards
        cls.SubClasses = [testmodule.DCArgumentType, testmodule.DCReturnType]
        #True downwards
        cls.Properties = {'Traceback' : tb,
                          'CallChain' : list,
                          'Info' : str}
        strValue = 'Attr'
        typeTest = int
        strMessage = '{} of {} is not of {}'.format(strValue, type(strValue),
                                                            typeTest.__name__)
        cls.Attributes = {'message' : strMessage,
                          'args' : (strValue, typeTest)}

class Test_DCArgumentType(Test_CustomError):
    """
    Test cases for the class pos.exceptions.DCArgumentType
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        cls.TestClass = testmodule.DCArgumentType
        cls.SuperClasses = [Exception, StandardError, TypeError,
                            testmodule.CustomError, testmodule.CustomTypeError,
                            testmodule.DesignContractError
                            ]
        #True upwards
        cls.NotRelatedClasses = [SyntaxError, ValueError, AttributeError,
                                 testmodule.NotInDCError,
                                 testmodule.CustomValueError,
                                 testmodule.DCArgumentValue,
                                 testmodule.DCReturnValue,
                                 testmodule.ConstantAttributeAssignment,
                                 testmodule.ConstantAssignment,
                                 testmodule.NotExistingAttribute,
                                 testmodule.PrivateAttributeAccess,
                                 testmodule.CustomAttributeError,
                                 testmodule.DCReturnType
                                 ]
        #False upwards and downwards
        cls.SubClasses = []
        #True downwards
        cls.Properties = {'Traceback' : tb,
                          'CallChain' : list,
                          'Info' : str}
        strValue = 'Attr'
        typeTest = int
        strMessage = '{} of {} is not of {}'.format(strValue, type(strValue),
                                                            typeTest.__name__)
        cls.Attributes = {'message' : strMessage,
                          'args' : (strValue, typeTest)}

class Test_DCReturnType(Test_CustomError):
    """
    Test cases for the class pos.exceptions.DCReturnType
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        cls.TestClass = testmodule.DCReturnType
        cls.SuperClasses = [Exception, StandardError, TypeError,
                            testmodule.CustomError, testmodule.CustomTypeError,
                            testmodule.DesignContractError
                            ]
        #True upwards
        cls.NotRelatedClasses = [SyntaxError, ValueError, AttributeError,
                                 testmodule.NotInDCError,
                                 testmodule.CustomValueError,
                                 testmodule.DCArgumentValue,
                                 testmodule.DCReturnValue,
                                 testmodule.ConstantAttributeAssignment,
                                 testmodule.ConstantAssignment,
                                 testmodule.NotExistingAttribute,
                                 testmodule.PrivateAttributeAccess,
                                 testmodule.CustomAttributeError,
                                 testmodule.DCArgumentType
                                 ]
        #False upwards and downwards
        cls.SubClasses = []
        #True downwards
        cls.Properties = {'Traceback' : tb,
                          'CallChain' : list,
                          'Info' : str}
        strValue = 'Attr'
        typeTest = int
        strMessage = '{} of {} is not of {}'.format(strValue, type(strValue),
                                                            typeTest.__name__)
        cls.Attributes = {'message' : strMessage,
                          'args' : (strValue, typeTest)}

class Test_CustomValueError(Test_CustomError):
    """
    Test cases for the class pos.exceptions.CustomValueError
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        cls.TestClass = testmodule.CustomValueError
        cls.SuperClasses = [Exception, StandardError, ValueError,
                            testmodule.CustomError
                            ]
        #True upwards
        cls.NotRelatedClasses = [SyntaxError, TypeError, AttributeError,
                                 testmodule.NotInDCError,
                                 testmodule.CustomTypeError,
                                 testmodule.DCArgumentType,
                                 testmodule.DCReturnType,
                                 testmodule.DesignContractError,
                                 testmodule.ConstantAttributeAssignment,
                                 testmodule.ConstantAssignment,
                                 testmodule.NotExistingAttribute,
                                 testmodule.PrivateAttributeAccess,
                                 testmodule.CustomAttributeError
                                 ]
        #False upwards and downwards
        cls.SubClasses = [testmodule.DCArgumentValue, testmodule.DCReturnValue]
        #True downwards
        cls.Properties = {'Traceback' : tb,
                          'CallChain' : list,
                          'Info' : str}
        strValue = 'Attr'
        strError = 'all capitals'
        strMessage = "Value {} doesn't match criteria {}".format(strValue,
                                                                    strError)
        cls.Attributes = {'message' : strMessage,
                          'args' : (strValue, strError)}

class Test_DCArgumentValue(Test_CustomError):
    """
    Test cases for the class pos.exceptions.DCArgumentValue
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        cls.TestClass = testmodule.DCArgumentValue
        cls.SuperClasses = [Exception, StandardError, ValueError,
                            testmodule.CustomError, testmodule.CustomValueError,
                            testmodule.DesignContractError
                            ]
        #True upwards
        cls.NotRelatedClasses = [SyntaxError, TypeError, AttributeError,
                                 testmodule.NotInDCError,
                                 testmodule.CustomTypeError,
                                 testmodule.DCArgumentType,
                                 testmodule.DCReturnType,
                                 testmodule.ConstantAttributeAssignment,
                                 testmodule.ConstantAssignment,
                                 testmodule.NotExistingAttribute,
                                 testmodule.PrivateAttributeAccess,
                                 testmodule.CustomAttributeError,
                                 testmodule.DCReturnValue
                                 ]
        #False upwards and downwards
        cls.SubClasses = []
        #True downwards
        cls.Properties = {'Traceback' : tb,
                          'CallChain' : list,
                          'Info' : str}
        strValue = 'Attr'
        strError = 'all capitals'
        strMessage = "Value {} doesn't match criteria {}".format(strValue,
                                                                    strError)
        cls.Attributes = {'message' : strMessage,
                          'args' : (strValue, strError)}

class Test_DCReturnValue(Test_CustomError):
    """
    Test cases for the class pos.exceptions.DCReturnValue
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        cls.TestClass = testmodule.DCReturnValue
        cls.SuperClasses = [Exception, StandardError, ValueError,
                            testmodule.CustomError, testmodule.CustomValueError,
                            testmodule.DesignContractError
                            ]
        #True upwards
        cls.NotRelatedClasses = [SyntaxError, TypeError, AttributeError,
                                 testmodule.NotInDCError,
                                 testmodule.CustomTypeError,
                                 testmodule.DCArgumentType,
                                 testmodule.DCReturnType,
                                 testmodule.ConstantAttributeAssignment,
                                 testmodule.ConstantAssignment,
                                 testmodule.NotExistingAttribute,
                                 testmodule.PrivateAttributeAccess,
                                 testmodule.CustomAttributeError,
                                 testmodule.DCArgumentValue
                                 ]
        #False upwards and downwards
        cls.SubClasses = []
        #True downwards
        cls.Properties = {'Traceback' : tb,
                          'CallChain' : list,
                          'Info' : str}
        strValue = 'Attr'
        strError = 'all capitals'
        strMessage = "Value {} doesn't match criteria {}".format(strValue,
                                                                    strError)
        cls.Attributes = {'message' : strMessage,
                          'args' : (strValue, strError)}

#+ test suites

TestSuite1 = unittest.TestLoader().loadTestsFromTestCase(Test_CustomError)
TestSuite2 = unittest.TestLoader().loadTestsFromTestCase(
                                                    Test_DesignContractError)
TestSuite3 = unittest.TestLoader().loadTestsFromTestCase(
                                                    Test_ConstantAssignment)
TestSuite4 = unittest.TestLoader().loadTestsFromTestCase(
                                                    Test_NotInDCError)
TestSuite5 = unittest.TestLoader().loadTestsFromTestCase(
                                                    Test_CustomAttributeError)
TestSuite6 = unittest.TestLoader().loadTestsFromTestCase(
                                            Test_ConstantAttributeAssignment)
TestSuite7 = unittest.TestLoader().loadTestsFromTestCase(
                                            Test_NotExistingAttribute)
TestSuite8 = unittest.TestLoader().loadTestsFromTestCase(
                                            Test_PrivateAttributeAccess)
TestSuite9 = unittest.TestLoader().loadTestsFromTestCase(
                                            Test_CustomTypeError)
TestSuite10 = unittest.TestLoader().loadTestsFromTestCase(
                                            Test_DCArgumentType)
TestSuite11 = unittest.TestLoader().loadTestsFromTestCase(
                                            Test_DCReturnType)
TestSuite12 = unittest.TestLoader().loadTestsFromTestCase(
                                            Test_CustomValueError)
TestSuite13 = unittest.TestLoader().loadTestsFromTestCase(
                                            Test_DCArgumentValue)
TestSuite14 = unittest.TestLoader().loadTestsFromTestCase(
                                            Test_DCReturnValue)
TestSuite = unittest.TestSuite()
TestSuite.addTests([TestSuite1, TestSuite2, TestSuite3, TestSuite4,
                    TestSuite5, TestSuite6, TestSuite7, TestSuite8,
                    TestSuite9, TestSuite10, TestSuite11, TestSuite12,
                    TestSuite13, TestSuite14])

if __name__ == "__main__":
    sys.stdout.write("Conducting pos.exceptions module tests...\n")
    sys.stdout.flush()
    unittest.TextTestRunner(verbosity = 2).run(TestSuite)