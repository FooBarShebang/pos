#usr/bin/python
"""
Module pos.utils.docstring_parsers

Implements classes to parse the docstrings, i.e. extract / remove the signature
of the method / function from the docstring, remove the extra indentation,
extract explicitly defined signature and arguments names.

Supported formats (if adhere to the style guidelines) are:
    * Epytext
    * reST
    * Google format for the Python docstrings
    * Numpydoc
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
"""

__version__ = "0.0.1.1"
__date__ = "11-07-2018"
__status__ = "Testing"

#imports

#+ standard libraries

import sys

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
        extractSignature(strDocstring):
            str -> str OR None
        extractArguments(strDocstring):
            str -> list(str)
    
    Version 0.0.1.1
    """
    
    #class attributes
    
    SkipTokens = ['>>>']
    
    SecondLineSymbol = None
    
    SignatureToken = None
    
    ArgsToken = None
    
    #public class methods
    
    @classmethod
    def trimDocstring(cls, strDocstring):
        """
        Beautifies the docstring by expanding the tabs into 4 whitespaces,
        removing the excessive indentation, tailing whitespaces, and the empty
        first and tailing lines if they are empty.
        
        Signature:
            str -> str
        
        Raises:
            pos.exceptions.CustomTypeError: input is not a string
            pos.exceptions.CustomValueError: input string contains only the
                whitespace characters (including tabs and new lines) or is empty
        
        Version 0.0.1.0
        """
        strResult = ''
        if isinstance(strDocstring, basestring):
            if len(strDocstring):
                strlstBuffer = [strLine.expandtabs(4).rstrip()
                                    for strLine in strDocstring.split('\n')]
                #define minimum indentation (will be removed from all strings
                #but the first)
                if len(strlstBuffer) > 1:
                    iIndent= sys.maxint
                    for strLine in strlstBuffer[1:]:
                        strStripped = strLine.lstrip()
                        if len(strStripped):
                            iIndent = min(iIndent,
                                                len(strLine) - len(strStripped))
                #append the first line if it is not empty
                strLine = strlstBuffer[0].lstrip()
                if len(strLine):
                    strlstNewBuffer = [strLine]
                else:
                    strlstNewBuffer = []
                #remove excessive indentation
                for strLine in strlstBuffer[1:]:
                    if iIndent < sys.maxint:
                        if len(strLine) > iIndent:
                            strlstNewBuffer.append(strLine[iIndent:])
                        else:
                            strlstNewBuffer.append('')
                    else:
                        strlstNewBuffer.append(strLine)
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
        
        Raises:
            pos.exceptions.CustomTypeError: input is not a string
            pos.exceptions.CustomValueError: input string contains only the
                whitespace characters (including tabs and new lines) or is empty
        
        Version 0.0.1.0
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
                        else:
                            bCond4 = True
                        while not (bCond4): #skipping lines
                            iIndex += 1
                            if iIndex < iLength:
                                strNewLine=strlstTrimmed[iIndex].strip().lower()
                                bCond2 = any(map(
                                    lambda x: strNewLine.startswith(x.lower()),
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
    def extractSignature(cls, strDocstring):
        """
        Attempts to extract the explicit definition of a method's or function's
        signature from its docstring. Returns None if such information is not
        found within a proper docstring.
        
        Signature:
            str -> str OR None
        
        Raises:
            pos.exceptions.CustomTypeError: input is not a string
            pos.exceptions.CustomValueError: input string contains only the
                whitespace characters (including tabs and new lines) or is empty
        
        Version 0.0.1.0
        """
        strlstTrimmed = [strLine.strip()
                    for strLine in cls.trimDocstring(strDocstring).split('\n')]
        iLength = len(strlstTrimmed)
        if cls.SignatureToken is None:
            gResult = None
        else:
            strlstBuffer = []
            bFlag = False
            for iIdx, strLine in enumerate(strlstTrimmed):
                bCond1 = strLine.lower().startswith(cls.SignatureToken.lower())
                bCond2 = not len(strLine)
                bCond3 = any(map(lambda x: strLine.startswith(x.lower()),
                                                                cls.SkipTokens))
                if bCond1:
                    if cls.SecondLineSymbol is None:
                        bFlag = True
                        strRest = strLine[len(cls.SignatureToken):].strip()
                        if len(strRest):
                            strlstBuffer.append(strRest)
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
                    if bFlag:
                        break
                elif bFlag:
                    if cls.SecondLineSymbol is None:
                        strlstBuffer.append(strLine)
                    elif not strLine.startswith(cls.SecondLineSymbol):
                        strlstBuffer.append(strLine)
            if len(strlstBuffer):
                gResult = ' '.join(strlstBuffer)
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
        
        Raises:
            pos.exceptions.CustomTypeError: input is not a string
            pos.exceptions.CustomValueError: input string contains only the
                whitespace characters (including tabs and new lines) or is empty
        
        Version 0.0.1.0
        """
        strlstTrimmed = [strLine.strip()
                    for strLine in cls.trimDocstring(strDocstring).split('\n')]
        iLength = len(strlstTrimmed)
        if cls.ArgsToken is None:
            lstResult = []
        else:
            strlstBuffer = []
            bFlag = False
            for iIdx, strLine in enumerate(strlstTrimmed):
                bCond1 = strLine.lower().startswith(cls.ArgsToken.lower())
                bCond2 = not len(strLine)
                bCond3 = any(map(lambda x: strLine.startswith(x.lower()),
                                                                cls.SkipTokens))
                if bCond1:
                    if cls.SecondLineSymbol is None:
                        bFlag = True
                        strRest = strLine[len(cls.ArgsToken):].strip()
                        if len(strRest): #reST, Epytext and alike - in same line
                            strlstBuffer.append(strRest)
                            bFlag = False
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
                elif bFlag: #Google, Numpydoc and alike
                    if cls.SecondLineSymbol is None:
                        if ':' in strLine:
                            strlstBuffer.append(strLine)
                    elif not strLine.startswith(cls.SecondLineSymbol):
                        if ':' in strLine:
                            strlstBuffer.append(strLine)
            strlstBuffer = filter(lambda x: ':' in x, strlstBuffer)
            lstResult = [strLine.split(':')[0].strip()
                                                    for strLine in strlstBuffer]
        return lstResult

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
    
    Class methods:
        trimDocstring(strDocstring):
            str -> str
        reduceDocstring(strDocstring):
            str -> str
        extractSignature(strDocstring):
            str -> str OR None
        extractArguments(strDocstring):
            str -> list(str)
    
    Version 0.0.1.1
    """
    
    #class attributes
    
    SkipTokens = ['@param', '@return', '@raise', '@author', '@version',
                    '@exception', '@throws', '@see', '@since', '@serial',
                    '@serialField', '@serialData', '@deprecated', '>>>']
    
    SecondLineSymbol = None
    
    SignatureToken = None
    
    ArgsToken = '@param'

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
        ArgsToken: str
    
    Class methods:
        trimDocstring(strDocstring):
            str -> str
        reduceDocstring(strDocstring):
            str -> str
        extractSignature(strDocstring):
            str -> str OR None
        extractArguments(strDocstring):
            str -> list(str)
    
    Version 0.0.1.1
    """
    
    #class attributes
    
    SkipTokens = [':param', ':returns:', ':raises', '>>>']
    
    SecondLineSymbol = None
    
    SignatureToken = None
    
    ArgsToken = ':param'

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
    
    Class methods:
        trimDocstring(strDocstring):
            str -> str
        reduceDocstring(strDocstring):
            str -> str
        extractSignature(strDocstring):
            str -> str OR None
        extractArguments(strDocstring):
            str -> list(str)
    
    Version 0.0.1.1
    """
    
    #class attributes
    
    SkipTokens = ['Args:', 'Returns:', 'Raises:', 'Attributes:', '>>>']
    
    SecondLineSymbol = None
    
    SignatureToken = None
    
    ArgsToken = 'Args:'

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
    
    Class methods:
        trimDocstring(strDocstring):
            str -> str
        reduceDocstring(strDocstring):
            str -> str
        extractSignature(strDocstring):
            str -> str OR None
        extractArguments(strDocstring):
            str -> list(str)
    
    Version 0.0.1.1
    """
    
    #class attributes
    
    SkipTokens = list(GoogleParser.SkipTokens)
    SkipTokens.extend(['Signature:', 'Classes:', 'Properties:', 'Methods:',
                    'Class methods:', 'Read-only properties:', 'Functions:',
                    'Class attributes:', 'Packages:', 'Modules:'])
    
    SecondLineSymbol = None
    
    SignatureToken = 'Signature:'
    
    ArgsToken = 'Args:'
    
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
        
        Raises:
            pos.exceptions.CustomTypeError: input is not a string
            pos.exceptions.CustomValueError: input string contains only the
                whitespace characters (including tabs and new lines) or is empty
        
        Version 0.0.1.0
        """
        strlstTrimmed = [strLine.strip()
                    for strLine in cls.trimDocstring(strDocstring).split('\n')]
        lstResult = []
        if not (cls.ArgsToken is None):
            strlstBuffer = []
            bFlag = False
            for strLine in strlstTrimmed:
                bCond1 = strLine.lower().startswith(cls.ArgsToken.lower())
                bCond2 = not len(strLine)
                bCond3 = any(map(lambda x: strLine.startswith(x.lower()),
                                                                cls.SkipTokens))
                if bCond1:
                    bFlag = True
                elif bCond2 or bCond3:
                    bFlag = False
                elif bFlag and (':' in strLine):
                    strlstBuffer.append(strLine)
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
        ArgsToken: str
    
    Class methods:
        trimDocstring(strDocstring):
            str -> str
        reduceDocstring(strDocstring):
            str -> str
        extractSignature(strDocstring):
            str -> str OR None
        extractArguments(strDocstring):
            str -> list(str)
    
    Version 0.0.1.1
    """
    
    #class attributes
    
    SkipTokens = ['Parameters', 'Returns', 'Raises', 'Usage', 'Examples',
                  'Yields', 'See Also', 'Attributes']
    
    SecondLineSymbol = '-'
    
    SignatureToken = None
    
    ArgsToken = 'Parameters'

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

#testing - temporary

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


if __name__ == '__main__':
    try:
        #Epytext / javadoc
        #strDocstring = epytext_style.__doc__
        #rest
        #strDocstring = rest_style.__doc__
        #Google /AA
        strDocstring = google_style.__doc__
        #Numpydoc
        #strDocstring = numpydoc_style.__doc__
        print 'Original docstring\n'
        print strDocstring
        clsParser = guess_docstyle(strDocstring)
        print '\nProposed parser is {}\n'.format(clsParser.__name__)
        strPass1 =  clsParser.trimDocstring(strDocstring)
        print '\nTrimmed docstring\n'
        print strPass1
        strPass2 = clsParser.reduceDocstring(strPass1)
        print '\nReduced docstring\n'
        print strPass2
        gSign = clsParser.extractSignature(strPass1)
        print '\nSignature\n'
        print gSign
        strlstArgs = clsParser.extractArguments(strPass1)
        print '\nArguments\n'
        print strlstArgs
    except (CustomTypeError, CustomValueError) as err:
        print err.message