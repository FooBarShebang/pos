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
    
    def test_IsSubclass(self):
        """
        Checks ascending 'IS A' relations of this class including the virtual
        sub classes as well as 'HAS A' checks (composition).
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
        sub classes as well as 'HAS A' checks (composition).
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