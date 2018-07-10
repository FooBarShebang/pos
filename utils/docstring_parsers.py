#usr/bin/python
"""
Module pos.utils.docstring_parsers

Implements classes to parse the docstrings, i.e. extract / remove the signature
of the method / function from the docstring, remove the extra indentation, etc.

Supported formats (if adhere to the style guidelines) are:
    * Epytext
    * reST
    * Google format for the Python docstrings
    * Numpydoc
    * Slightly modified Google format with the explicit signature definition
        in the Haskell style and explicit indication of the optional arguments
        in the Args part adopted by AA (library's author)

Defines classes:
    GenericParser
        GoogleParser
            AAParser

"""

__version__ = "0.0.1.0"
__date__ = "10-07-2018"
__status__ = "Development"

#imports

#+ standard libraries

import sys

#+ library's modules

from pos.exceptions import CustomTypeError, CustomValueError

#classes

class GenericParser(object):
    """
    """
    
    #class attributes
    
    SkipTokens = []
    
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

class GoogleParser(GenericParser):
    """
    """
    
    #class attributes
    
    SkipTokens = ['Args:', 'Returns:', 'Raises:', 'Attributes:']
    
    SecondLineSymbol = None
    
    SignatureToken = None
    
    ArgsToken = None

class AAParser(GoogleParser):
    """
    """
    
    #class attributes
    
    SkipTokens = list(GoogleParser.SkipTokens)
    SkipTokens.extend(['Signature:', 'Classes:', 'Properties:', 'Methods:',
                        'Class methods:', 'Read-only properties:'])
    
    SecondLineSymbol = None
    
    SignatureToken = None
    
    ArgsToken = None

#testing - temporary

if __name__ == '__main__':
    try:
        strPass1 =  AAParser.trimDocstring(AAParser.reduceDocstring.__doc__)
        print strPass1
        print
        strPass2 = AAParser.reduceDocstring(strPass1)
        print strPass2
    except (CustomTypeError, CustomValueError) as err:
        print err.message