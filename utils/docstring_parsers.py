#usr/bin/python
"""
Module pos.utils.docstring_parsers

Implements classes to parse the docstrings, i.e. extract / remove the signature,
arguments list, return value(s) and exceptions to be raised list of the method
/ function from the docstring; remove the extra indentation; extract explicitly
defined signature and arguments names, returned types and exceptions, which can
be raised.

Supported formats (if adhere to the style guidelines) are:
    * Epytext
    * reST
    * Google format for the Python docstrings
    * NumPydoc
    * Slightly modified Google format with the explicit signature definition
        in the Haskell style and explicit indication of the optional arguments
        in the Args part adopted by AA (library's author)

Classes:
    GenericParser
        EpytextParser
        reSTParser
        GoogleParser
            AAParser
        NumPydocParser

Functions:
    guess_docstyle(strDocstring):
        str -> class 'GenericParser
    indent_docstring(strDocString):
        str/, int >= 0/ -> str
"""

__version__ = "0.0.1.6"
__date__ = "25-07-2018"
__status__ = "Production"

#imports

#+ standard libraries

import sys
import collections

#+ library's modules

from pos.exceptions import CustomTypeError, CustomValueError

#classes

class GenericParser(object):
    """
    Prototype class for the docstrings parsing. Implements all required class
    methods generically. The specific format parsers as subclasses of this
    prototype must change the class attributes defining the tokens according to
    their specific format. As a prototype, only the doctest lines removal is
    supported.
    
    Designed to be used without instantiation, since all methods are class
    methods.
    
    Class attributes:
        SkipTokens: list
        SecondLineSymbol: None
        SignatureToken: None
        ArgsToken: None
    
    Class methods:
        trimDocstring(strDocstring):
            str -> str
        reduceDocstring(strDocstring):
            str -> str
        extractLinesByTokens(strDocstring, Tokens):
            str, str OR seq(str) OR None -> list(str)
        extractSignature(strDocstring):
            str -> str OR None
        extractArguments(strDocstring):
            str -> list(str)
        extractReturnedValues(strDocstring):
            str -> list(str)
        extractRaises(strDocstring):
            str -> list(str)
    
    Version 0.0.2.1
    """
    
    #class attributes
    
    SkipTokens = ['>>>']
    
    SecondLineSymbol = None
    
    SignatureToken = None
    
    ArgsToken = None
    
    ReturnTokens = None
    
    RaisesTokens = None
    
    #public class methods
    
    @classmethod
    def trimDocstring(cls, strDocstring):
        """
        Beautifies the docstring by expanding the tabs into 4 whitespaces,
        removing the excessive indentation, tailing whitespaces, and the empty
        first and tailing lines if they are empty.
        
        Signature:
            str -> str
        
        Args:
            strDocstring: string
        
        Raises:
            pos.exceptions.CustomTypeError: input is not a string
            pos.exceptions.CustomValueError: input string contains only the
                whitespace characters (including tabs and new lines) or is empty
        
        Version 0.0.1.1
        """
        if isinstance(strDocstring, basestring):
            if len(strDocstring):
                strlstBuffer = [strLine.expandtabs(4).rstrip()
                                    for strLine in strDocstring.split('\n')]
                #define minimum indentation (will be removed from all strings
                #but the first)
                iIndent= sys.maxint
                if len(strlstBuffer) > 1:
                    for strLine in strlstBuffer[1:]:
                        strStripped = strLine.lstrip()
                        if len(strStripped):
                            iIndent = min(iIndent,
                                                len(strLine) - len(strStripped))
                if iIndent == sys.maxint:
                    iIndent = 0
                #append the first line if it is not empty
                strLine = strlstBuffer[0].lstrip()
                if len(strLine):
                    strlstNewBuffer = [strLine]
                else:
                    strlstNewBuffer = []
                #remove excessive indentation
                for strLine in strlstBuffer[1:]:
                    if len(strLine) > iIndent:
                        strlstNewBuffer.append(strLine[iIndent:])
                    else:
                        strlstNewBuffer.append('')
                #remove tailing empty strings
                while len(strlstNewBuffer) and not len(strlstNewBuffer[-1]):
                    strlstNewBuffer.pop()
                #remove heading empty strings
                while len(strlstNewBuffer) and not len(strlstNewBuffer[0]):
                    strlstNewBuffer.pop(0)
                strResult = '\n'.join(strlstNewBuffer)
                if not len(strResult):
                    raise CustomValueError(strDocstring,
                                        "'contains non-whitespaces characters'")
            else:
                raise CustomValueError(strDocstring, "'not empty string'")
        else:
            raise CustomTypeError(strDocstring, basestring)
        return strResult
    
    @classmethod
    def reduceDocstring(cls, strDocstring):
        """
        First beautifies the passed docstring using class method trimDocstring()
        and then removes all documentation auto-generation related information
        according to the format specifications.
        
        Signature:
            str -> str
        
        Args:
            strDocstring: string
        
        Raises:
            pos.exceptions.CustomTypeError: input is not a string
            pos.exceptions.CustomValueError: input string contains only the
                whitespace characters (including tabs and new lines) or is empty
        
        Version 0.0.1.1
        """
        strlstTrimmed = cls.trimDocstring(strDocstring).split('\n')
        iLength = len(strlstTrimmed)
        strlstReduced = []
        iIndex = 0
        while iIndex < iLength:
            strLine = strlstTrimmed[iIndex]
            if len(cls.SkipTokens):
                strStripped = strLine.strip().lower()
                bCond1 = any(map(lambda x: strStripped.startswith(x.lower()),
                                                                cls.SkipTokens))
                if bCond1:
                    if not (cls.SecondLineSymbol is None):
                        iNextIdx = iIndex + 1
                        if iNextIdx < iLength:
                            strNextLine =strlstTrimmed[iNextIdx].strip().lower()
                            if strNextLine.startswith(
                                    cls.SecondLineSymbol.lower()):
                                iIndex = iNextIdx
                                bSkip = True
                            else:
                                bSkip = False
                        else:
                            bSkip = False
                    else:
                        bSkip = True
                    if bSkip:
                        iIndex += 1
                        if iIndex < iLength:
                            strNewLine = strlstTrimmed[iIndex].strip().lower()
                            bCond2 = any(map(
                                    lambda x: strNewLine.startswith(x.lower()),
                                        cls.SkipTokens)) #another token
                            bCond3 = not len(strNewLine) #empty line
                            bCond4 = bCond2 or bCond3
                            while not (bCond4): #skipping lines
                                iIndex += 1
                                if iIndex < iLength:
                                    strNewLine = (
                                        strlstTrimmed[iIndex].strip().lower())
                                    bCond2 = any(map(
                                        lambda x: strNewLine.startswith(
                                            x.lower()),
                                                cls.SkipTokens)) #another token
                                    bCond3 = not len(strNewLine) #empty line
                                    bCond4 = bCond2 or bCond3
                                else:
                                    bCond4 = True
                            if not len(strNewLine):
                                iIndex += 1
                    else:
                        strlstReduced.append(strLine)
                        iIndex += 1
                else:
                    strlstReduced.append(strLine)
                    iIndex += 1
            else:
                strlstReduced.append(strLine)
                iIndex += 1
        strResult = '\n'.join(strlstReduced)
        return strResult
    
    @classmethod
    def extractLinesByTokens(cls, strDocstring, Tokens):
        """
        Extracts the lines from the docstring, which are part of the
        documentation auto-generation for the specified token(s). The tokens
        themselves are removed.
        
        Signature:
            str, str OR seq(str) OR None -> list(str)
        
        Args:
            strDocstring: string
            Tokens: str OR seq(str) OR None
            
        Raises:
            pos.exceptions.CustomTypeError: the first argument is not a string
            pos.exceptions.CustomValueError: input docstring contains only the
                whitespace characters (including tabs and new lines) or is empty
            TypeError: the second argument is neither None, nor string, nor a
                sequence of strings
        
        Version 0.0.1.0
        """
        
        strlstBuffer = cls.trimDocstring(strDocstring).split('\n')
        strlstTrimmed = [strLine.strip() for strLine in strlstBuffer]
        iLength = len(strlstTrimmed)
        strlstResult = []
        if not (Tokens is None):
            bCond1 = isinstance(Tokens, basestring)
            bCond2 = (isinstance(Tokens, collections.Sequence) and
                        all(map(lambda x: isinstance(x, basestring), Tokens)))
            if not (bCond1 or bCond2):
                strMessage = ' '.join(['Tokens must be either None, string,',
                                        'or sequence of strings; got',
                                        str(type(Tokens)), 'instead'])
                raise TypeError(strMessage)
            elif bCond1:
                strlstTokens = [Tokens.lower()]
            else:
                strlstTokens = map(lambda x: x.lower(), Tokens)
            bFlag = False
            for iIdx, strLine in enumerate(strlstTrimmed):
                for strToken in strlstTokens:
                    if strLine.lower().startswith(strToken):
                        bCond1 = True
                        strFoundToken = strToken
                        break
                else:
                    bCond1 = False
                    strFoundToken = None
                bCond2 = not len(strLine)
                bCond3 = any(map(lambda x: strLine.startswith(x.lower()),
                                                                cls.SkipTokens))
                if bCond1:
                    if cls.SecondLineSymbol is None:
                        bFlag = True
                        strRest = strLine[len(strFoundToken):].strip()
                        if len(strRest):
                            strlstResult.append(strRest)
                    else:
                        if iIdx < iLength - 2:
                            if strlstTrimmed[iIdx + 1].startswith(
                                                        cls.SecondLineSymbol):
                                bFlag = True
                            else:
                                bFlag = False
                        else:
                            bFlag = False
                elif bCond2 or bCond3:
                    bFlag = False
                elif bFlag:
                    if cls.SecondLineSymbol is None:
                        strlstResult.append(strlstBuffer[iIdx])
                    elif not strLine.startswith(cls.SecondLineSymbol):
                        strlstResult.append(strlstBuffer[iIdx])
        return strlstResult
    
    @classmethod
    def extractSignature(cls, strDocstring):
        """
        Attempts to extract the explicit definition of a method's or function's
        signature from its docstring. Returns None if such information is not
        found within a proper docstring.
        
        Signature:
            str -> str OR None
        
        Args:
            strDocstring: string
            
        Raises:
            pos.exceptions.CustomTypeError: input is not a string
            pos.exceptions.CustomValueError: input string contains only the
                whitespace characters (including tabs and new lines) or is empty
        
        Version 0.0.2.0
        """
        strlstBuffer =cls.extractLinesByTokens(strDocstring, cls.SignatureToken)
        if len(strlstBuffer):
            gResult = ' '.join(map(lambda x: x.strip(), strlstBuffer))
        else:
            gResult = None
        return gResult
    
    @classmethod
    def extractArguments(cls, strDocstring):
        """
        Attempts to extract the names of the arguments of  a method or function
        from its docstring. Returns an empty list if such information is not
        found within a proper docstring.
        
        Signature:
            str -> list(str)
        
        Args:
            strDocstring: string
        
        Raises:
            pos.exceptions.CustomTypeError: input is not a string
            pos.exceptions.CustomValueError: input string contains only the
                whitespace characters (including tabs and new lines) or is empty
        
        Version 0.0.2.1
        """
        strlstBuffer = cls.extractLinesByTokens(strDocstring, cls.ArgsToken)
        strlstBuffer = filter(lambda x: ':' in x, strlstBuffer)
        strlstResult = []
        for strLine in strlstBuffer:
            strTemp = strLine.split(':')[0].strip()
            if not (strTemp in strlstResult):
                strlstResult.append(strTemp)
        return strlstResult
    
    @classmethod
    def extractReturnedValues(cls, strDocstring):
        """
        Attempts to extract the names of the types of the returned values of a
        method or function from its docstring. Returns an empty list if such
        information is not found within a proper docstring.
        
        Signature:
            str -> list(str)
        
        Args:
            strDocstring: string
        
        Raises:
            pos.exceptions.CustomTypeError: input is not a string
            pos.exceptions.CustomValueError: input string contains only the
                whitespace characters (including tabs and new lines) or is empty
        
        Version 0.0.1.0
        """
        strlstBuffer = cls.extractLinesByTokens(strDocstring, cls.ReturnTokens)
        strlstResult = [strLine.split(':')[0].strip()
                                                    for strLine in strlstBuffer]
        return strlstResult
    
    @classmethod
    def extractRaises(cls, strDocstring):
        """
        Attempts to extract the names of the exceptions which can be raised by a
        method or function from its docstring. Returns an empty list if such
        information is not found within a proper docstring.
        
        Signature:
            str -> list(str)
        
        Args:
            strDocstring: string
        
        Raises:
            pos.exceptions.CustomTypeError: input is not a string
            pos.exceptions.CustomValueError: input string contains only the
                whitespace characters (including tabs and new lines) or is empty
        
        Version 0.0.1.0
        """
        strlstBuffer = cls.extractLinesByTokens(strDocstring, cls.RaisesTokens)
        strlstBuffer = filter(lambda x: ':' in x, strlstBuffer)
        strlstResult = [strLine.split(':')[0].strip()
                                                    for strLine in strlstBuffer]
        return strlstResult

class EpytextParser(GenericParser):
    """
    Epytext format docstring parser. Subclass of  GenericParser. Supports the
    removal of the doctest lines.
    
    Designed to be used without instantiation, since all methods are class
    methods.
    
    Class attributes:
        SkipTokens: list(str)
        SecondLineSymbol: None
        SignatureToken: None
        ArgsToken: str
        ReturnTokens: str
        RaisesTokens: list(str)
    
    Class methods:
        trimDocstring(strDocstring):
            str -> str
        reduceDocstring(strDocstring):
            str -> str
        extractLinesByTokens(strDocstring, Tokens):
            str, str OR seq(str) OR None -> list(str)
        extractSignature(strDocstring):
            str -> str OR None
        extractArguments(strDocstring):
            str -> list(str)
        extractReturnedValues(strDocstring):
            str -> list(str)
        extractRaises(strDocstring):
            str -> list(str)
    
    Version 0.0.1.1
    """
    
    #class attributes
    
    SkipTokens = ['@param', '@return:', '@raise', '@author', '@version',
                    '@exception', '@throws', '@see', '@since', '@serial',
                    '@serialField', '@serialData', '@deprecated', '>>>']
    
    SecondLineSymbol = None
    
    SignatureToken = None
    
    ArgsToken = '@param'
    
    ReturnTokens = '@return:'
    
    RaisesTokens = ['@raise', '@exception', '@throws']

class reSTParser(GenericParser):
    """
    reST format docstring parser - partial, only the method / function signature
    related tokens are supported. Subclass of  GenericParser. Also supports the
    removal of the doctest lines.
    
    Designed to be used without instantiation, since all methods are class
    methods.
    
    Class attributes:
        SkipTokens: list(str)
        SecondLineSymbol: None
        SignatureToken: None
        ArgsToken: list(str)
        ReturnTokens: str
        RaisesTokens: list(str)
    
    Class methods:
        trimDocstring(strDocstring):
            str -> str
        reduceDocstring(strDocstring):
            str -> str
        extractLinesByTokens(strDocstring, Tokens):
            str, str OR seq(str) OR None -> list(str)
        extractSignature(strDocstring):
            str -> str OR None
        extractArguments(strDocstring):
            str -> list(str)
        extractReturnedValues(strDocstring):
            str -> list(str)
        extractRaises(strDocstring):
            str -> list(str)
    
    Version 0.0.1.2
    """
    
    #class attributes
    
    SkipTokens = [':param', ':parameter', ':arg', ':argument', ':key',
                    ':keyword', ':type',':returns:', ':return:', ':rtype:',
                    ':raises', ':raise', ':except', ':exception', ':var',
                    ':ivar', ':cvar', ':Example:', '>>>', '.. seealso::',
                    '.. warning::', '.. note::', '.. todo::', '.. automodule::',
                    ':members:', ':undoc-members:', ':inherited-members:',
                    ':show-inheritance:']
    
    SecondLineSymbol = None
    
    SignatureToken = None
    
    ArgsToken = [':param', ':parameter', ':arg', ':argument', ':key',
                    ':keyword', ':type']
    
    ReturnTokens = ':rtype:'
    
    RaisesTokens = [':raises', ':raise', ':except', ':exception']
    
    #public class methods
    
    @classmethod
    def extractSignature(cls, strDocstring):
        """
        Attempts to extract the implicit definition of a method's or function's
        signature from its docstring, based on the found tokens :type and the
        'hinted' lists of the parameters' names and returned type(s), see the
        methods extractArguments() and extactReturnedValues(). Returns None if
        the information on the arguments names is not found.
        
        Signature:
            str -> str OR None
        
        Args:
            strDocstring: string
            
        Raises:
            pos.exceptions.CustomTypeError: input is not a string
            pos.exceptions.CustomValueError: input string contains only the
                whitespace characters (including tabs and new lines) or is empty
        
        Version 0.0.1.0
        """
        strlstArgs = cls.extractArguments(strDocstring)
        strlstReturns = cls.extractReturnedValues(strDocstring)
        strlstTypes = cls.extractLinesByTokens(strDocstring, ':type')
        strlstTypes = filter(lambda x: ':' in x, strlstTypes)
        strlstTypes = map(lambda x: x.strip(), strlstTypes)
        strlstTypes = filter(lambda x: any(map(
                        lambda y: x.lower().startswith(y.lower()), strlstArgs)),
                            strlstTypes)
        strlstNames = [strLine.split(':')[0].strip() for strLine in strlstTypes]
        strlstTypes = [''.join(strLine.split(':')[1:]).strip()
                                                    for strLine in strlstTypes]
        if len(strlstArgs):
            if len(strlstNames):
                strlstTemp = []
                for strName in strlstArgs:
                    try:
                        iIdx = strlstNames.index(strName)
                        strlstTemp.append(strlstTypes[iIdx])
                    except ValueError:
                        strlstTemp.append('type A')
                gResult = ', '.join(strlstTemp)
            else:
                gResult = ', '.join(['type A'] * len(strlstArgs))
            if len(strlstReturns):
                strReturns = ', '.join(strlstReturns)
            else:
                strReturns = 'None'
            gResult = '{} -> {}'.format(gResult, strReturns)
        else:
            gResult = None
        return gResult

class GoogleParser(GenericParser):
    """
    Google recommended format docstring parser. Subclass of  GenericParser. Also
    supports the removal of the doctest lines.
    
    Designed to be used without instantiation, since all methods are class
    methods.
    
    Class attributes:
        SkipTokens: list(str)
        SecondLineSymbol: None
        SignatureToken: None
        ArgsToken: str
        ReturnTokens: list(str)
        RaisesTokens: str
    
    Class methods:
        trimDocstring(strDocstring):
            str -> str
        reduceDocstring(strDocstring):
            str -> str
        extractLinesByTokens(strDocstring, Tokens):
            str, str OR seq(str) OR None -> list(str)
        extractSignature(strDocstring):
            str -> str OR None
        extractArguments(strDocstring):
            str -> list(str)
        extractReturnedValues(strDocstring):
            str -> list(str)
        extractRaises(strDocstring):
            str -> list(str)
    
    Version 0.0.1.1
    """
    
    #class attributes
    
    SkipTokens = ['Args:', 'Returns:', 'Raises:', 'Attributes:', 'Note:',
                  'Yields:', 'Todo:', 'Example:','Examples:', '>>>']
    
    SecondLineSymbol = None
    
    SignatureToken = None
    
    ArgsToken = 'Args:'
    
    ReturnTokens = ['Returns:', 'Yields']
    
    RaisesTokens = 'Raises:'

class AAParser(GoogleParser):
    """
    Extends the Google recommended format docstring parser by additional tokens
    and support for the optional arguments recognition. Subclass of
    GoogleParser -|> GenericParser. Also supports the removal of the doctest
    lines.
    
    Designed to be used without instantiation, since all methods are class
    methods.
    
    Class attributes:
        SkipTokens: list(str)
        SecondLineSymbol: None
        SignatureToken: None
        ArgsToken: str
        ReturnTokens: list(str)
        RaisesTokens: str
    
    Class methods:
        trimDocstring(strDocstring):
            str -> str
        reduceDocstring(strDocstring):
            str -> str
        extractLinesByTokens(strDocstring, Tokens):
            str, str OR seq(str) OR None -> list(str)
        extractSignature(strDocstring):
            str -> str OR None
        extractArguments(strDocstring):
            str -> list(str)
        extractReturnedValues(strDocstring):
            str -> list(str)
        extractRaises(strDocstring):
            str -> list(str)
    
    Version 0.0.1.2
    """
    
    #class attributes
    
    SkipTokens = list(GoogleParser.SkipTokens)
    SkipTokens.extend(['Signature:', 'Classes:', 'Properties:', 'Methods:',
                    'Class methods:', 'Read-only properties:', 'Functions:',
                    'Class attributes:', 'Packages:', 'Modules:'])
    
    SecondLineSymbol = None
    
    SignatureToken = 'Signature:'
    
    ArgsToken = 'Args:'
    
    ReturnTokens = ['Returns:', 'Yields:']
    
    RaisesTokens = 'Raises:'
    
    #public class methods - overriden
    
    @classmethod
    def extractArguments(cls, strDocstring):
        """
        Attempts to extract the names of the arguments of  a method or function
        from its docstring. Returns an empty list if such information is not
        found within a proper docstring. Unlike the method of its super class,
        this method recognizes the optional arguments by '(optional)' token
        placed just after the argument's name and colon ':'.
        
        Signature:
            str -> list(str)
        
        Args:
            strDocstring: string
        
        Raises:
            pos.exceptions.CustomTypeError: input is not a string
            pos.exceptions.CustomValueError: input string contains only the
                whitespace characters (including tabs and new lines) or is empty
        
        Version 0.0.2.0
        """
        strlstBuffer = cls.extractLinesByTokens(strDocstring, cls.ArgsToken)
        strlstBuffer = filter(lambda x: ':' in x, strlstBuffer)
        lstResult = []
        for strLine in strlstBuffer:
            strlstTemp = strLine.split(':')
            strName = strlstTemp[0].strip()
            strRest = strlstTemp[1].strip().lower()
            if strRest.startswith('(optional)'):
                lstResult.append('/{}/'.format(strName))
            else:
                lstResult.append(strName)
        return lstResult

class NumPydocParser(GenericParser):
    """
    NumPydoc format docstring parser. Subclass of  GenericParser. N.B. does
    not support the removal of the doctest lines if they are not preceded by
    either of the tokens 'Usage' or 'Examples'; there should be no empty lines
    in the entire section.
    
    Designed to be used without instantiation, since all methods are class
    methods.
    
    Class attributes:
        SkipTokens: list(str)
        SecondLineSymbol: None
        SignatureToken: None
        ArgsToken: list(str)
        ReturnTokens: list(str)
        RaisesTokens: list(str)
    
    Class methods:
        trimDocstring(strDocstring):
            str -> str
        reduceDocstring(strDocstring):
            str -> str
        extractLinesByTokens(strDocstring, Tokens):
            str, str OR seq(str) OR None -> list(str)
        extractSignature(strDocstring):
            str -> str OR None
        extractArguments(strDocstring):
            str -> list(str)
        extractReturnedValues(strDocstring):
            str -> list(str)
        extractRaises(strDocstring):
            str -> list(str)
    
    Version 0.0.1.2
    """
    
    #class attributes
    
    SkipTokens = ['Parameters', 'Returns', 'Raises', 'Usage', 'Examples',
                  'Yields', 'See Also', 'Attributes', 'Other Parameters',
                  'Warns', 'Warnings']
    
    SecondLineSymbol = '-'
    
    SignatureToken = None
    
    ArgsToken = ['Parameters', 'Other Parameters']
    
    ReturnTokens = ['Returns', 'Yields']
    
    RaisesTokens = ['Raises', 'Warns']
    
    #'private' / helper class methods
    
    @classmethod
    def _filterLines(cls, strlstBuffer):
        """
        Returns a copy of the passed lines' buffer (as sequence of strings) with
        the lines having greater indentation than the first one being removed.
        If the buffer is empty, an empty list is returned.
        
        Signature:
            seq(str) -> list(str)
        
        Args:
            strlstBuffer: a sequence of strings
        
        Version 0.0.1.0
        """
        strlstResult = []
        if len(strlstBuffer):
            iIndent = len(strlstBuffer[0]) - len(strlstBuffer[0].lstrip())
            strlstResult = filter(
                            lambda x: (len(x) - len(x.lstrip())) <= iIndent,
                                strlstBuffer)
        return strlstResult
    
    #public class methods
    
    @classmethod
    def extractReturnedValues(cls, strDocstring):
        """
        Attempts to extract the names of the types of the returned values of a
        method or function from its docstring. Returns an empty list if such
        information is not found within a proper docstring.
        
        Signature:
            str -> list(str)
        
        Args:
            strDocstring: string
        
        Raises:
            pos.exceptions.CustomTypeError: input is not a string
            pos.exceptions.CustomValueError: input string contains only the
                whitespace characters (including tabs and new lines) or is empty
        
        Version 0.0.1.0
        """
        strlstBuffer = cls.extractLinesByTokens(strDocstring, cls.ReturnTokens)
        strlstBuffer = cls._filterLines(strlstBuffer)
        strlstResult = [strLine.split(':')[0].strip()
                                                    for strLine in strlstBuffer]
        return strlstResult
    
    @classmethod
    def extractRaises(cls, strDocstring):
        """
        Attempts to extract the names of the exceptions which can be raised by a
        method or function from its docstring. Returns an empty list if such
        information is not found within a proper docstring.
        
        Signature:
            str -> list(str)
        
        Args:
            strDocstring: string
        
        Raises:
            pos.exceptions.CustomTypeError: input is not a string
            pos.exceptions.CustomValueError: input string contains only the
                whitespace characters (including tabs and new lines) or is empty
        
        Version 0.0.1.0
        """
        strlstBuffer = cls.extractLinesByTokens(strDocstring, cls.RaisesTokens)
        strlstBuffer = cls._filterLines(strlstBuffer)
        strlstResult = [strLine.strip() for strLine in strlstBuffer]
        return strlstResult

#functions

def guess_docstyle(strDocstring):
    """
    Returns the best suited docstring parser for the given docstring based on
    its ability to effectively remove the lines related to the auto-generation
    of the documentation. The parsers are tried in the following order of
    preference: AAParser (as superset of GoogleParser), reSTParser (recommended
    by PEP287 format), EpytextParser (similar to popular javadoc format) and
    NumPydoc. If neither of these parsers is able to remove any of the such
    lines (or they are simply not present in the docstring), the default
    AAParser class is returned.
    
    Signature:
        str -> class 'GenericParser
    
    Args:
        strDocstring: string
    
    Raises:
        pos.exceptions.CustomTypeError: input is not a string
        pos.exceptions.CustomValueError: input string contains only the
            whitespace characters (including tabs and new lines) or is empty
        
    Version 0.0.1.0
    """
    strTrimmed = GenericParser.trimDocstring(strDocstring)
    iLen = len(strTrimmed)
    clsFoundParser = None
    for clsParser in [AAParser, reSTParser, EpytextParser, NumPydocParser]:
        strReduced = clsParser.reduceDocstring(strDocstring)
        iNewLen = len(strReduced)
        if iNewLen < iLen:
            clsFoundParser = clsParser
            iLen = iNewLen
    if clsFoundParser is None:
        clsFoundParser = AAParser
    return clsFoundParser

def indent_docstring(strDocstring, iTabs = 1):
    """
    Prepends each line in the passed docstring (may be already trimmed) with the
    4 times the specified number (second, optional argument) number of spaces.
    
    Signature:
        str/, int >= 0/ -> str
    
    Args:
        strDocstring: string
        iTabs: (optional), non negative integer, amount of 'tabs' to be inserted
            into the beginning of each line (each 'tab' is replaced by 4 space
            characters); default value is 1 (-> 4 spaces)
    
    Raises:
        pos.exceptions.CustomTypeError: the first argument is not a string, or
            the second argument is not an integer
        pos.exceptions.CustomValueError: the first argument is an empty string,
            or the second argument is a negative integer
    
    Version 0.0.1.0
    """
    if not isinstance(strDocstring, basestring):
        raise CustomTypeError(strDocstring, basestring)
    elif not len(strDocstring):
        raise CustomValueError(strDocstring, "'not empty string'")
    if not isinstance(iTabs, int):
        raise CustomTypeError(iTabs, int)
    elif iTabs < 0:
        raise CustomValueError(iTabs, "'not negative'")
    strlstTemp = strDocstring.split('\n')
    strPrefix = " " * (4 * iTabs)
    strResult = '\n'.join([''.join([strPrefix, strLine])
                                                    for strLine in strlstTemp])
    return strResult