#usr/bin/python
"""
Module pos.tests.utils.traceback_ut

Implements unit testing of the module pos.utils.traceback.
"""

__version__ = "0.0.1.0"
__date__ = "19-06-2018"
__status__ = "Testing"

#imports

#+ standard libraries

import sys
import unittest

#+ my libraries

import pos.utils.traceback as testmodule

#helper functions

def inner():
    """
    The inner function in the chain outer() -> middle() -> inner(), which,
    actually, raises the ValueError exception.
    """
    raise ValueError()

def middle():
    """
    The middle function in the chain outer() -> middle() -> inner(), which leads
    to the ValueError exception.
    """
    return inner()

def outer():
    """
    The outer function in the chain outer() -> middle() -> inner(), which leads
    to the ValueError exception.
    """
    return middle()

#classes

#+ test cases

class Test_StackTraceback(unittest.TestCase):
    """
    Test cases for the class pos.utils.traceback.StackTraceback
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        cls.TestClass = testmodule.StackTraceback
        cls.RequiredClassFields = ['ConsoleWidth', 'ContextLenght']
        cls.RequiredClassFieldsTypes = [int, int]
        cls.RequiredProperties = ['CallChain', 'Info']
        cls.RequiredPropertiesTypes = [list, str]
    
    def test_ClassHasAttributes(self):
        """
        Checks that the class has all required class attributes and properties.
        """
        for strItem in self.RequiredClassFields:
            strMessage = '{} doesn`t have attribute {}'.format(self.TestClass,
                                                                        strItem)
            self.assertTrue(hasattr(self.TestClass, strItem), strMessage)
        for strItem in self.RequiredProperties:
            strMessage = '{} doesn`t have attribute {}'.format(self.TestClass,
                                                                        strItem)
            self.assertTrue(hasattr(self.TestClass, strItem), strMessage)
    
    def test_ClassAttributesTypes(self):
        """
        Checks that all required attributes of the class are of the proper types
        """
        for iIdx, strItem in enumerate(self.RequiredClassFields):
            gType = self.RequiredClassFieldsTypes[iIdx]
            strMessage = 'Attribute {}.{} is not of type {}'.format(
                                        self.TestClass, strItem, gType)
            self.assertIsInstance(getattr(self.TestClass, strItem), gType,
                                                                    strMessage)
    
    def test_InstanceHasAttributes(self):
        """
        Checks that an instance of the class has all required attributes and
        properties.
        """
        objTest = self.TestClass()
        for strItem in self.RequiredClassFields:
            strMessage = '{} doesn`t have attribute {}'.format(self.TestClass,
                                                                        strItem)
            self.assertTrue(hasattr(objTest, strItem), strMessage)
        for strItem in self.RequiredProperties:
            strMessage = '{} doesn`t have attribute {}'.format(self.TestClass,
                                                                        strItem)
            self.assertTrue(hasattr(objTest, strItem), strMessage)
        del objTest
    
    def test_InstanceAttributesTypes(self):
        """
        Checks that all required properties return the proper types.
        """
        objTest = self.TestClass()
        for iIdx, strItem in enumerate(self.RequiredClassFields):
            gType = self.RequiredClassFieldsTypes[iIdx]
            strMessage = 'Attribute {}.{} is not of type {}'.format(
                                        self.TestClass, strItem, gType)
            self.assertIsInstance(getattr(objTest, strItem), gType,
                                                                    strMessage)
        for iIdx, strItem in enumerate(self.RequiredProperties):
            gType = self.RequiredPropertiesTypes[iIdx]
            strMessage = 'Property {}.{} doesn`t return type {}'.format(
                                        self.TestClass, strItem, gType)
            self.assertIsInstance(getattr(objTest, strItem), gType, strMessage)
        del objTest
    
    def test_CallChain(self):
        """
        Checks the correctness of the callers chain returned by the property
        CallChain.
        """
        objTest = self.TestClass()
        lstCallChain = objTest.CallChain
        self.assertEqual(lstCallChain[0], '__main__',
                         'top of the stack - {} not "__main__"'.format(
                                                            lstCallChain[0]))
        #must start always at the top level
        self.assertEqual(lstCallChain[-1],
            '{}.{}.test_CallChain'.format(__name__, self.__class__.__name__),
                'bottom of the stack - {} not this method'.format(
                                                            lstCallChain[-2]))
        # must be called from this method
        objTestNew = self.TestClass(iSkip = 2)
        lstCallChainNew = objTestNew.CallChain
        self.assertListEqual(lstCallChainNew, lstCallChain[:-2])
        #the stack trace must be the same at the top but 2 elements shorter
        del objTest
        del objTestNew
    
    def test_Info(self):
        """
        Checks partially the correctness of the result returned by the Info
        property - only the total number of the lines, the source code lines
        truncation and that the callers names are in the first line per frame
        trace and are fully qualified.
        """
        iMaxWidth = 15
        iNumberLines = 5
        iLinesPerFrame = iNumberLines + 2
        objTest = self.TestClass(iContext = iNumberLines, iWidth = iMaxWidth)
        lstCallChain = objTest.CallChain
        lstTraceback = objTest.Info.split('\n')
        self.assertEqual(len(lstCallChain) * iLinesPerFrame, len(lstTraceback),
            'number of lines is not number of frames x(2+code lines per frame)')
        for iFrame in range(len(lstCallChain)):
            iOffset = iFrame * iLinesPerFrame
            self.assertNotEqual(
                lstTraceback[iOffset].find(lstCallChain[iFrame]), -1,
                'Caller not found in the 1st line of the frame trace {}'.format(
                    lstTraceback[iOffset]))
            for iLineOffet in range(iNumberLines):
                strLine = lstTraceback[iOffset + 2 + iLineOffet]
                iLength = len(strLine)
                self.assertLessEqual(iLength, iMaxWidth,
                                    'code line {} is too long'.format(strLine))
        del objTest

class Test_ExceptionTraceback(Test_StackTraceback):
    """
    Test cases for the class pos.utils.traceback.ExceptionTraceback. Extends
    the unit test class Test_StackTraceback.
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        super(Test_ExceptionTraceback, cls).setUpClass()
        cls.TestClass = testmodule.ExceptionTraceback
    
    def test_CallChain(self):
        """
        Checks the correctness of the callers chain returned by the property
        CallChain.
        """
        try:
            outer()
        except ValueError:
            pass
        objTest = self.TestClass()
        lstCallChain = objTest.CallChain
        #must contain exactly 4 elements
        self.assertEqual(len(lstCallChain), 4,
                'traceback size must be 4 not {}'.format(len(lstCallChain)))
        #must start always in this method
        self.assertEqual(lstCallChain[0],
            '{}.{}.test_CallChain'.format(__name__, self.__class__.__name__),
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
        objTestNew = self.TestClass(iSkip = 2)
        lstCallChainNew = objTestNew.CallChain
        self.assertListEqual(lstCallChainNew, lstCallChain[:-2])
        #the stack trace must be the same at the top but 2 elements shorter
        del objTest
        del objTestNew
    
    def test_Info(self):
        """
        Checks partially the correctness of the result returned by the Info
        property - only the total number of the lines, the source code lines
        truncation and that the callers names are in the first line per frame
        trace and are fully qualified.
        """
        try:
            outer()
        except ValueError:
            super(Test_ExceptionTraceback, self).test_Info()

#+ test suites

TestSuite1 = unittest.TestLoader().loadTestsFromTestCase(Test_StackTraceback)
TestSuite2 = unittest.TestLoader().loadTestsFromTestCase(
                                                    Test_ExceptionTraceback)
TestSuite = unittest.TestSuite()
TestSuite.addTests([TestSuite1, TestSuite2])

if __name__ == "__main__":
    sys.stdout.write("Conducting pos.utils.traceback module tests...\n")
    sys.stdout.flush()
    unittest.TextTestRunner(verbosity = 2).run(TestSuite)