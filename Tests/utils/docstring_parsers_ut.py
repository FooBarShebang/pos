#usr/bin/python
"""
Module pos.tests.utils.docstring_parsers_ut

Implements unit testing of the module pos.utils.docstring_parsers.
"""

__version__ = "0.0.1.0"
__date__ = "18-07-2018"
__status__ = "Testing"

#imports

#+ standard libraries

import sys
import unittest

#+ my libraries

import pos.utils.docstring_parsers as testmodule

from pos.exceptions import CustomTypeError, CustomValueError

#helper functions

def epytext_style(Name, *args, **kwargs):
    """
    Epytext / javadoc style docstring
    
    @param Name: string, name of something
    @param *args: (optional), any amount of arguments of any types, not really
    used
    @param **kwargs: (optional), any amount of arguments of any types, not
    really used
    @return: None
    @raise None: no exceptions
    
    >>>epytext_style('whatever')
    None
    
    Version 0.0.1.0
    """
    return None

def rest_style(Name, *args, **kwargs):
    """
    reST style docstring
    
    :param Name: string, name of something
    :param *args: (optional), any amount of arguments of any types, not really
        used
    :param **kwargs: (optional), any amount of arguments of any types, not
        really used
    :returns: None
    :raises None: no exceptions
    
    >>>rest_style('whatever')
    None
    
    Version 0.0.1.0
    """
    return None

def google_style(Name, *args, **kwargs):
    """
    Google / AA style docstring
    
    Signature:
        str, /type A, type B/ -> None
    
    Args:
        Name: string, name of something
        *args: (optional), any amount of arguments of any types, not really used
        **kwargs: (optional), keyword, any amount of arguments of any types, not
            really used
    
    Returns:
        None
    
    Raises:
        no exceptions
    
    >>>google_style('whatever')
    None
    
    Version 0.0.1.0
    """
    return None

def numpydoc_style(Name, *args, **kwargs):
    """
    NumPydoc style docstring
    
    Parameters
    ----------
    Name : string, name of something
    *args : (optional), any amount of arguments of any types
        not really used
    **kwargs : (optional), keyword, any amount of arguments of any types
        not really used
    
    Returns
    -------
    None
        nothing is returned
    
    Raises
    ------
    None
        no exceptions
    
    Usage
    -----
    >>>numpydoc_style('whatever')
    None
    
    Version 0.0.1.0
    """
    return None

#globals

dictTests = {
    "Epytext" : {
        "function" : epytext_style,
        "trimmed" : '\n'.join([
            "Epytext / javadoc style docstring", "",
            "@param Name: string, name of something",
            "@param *args: (optional), any amount of arguments of any types, not really",
            "used",
            "@param **kwargs: (optional), any amount of arguments of any types, not",
            "really used",
            "@return: None",
            "@raise None: no exceptions", "",
            ">>>epytext_style('whatever')",
            "None", "",
            "Version 0.0.1.0"
            ]),
        "reduced" : '\n'.join([
            "Epytext / javadoc style docstring", "",
            "Version 0.0.1.0"
            ]),
        "signature" : None,
        "arguments" : ['Name', '*args', '**kwargs'],
        "parser" : testmodule.EpytextParser
        },
    "reST" : {
        "function" : rest_style,
        "trimmed" : '\n'.join([
            "reST style docstring", "",
            ":param Name: string, name of something",
            ":param *args: (optional), any amount of arguments of any types, not really",
            "    used",
            ":param **kwargs: (optional), any amount of arguments of any types, not",
            "    really used",
            ":returns: None",
            ":raises None: no exceptions", "",
            ">>>rest_style('whatever')",
            "None", "",
            "Version 0.0.1.0"
            ]),
        "reduced" : '\n'.join([
            "reST style docstring", "",
            "Version 0.0.1.0"
            ]),
        "signature" : None,
        "arguments" : ['Name', '*args', '**kwargs'],
        "parser" : testmodule.reSTParser
        },
    "Google" : {
        "function" : google_style,
        "trimmed" : '\n'.join([
            "Google / AA style docstring", "",
            "Signature:",
            "    str, /type A, type B/ -> None", "",
            "Args:",
            "    Name: string, name of something",
            "    *args: (optional), any amount of arguments of any types, not really used",
            "    **kwargs: (optional), keyword, any amount of arguments of any types, not",
            "        really used", "",
            "Returns:",
            "    None", "",
            "Raises:",
            "    no exceptions", "",
            ">>>google_style('whatever')",
            "None", "",
            "Version 0.0.1.0"
            ]),
        "reduced" : '\n'.join([
            "Google / AA style docstring", "", "Signature:",
            "    str, /type A, type B/ -> None", "",
            "Version 0.0.1.0"
            ]),
        "signature" : None,
        "arguments" : ['Name', '*args', '**kwargs'],
        "parser" : testmodule.AAParser
        },
    "AA" : {
        "function" : google_style,
        "trimmed" : '\n'.join([
            "Google / AA style docstring", "",
            "Signature:",
            "    str, /type A, type B/ -> None", "",
            "Args:",
            "    Name: string, name of something",
            "    *args: (optional), any amount of arguments of any types, not really used",
            "    **kwargs: (optional), keyword, any amount of arguments of any types, not",
            "        really used", "",
            "Returns:",
            "    None", "",
            "Raises:",
            "    no exceptions", "",
            ">>>google_style('whatever')",
            "None", "",
            "Version 0.0.1.0"
            ]),
        "reduced" : '\n'.join([
            "Google / AA style docstring", "",
            "Version 0.0.1.0"
            ]),
        "signature" : "str, /type A, type B/ -> None",
        "arguments" : ['Name', '/*args/', '/**kwargs/'],
        "parser" : testmodule.AAParser
        },
    "NumPy" : {
        "function" : numpydoc_style,
        "trimmed" : '\n'.join([
            "NumPydoc style docstring", "",
            "Parameters", "----------",
            "Name : string, name of something",
            "*args : (optional), any amount of arguments of any types",
            "    not really used",
            "**kwargs : (optional), keyword, any amount of arguments of any types",
            "    not really used", "",
            "Returns", "-------",
            "None", "    nothing is returned", "",
            "Raises", "------", 
            "None", "    no exceptions", "",
            "Usage", "-----",
            ">>>numpydoc_style('whatever')",
            "None", "",
            "Version 0.0.1.0"
            ]),
        "reduced" : '\n'.join([
            "NumPydoc style docstring", "",
            "Version 0.0.1.0"
            ]),
        "signature" : None,
        "arguments" : ['Name', '*args', '**kwargs'],
        "parser" : testmodule.NumPydocParser
        }
    }

#classes

#+ test cases

class Test_GenericParser(unittest.TestCase):
    """
    Test cases for the class pos.utils.docstring_parsers.GenericParser
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        cls.TestClass = testmodule.GenericParser
        cls.TestCases = ["Epytext", 'reST', 'Google', 'NumPy']
    
    def test_trimDocstring(self):
        """
        Test the method trimDocstring() inherited from the GenericParser class -
        i.e. removal of the excessive indentation, tailing whitespaces (for
        each line) and heading and tailing empty lines.
        Also tests that the proper exceptions are raised with the wrong input.
        """
        for strCase in self.TestCases:
            funcSource = dictTests[strCase]["function"]
            strSource = funcSource.__doc__
            strResult = dictTests[strCase]["trimmed"]
            strMessage = 'Wrong result of trimDocstring() method for {}'.format(
                                                                        strCase)
            strTest = self.TestClass.trimDocstring(strSource)
            self.assertEqual(strTest, strResult, strMessage)
            with self.assertRaises(CustomTypeError):
                self.TestClass.trimDocstring(1) #not a string
            with self.assertRaises(CustomValueError):
                self.TestClass.trimDocstring('') #empty string
            with self.assertRaises(CustomValueError):
                self.TestClass.trimDocstring(' \n\t\n')
                #string with only whitespaces

class Test_EpytextParser(Test_GenericParser):
    """
    Test cases for the class pos.utils.docstring_parsers.EpytextParser
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        cls.TestClass = testmodule.EpytextParser
        cls.TestCases = ["Epytext"]
    
    def test_reduceDocstring(self):
        """
        Test the method reduceDocstring() inherited from the GenericParser class
        - i.e. removal of the excessive indentation, tailing whitespaces (for
        each line) and heading and tailing empty lines, as well as of all lines
        related to the automated documentation generation.
        Also tests that the proper exceptions are raised with the wrong input.
        """
        for strCase in self.TestCases:
            funcSource = dictTests[strCase]["function"]
            strSource = funcSource.__doc__
            strResult = dictTests[strCase]["reduced"]
            strMessage = ' '.join(['Wrong result of reduceDocstring() method',
                                   'for', strCase, 'format'])
            strTest = self.TestClass.reduceDocstring(strSource)
            self.assertEqual(strTest, strResult, strMessage)
            with self.assertRaises(CustomTypeError):
                self.TestClass.reduceDocstring(1) #not a string
            with self.assertRaises(CustomValueError):
                self.TestClass.reduceDocstring('') #empty string
            with self.assertRaises(CustomValueError):
                self.TestClass.reduceDocstring(' \n\t\n')
                #string with only whitespaces
    
    def test_extractSignature(self):
        """
        Test the method extractSignature() inherited from the GenericParser
        class - i.e. extraction of the explicitly defined signature (not for
        all formats).
        Also tests that the proper exceptions are raised with the wrong input.
        """
        for strCase in self.TestCases:
            funcSource = dictTests[strCase]["function"]
            strSource = funcSource.__doc__
            strResult = dictTests[strCase]["signature"]
            strMessage = ' '.join(['Wrong result of extractSignature() method',
                                   'for', strCase, 'format'])
            strTest = self.TestClass.extractSignature(strSource)
            if not (strResult is None):
                self.assertEqual(strTest, strResult, strMessage)
            else:
                self.assertIsNone(strTest, strMessage)
            with self.assertRaises(CustomTypeError):
                self.TestClass.extractSignature(1) #not a string
            with self.assertRaises(CustomValueError):
                self.TestClass.extractSignature('') #empty string
            with self.assertRaises(CustomValueError):
                self.TestClass.extractSignature(' \n\t\n')
                #string with only whitespaces
    
    def test_extractArguments(self):
        """
        Test the method extractArguments() inherited from the GenericParser
        class - i.e. extraction of the explicitly defined signature (not for
        all formats).
        Also tests that the proper exceptions are raised with the wrong input.
        """
        for strCase in self.TestCases:
            funcSource = dictTests[strCase]["function"]
            strSource = funcSource.__doc__
            strResult = dictTests[strCase]["arguments"]
            strMessage = ' '.join(['Wrong result of extractArguments() method',
                                   'for', strCase, 'format'])
            strTest = self.TestClass.extractArguments(strSource)
            self.assertEqual(strTest, strResult, strMessage)
            with self.assertRaises(CustomTypeError):
                self.TestClass.extractArguments(1) #not a string
            with self.assertRaises(CustomValueError):
                self.TestClass.extractArguments('') #empty string
            with self.assertRaises(CustomValueError):
                self.TestClass.extractArguments(' \n\t\n')
                #string with only whitespaces

class Test_reSTParser(Test_EpytextParser):
    """
    Test cases for the class pos.utils.docstring_parsers.reSTParser
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        cls.TestClass = testmodule.reSTParser
        cls.TestCases = ["reST"]

class Test_GoogleParser(Test_EpytextParser):
    """
    Test cases for the class pos.utils.docstring_parsers.GoogleParser
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        cls.TestClass = testmodule.GoogleParser
        cls.TestCases = ["Google"]

class Test_AAParser(Test_EpytextParser):
    """
    Test cases for the class pos.utils.docstring_parsers.AAParser
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        cls.TestClass = testmodule.AAParser
        cls.TestCases = ["AA"]

class Test_NumPydocParser(Test_EpytextParser):
    """
    Test cases for the class pos.utils.docstring_parsers.NumPydocParser
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        cls.TestClass = testmodule.NumPydocParser
        cls.TestCases = ["NumPy"]

class Test_guess_docstyle(unittest.TestCase):
    """
    Test cases for the function pos.utils.docstring_parsers.guess_docstyle().
    """
    
    def test_guess_docstyle(self):
        """
        Checks that the function guess_docstyle() guesses the docstring style
        for the auto-generation of documentation correctly.
        Also tests that the proper exceptions are raised with the wrong input.
        """
        for strCase in dictTests:
            funcSource = dictTests[strCase]["function"]
            strSource = funcSource.__doc__
            clsResult = dictTests[strCase]["parser"]
            strMessage = ' '.join(['Wrong result of guess_docstyle() function',
                                   'for', strCase, 'format'])
            clsTest = testmodule.guess_docstyle(strSource)
            self.assertIs(clsTest, clsResult, strMessage)
        clsTest = testmodule.guess_docstyle(self.__doc__)
        clsResult = testmodule.AAParser
        strMessage = ' '.join(['Wrong result of guess_docstyle() function',
                                   'for an undefined format'])
        self.assertIs(clsTest, clsResult, strMessage)
        with self.assertRaises(CustomTypeError):
            testmodule.guess_docstyle(1) #not a string
        with self.assertRaises(CustomValueError):
            testmodule.guess_docstyle('') #empty string
        with self.assertRaises(CustomValueError):
            testmodule.guess_docstyle(' \n\t\n')
                #string with only whitespaces

class Test_indent_docstring(unittest.TestCase):
    """
    Test cases for the function pos.utils.docstring_parsers.indent_docstring().
    """
    
    def test_indent_docstring(self):
        """
        Checks that the function indent_docstring() properly indents a docstring
        - i.e. each line is prefixed by the same amount of white spaces (4, 8,
        etc.). Must not change the docstring if zero indentation is passed.
        """
        strInput = 'test\n    docstring\n\nexample'
        strOutput = '    test\n        docstring\n    \n    example'
        self.assertEqual(strOutput, testmodule.indent_docstring(strInput))
        strOutput = '\n'.join(['        test', '            docstring',
                               '        ', '        example'])
        self.assertEqual(strOutput, testmodule.indent_docstring(strInput, 2))
        strOutput = '\n'.join(['            test', '                docstring',
                               '            ', '            example'])
        self.assertEqual(strOutput, testmodule.indent_docstring(strInput, 3))

        self.assertEqual(strInput, testmodule.indent_docstring(strInput,
                                                                    iTabs = 0))
        for strCase in dictTests:
            funcSource = dictTests[strCase]["function"]
            strSource = '\n'.join(funcSource.__doc__.split('\n')[1:-1])
            strInput = dictTests[strCase]["trimmed"]
            strMessage =' '.join(['Wrong result of indent_docstring() function',
                                   'for', strCase, 'format'])
            strTest = testmodule.indent_docstring(strInput)
            self.assertEqual(strSource, strTest, strMessage)
    
    def test_indent_docstring_raises(self):
        """
        Checks that the function raises proper exceptions with improper input.
        """
        with self.assertRaises(CustomTypeError):
            testmodule.indent_docstring(1) #not a string - first argument
        with self.assertRaises(CustomValueError):
            testmodule.indent_docstring('') #first argument is an empty string
        with self.assertRaises(CustomTypeError):
            testmodule.indent_docstring('1', "1") #not an int - second argument
        with self.assertRaises(CustomValueError):
            testmodule.indent_docstring('1', -1) #second argument is negative

#+ test suites

TestSuite1 = unittest.TestLoader().loadTestsFromTestCase(Test_GenericParser)
TestSuite2 = unittest.TestLoader().loadTestsFromTestCase(Test_EpytextParser)
TestSuite3 = unittest.TestLoader().loadTestsFromTestCase(Test_reSTParser)
TestSuite4 = unittest.TestLoader().loadTestsFromTestCase(Test_GoogleParser)
TestSuite5 = unittest.TestLoader().loadTestsFromTestCase(Test_AAParser)
TestSuite6 = unittest.TestLoader().loadTestsFromTestCase(Test_NumPydocParser)
TestSuite7 = unittest.TestLoader().loadTestsFromTestCase(Test_guess_docstyle)
TestSuite8 = unittest.TestLoader().loadTestsFromTestCase(Test_indent_docstring)

TestSuite = unittest.TestSuite()
TestSuite.addTests([TestSuite1, TestSuite2, TestSuite3, TestSuite4, TestSuite5,
                        TestSuite6, TestSuite7, TestSuite8])

if __name__ == "__main__":
    sys.stdout.write("Conducting pos.utils.docstring_parsers module tests...\n")
    sys.stdout.flush()
    unittest.TextTestRunner(verbosity = 2).run(TestSuite)