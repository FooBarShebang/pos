#usr/bin/python
"""
Module pos.exceptions

Custom exceptions with the added functionality of the exception traceback and
'IS A' relations build on the direct / indirect subclasses as well as virtual
subclasses.

Classes:
    ErrorMixin
        CustomError(StandardError --|> Exception)
            DesignContractError
            ConstantAssignment
        CustomAttributeError(AttributeError --|> StandardError --|> Exception)
            ConstantAttributeAssignment
            NotExistingAttribute
            PrivateAttributeAccess
        NotInDCError(SyntaxError --|> StandardError --|> Exception)
        CustomTypeError(TypeError --|> StandardError --|> Exception)
            DCArgumentType
            DCReturnType
        CustomValueError(ValueError --|> StandardError --|> Exception)
            DCArgumentValue
            DCReturnValue
Added 'virtual subclass' relations (not real inheritance):
    CustomError
        <|.. CustomAttributeError
        <|.. CustomTypeError
        <|.. CustomValueError
    DesignContractError
        <|.. DCArgumentType
        <|.. DCArgumentValue
        <|.. DCReturnType
        <|.. DCReturnValue
        <|.. NotInDCError
    ConstantAssignment
        <|.. ConstantAttributeAssignment

The exception traceback functionality is implemented via composition with the
mix-in class ErrorMixin.
"""

__version__ = "0.0.1.0"
__date__ = "21-06-2018"
__status__ = "Production"

#imports

#+ standard libraries

from abc import ABCMeta

#+ my libraries

from pos.utils.traceback import ExceptionTraceback

#classes

#+ mix-in

class ErrorMixin(object):
    """
    Helper / mix-in class to add the traceback analysis functionality to the
    custom exception classes.
    
    Read-only properties:
        Traceback : pos.utils.traceback.ExceptionTraceback
        CallChain : list(str)
        Info : str
    
    And a public method intended to be called from the initialization methods of
    these exceptions.
    
    Methods:
        presetTraceback()
            /pos.utils.traceback.ExceptionTraceback, int/ -> None
    
    Version 0.0.1.0
    """
    
    def __del__(self):
        """
        Special method to ensure the proper de-referencing of the internally
        stored instance of pos.utils.traceback.ExceptionTraceback class upon
        deletion / de-referencing of the exception object. Thus minimize the
        chance of the hanging around orphan frame objects.
        
        Signature:
            None -> None
        
        Version 0.0.1.0
        """
        if hasattr(self, '_traceback'):
            del self._traceback
            self._traceback = None
    
    @property
    def Traceback(self):
        """
        Read-only property.
        
        Returns a reference to the internally stored instance of the class
        pos.utils.traceback.ExceptionTraceback, which stores and analyses the
        exception's traceback.
        
        If the traceback information has not been obtained yet, the
        corresponding object is created upon the call. If the desired number of
        the innermost call frames to hide has been passed into the
        initialization method of the exception, and it is a non-negative integer
        and it is not larger than the length of the retrieved traceback, the
        traceback chain is truncated by removing this number of the elements
        from the tail.
        
        Signature:
            None -> pos.utils.traceback.ExceptionTraceback
        
        Version 0.0.1.0
        """
        if ((not hasattr(self, '_traceback')) or
                        (not isinstance(self._traceback, ExceptionTraceback))):
            if not hasattr(self, '_skip') or (self._skip is None):
                self._traceback = ExceptionTraceback()
            else:
                self._traceback = ExceptionTraceback(iSkip = self._skip)
        return self._traceback
    
    @property
    def CallChain(self):
        """
        Read-only property.
        
        Returns the list of the fully qualified names of the caller along the
        exception traceback chain. Simply wraps the property CallChain of the
        stored instance of the pos.utils.traceback.ExceptionTraceback class.
        
        Signature:
            None -> list(str)
        
        Version 0.0.1.0
        """
        return self.Traceback.CallChain
    
    @property
    def Info(self):
        """
        Read-only property.
        
        Returns a single string containg multiple lines separated by the newline
        character ('\n') as the human readable representation of the exception's
        traceback frames records. The first line contains the name of the
        exception's class and its message. The following-up lines are the same
        lines as retunred by the property Info of the traceback class
        pos.utils.traceback.ExceptionTraceback in the context of this exception
        traceback.
        
        Signature:
            None -> str
        
        Version 0.0.1.0
        """
        strInfo = '\n'.join([
                        '{}: {}'.format(self.__class__.__name__, self.message),
                        self.Traceback.Info])
        return strInfo
    
    def presetTraceback(self, objTraceback = None, iSkipFrames = None):
        """
        Helper method to replace the internally stored traceback object and / or
        the number of the innermost call frames to hide. Intended to be used by
        the initialization methods of the custom exceptions. However, may also
        be used at any time to change the exception's traceback on the fly.
        
        Warning: the second optional argument - number of frames to skip - has
        an effect only if the following conditions are met:
        1.1) No calls to the properties Traceback, CallChain or Info are made
            yet since the instantiation / raise of the exception
        OR
        1.2) a valid traceback object is provided as the first optional argument
            (with the keyword arguments call the order is not important)
        2) the required number of the skipped frames is a non-negative integer
        3) this number doesn't exceed the length of the traceback
        
        Signature:
            /pos.utils.traceback.ExceptionTraceback, int/ -> None
        
        Args:
            objTraceback: (optional), a replacement traceback object as an
                instance of pos.utils.traceback.ExceptionTraceback class
            iSkipFrames: (optional), the required number of the innermost call
                stack frames, must be a non-negative integer but not larger than
                the expected length of the traceback or the length of the
                replacement traceback object
        
        Version 0.0.1.0
        """
        if isinstance(iSkipFrames, int) and (iSkipFrames > 0):
            self._skip = iSkipFrames
        if isinstance(objTraceback, ExceptionTraceback):
            #==================================================================
            #Warning: abuses the internals of the class
            #pos.utils.traceback.ExceptionTraceback instead of its public API,
            #thus this method may be broken if the implementation of that class
            #is changed.
            #==================================================================
            self._traceback = ExceptionTraceback()
            lstOldTraceback = objTraceback._tblstTraceback
            if hasattr(self, '_skip'):
                if (self._skip > 0) and (self._skip <= len(lstOldTraceback)):
                    self._traceback._tblstTraceback = (
                                                lstOldTraceback[ : -self._skip])
                else:
                    self._traceback._tblstTraceback = lstOldTraceback
            else:
                self._traceback._tblstTraceback = lstOldTraceback

#+ exceptions

class CustomError(StandardError, ErrorMixin):
    """
    Generic custom exception class to be raised in the unspecified / debug
    situation. Can be used as an 'umbrella' exception type to catch any custom
    exceptions defined in this library.
    
    Must be raised / instantiated with a mandatory positional argument as the
    error message. It is supposed to be a string, but its type is not checked.
    
    May also be raised with the optional (positional or keyword) arguments to
    specify a replacement exception traceback object to be used instead of the
    real traceback and / or the desired number of the innermost call frames to
    hide / not show in the traceback.
    
    Direct subclass of StandardError. Also inherits the traceback analysis
    properties from the ErrorMixin.
    
    Read-only properties:
        Traceback : pos.utils.traceback.ExceptionTraceback
        CallChain : list(str)
        Info : str
     
    Version 0.0.1.0
    """
    
    __metaclass__ = ABCMeta
    
    @classmethod
    def __subclasshook__(cls, clsOther):
        """
        Special class method to hook into the 'IS A' relation check upon which
        the built-in functions issubclass() and isinstance() rely. Introduces
        partial 'HAS A' (composition over inheritance / duck typing) resolution.
        
        A class will be considered being a sub-class of this one if:
        1) it is real direct (child) or indirect (grand-child and further)
            subclass of the CustomError (this class)
        OR
        2) it is real direct or indirect subclass of StandardError class AND
            it has attributes Traceback, CallChain and Info (expected to be
            properties, but their type is not checked), e.g. inherited from the
            ErrorMixin class
        
        Note: even though the direct subclasses of this class and their
        subclasses do inherit this method, for them the 'HAS A' check is not
        applicable, instead the standard 'IS A' check is applied.
        
        Signature:
            class A -> bool OR NotImplemented
        
        Version 0.0.1.0
        """
        if cls is CustomError:
            bCond1 = hasattr(clsOther, 'Traceback')
            bCond2 = hasattr(clsOther, 'CallChain')
            bCond3 = hasattr(clsOther, 'Info')
            bCond4 = issubclass(clsOther, StandardError)
            bCond5 = bCond1 and bCond2 and bCond3
            if bCond4 and bCond5:
                gResult = True
            elif not bCond4:
                gResult = False
            else:
                gResult = NotImplemented
        else:
            gResult = NotImplemented
        return gResult
    
    def __init__(self, strMessage, objTraceback = None, iSkipFrames = None):
        """
        Initialization. Requires mandatory argument which is stored in the
        attribute 'args' (tuple) and is used as the value of the attribute
        'message'.
        
        Optional arguments can be passed as the last positional or the keyword
        arguments (after the positional) to force replacement of the actual
        exception traceback by a replacement object and / or to hide the
        specified number of the last elements in the traceback as the innermost
        call frames.
        
        Signature:
            str/, pos.utils.traceback.ExceptionTraceback, int/ -> None
        
        Args:
            strMessage: expected to be a string, but is not checked, will be
                used as the exception message
            objTraceback: (optional), a replacement traceback object as an
                instance of pos.utils.traceback.ExceptionTraceback class
            iSkipFrames: (optional), the required number of the innermost call
                stack frames, must be a non-negative integer but not larger than
                the expected length of the traceback
        
        Version 0.0.1.0
        """
        super(CustomError, self).__init__(strMessage)
        self.presetTraceback(objTraceback = objTraceback,
                                                    iSkipFrames = iSkipFrames)

class DesignContractError(CustomError):
    """
    Generic custom exception class to be raised in the situations related to the
    Design by Contract violations. Can be used as an 'umbrella' exception type
    to catch NotInDCError, DCArgumentType, DCArgumentValue, DCReturnType and
    DCReturnValue errors.
    
    Must be raised / instantiated with a mandatory positional argument as the
    error message. It is supposed to be a string, but its type is not checked.
    
    May also be raised with the optional (positional or keyword) arguments to
    specify a replacement exception traceback object to be used instead of the
    real traceback and / or the desired number of the innermost call frames to
    hide / not show in the traceback.
    
    Direct subclass of CustomError class. Also inherits the traceback analysis
    properties from the ErrorMixin.
    
    Read-only properties:
        Traceback : pos.utils.traceback.ExceptionTraceback
        CallChain : list(str)
        Info : str
     
    Version 0.0.1.0
    """
    
    pass

class ConstantAssignment(CustomError):
    """
    Custom exception class to be raised in the situations related to the
    assignment to or attempted deletion of a constant type object. Can be used
    as an 'umbrella' exception type to catch ConstantAttributeAssignment type
    errors.
    
    Must be raised / instantiated with a mandatory positional argument as the
    name of an object, which is used to construct the error message. It is
    supposed to be a string, but its type is not checked.
    
    May also be raised with the optional (positional or keyword) arguments to
    specify a replacement exception traceback object to be used instead of the
    real traceback and / or the desired number of the innermost call frames to
    hide / not show in the traceback.
    
    Direct subclass of CustomError class. Also inherits the traceback analysis
    properties from the ErrorMixin.
    
    Read-only properties:
        Traceback : pos.utils.traceback.ExceptionTraceback
        CallChain : list(str)
        Info : str
     
    Version 0.0.1.0
    """
    
    def __init__(self, strObject, objTraceback = None, iSkipFrames = None):
        """
        Initialization. Requires mandatory argument which is stored in the
        attribute 'args' (tuple) and is used to form the value of the attribute
        'message' (string).
        
        Optional arguments can be passed as the last positional or the keyword
        arguments (after the positional) to force replacement of the actual
        exception traceback by a replacement object and / or to hide the
        specified number of the last elements in the traceback as the innermost
        call frames.
        
        Signature:
            str/, pos.utils.traceback.ExceptionTraceback, int/ -> None
        
        Args:
            strObject: expected to be a string, but is not checked, the name of
                an object, will be used to construct the exception message
            objTraceback: (optional), a replacement traceback object as an
                instance of pos.utils.traceback.ExceptionTraceback class
            iSkipFrames: (optional), the required number of the innermost call
                stack frames, must be a non-negative integer but not larger than
                the expected length of the traceback
        
        Version 0.0.1.0
        """
        strError = "Cannot change value of the constant {}".format(strObject)
        super(ConstantAssignment, self).__init__(strError)
        self.args = (strObject, )
        self.presetTraceback(objTraceback = objTraceback,
                                                    iSkipFrames = iSkipFrames)

class CustomAttributeError(AttributeError, ErrorMixin):
    """
    Generic custom exception class to be raised in the situations related to the
    attribute resolution violation situations. Can be used as an 'umbrella'
    exception type to catch ConstantAttributeAssignment, NotExistingAttribute
    and PrivateAttributeAccess type errors.
    
    Must be raised / instantiated with two mandatory positional arguments as the
    name of an attribute and the reference to the owner class (type), which are
    used to construct the error message. Type checks on the arguments are not
    performed.
    
    May also be raised with the optional (positional or keyword) arguments to
    specify a replacement exception traceback object to be used instead of the
    real traceback and / or the desired number of the innermost call frames to
    hide / not show in the traceback.
    
    Direct subclass of AttributeError. Also inherits the traceback analysis
    properties from the ErrorMixin.
    
    Read-only properties:
        Traceback : pos.utils.traceback.ExceptionTraceback
        CallChain : list(str)
        Info : str
    
    Also considered to be virtual sub-class of the CustomError class.
     
    Version 0.0.1.0
    """
    
    def __init__(self, strAttr, clsType, objTraceback=None, iSkipFrames=None):
        """
        Initialization. Requires two mandatory arguments which are stored in the
        attribute 'args' (tuple) and are used to form the value of the attribute
        'message' (string).
        
        Optional arguments can be passed as the last positional or the keyword
        arguments (after the positional) to force replacement of the actual
        exception traceback by a replacement object and / or to hide the
        specified number of the last elements in the traceback as the innermost
        call frames.
        
        Signature:
            str, class A/, pos.utils.traceback.ExceptionTraceback, int/ -> None
        
        Args:
            strAttr: expected to be a string, but is not checked, the name of an
                attribute, will be used to construct the exception message
            clsType: expected to be a reference to the supposed owner of this
                attribute (class as a type), but is not checked, will be used to
                construct the exception message
            objTraceback: (optional), a replacement traceback object as an
                instance of pos.utils.traceback.ExceptionTraceback class
            iSkipFrames: (optional), the required number of the innermost call
                stack frames, must be a non-negative integer but not larger than
                the expected length of the traceback
        
        Version 0.0.1.0
        """
        strMessage = 'Attribute "{}" of class {}.{}'.format(strAttr, 
                                        clsType.__module__, clsType.__name__)
        super(CustomAttributeError, self).__init__(strMessage)
        self.args = (strAttr, clsType)
        self.presetTraceback(objTraceback = objTraceback,
                                                    iSkipFrames = iSkipFrames)

class ConstantAttributeAssignment(CustomAttributeError):
    """
    Custom exception class to be raised in the situations related to the
    assignment or attempted deletion a constant attribute.
    
    Must be raised / instantiated with two mandatory positional arguments as the
    name of an attribute and the reference to the owner class (type), which are
    used to construct the error message. Type checks on the arguments are not
    performed.
    
    May also be raised with the optional (positional or keyword) arguments to
    specify a replacement exception traceback object to be used instead of the
    real traceback and / or the desired number of the innermost call frames to
    hide / not show in the traceback.
    
    Direct subclass of CustomAttributeError. So inherits the traceback analysis
    properties from the ErrorMixin:
        Traceback : pos.utils.traceback.ExceptionTraceback
        CallChain : list(str)
        Info : str
    
    Also considered to be virtual sub-class of the ConstantAssignment class.
     
    Version 0.0.1.0
    """
    
    pass

class NotExistingAttribute(CustomAttributeError):
    """
    Custom exception class to be raised in the situations related to an attempt
    of data retrieval from, assignment to or deletion of non-existing attribute.
    
    Must be raised / instantiated with two mandatory positional arguments as the
    name of an attribute and the reference to the owner class (type), which are
    used to construct the error message. Type checks on the arguments are not
    performed.
    
    May also be raised with the optional (positional or keyword) arguments to
    specify a replacement exception traceback object to be used instead of the
    real traceback and / or the desired number of the innermost call frames to
    hide / not show in the traceback.
    
    Direct subclass of CustomAttributeError. So inherits the traceback analysis
    properties from the ErrorMixin.
    
    Read-only properties:
        Traceback : pos.utils.traceback.ExceptionTraceback
        CallChain : list(str)
        Info : str
     
    Version 0.0.1.0
    """
    
    pass

class PrivateAttributeAccess(CustomAttributeError):
    """
    Custom exception class to be raised in the situations related to an attempt
    of data retrieval from, assignment to or deletion of a 'private' / hidden
    attribute.
    
    Must be raised / instantiated with two mandatory positional arguments as the
    name of an attribute and the reference to the owner class (type), which are
    used to construct the error message. Type checks on the arguments are not
    performed.
    
    May also be raised with the optional (positional or keyword) arguments to
    specify a replacement exception traceback object to be used instead of the
    real traceback and / or the desired number of the innermost call frames to
    hide / not show in the traceback.
    
    Direct subclass of CustomAttributeError. So inherits the traceback analysis
    properties from the ErrorMixin.
    
    Read-only properties:
        Traceback : pos.utils.traceback.ExceptionTraceback
        CallChain : list(str)
        Info : str
     
    Version 0.0.1.0
    """
    
    pass

class NotInDCError(SyntaxError, ErrorMixin):
    """
    Custom exception class to be raised in the situations when a function or
    method is not found in the Design Contracts table, whereas it is supposed
    to by under the DbC control.
    
    Must be raised / instantiated with a mandatory positional argument as the
    name of a function / method< which is supposed to be a string, but its type
    is not checked. It is used to construct the error message.
    
    May also be raised with the optional (positional or keyword) arguments to
    specify a replacement exception traceback object to be used instead of the
    real traceback and / or the desired number of the innermost call frames to
    hide / not show in the traceback.
    
    Direct subclass of SyntaxError. Also inherits the traceback analysis
    properties from the ErrorMixin.
    
    Read-only properties:
        Traceback : pos.utils.traceback.ExceptionTraceback
        CallChain : list(str)
        Info : str
    
    Also considered to be virtual sub-class of the DesignContractError class.
    
    Version 0.0.1.0
    """
    
    def __init__(self, strObject, objTraceback = None, iSkipFrames = None):
        """
        Initialization. Requires mandatory argument which is stored in the
        attribute 'args' (tuple) and is used to form the value of the attribute
        'message' (string).
        
        Optional arguments can be passed as the last positional or the keyword
        arguments (after the positional) to force replacement of the actual
        exception traceback by a replacement object and / or to hide the
        specified number of the last elements in the traceback as the innermost
        call frames.
        
        Signature:
            str/, pos.utils.traceback.ExceptionTraceback, int/ -> None
        
        Args:
            strObject: expected to be a string, but is not checked, the name of
                an object, will be used to construct the exception message
            objTraceback: (optional), a replacement traceback object as an
                instance of pos.utils.traceback.ExceptionTraceback class
            iSkipFrames: (optional), the required number of the innermost call
                stack frames, must be a non-negative integer but not larger than
                the expected length of the traceback
        
        Version 0.0.1.0
        """
        strError = "Design Contract is not found for {}".format(strObject)
        super(NotInDCError, self).__init__(strError)
        self.args = (strObject, )
        self.presetTraceback(objTraceback = objTraceback,
                                                    iSkipFrames = iSkipFrames)

class CustomTypeError(TypeError, ErrorMixin):
    """
    Generic custom exception class to be raised in the situations related to the
    unexpected / wrong type of data received or generated. Can be used as an
    'umbrella' exception type to catch DCArgumentType and DCReturnType type
    errors.
    
    Must be raised / instantiated with two mandatory positional arguments as the
    offending object and the reference class (type), which are used to construct
    the error message. Type checks on the arguments are not performed.
    
    May also be raised with the optional (positional or keyword) arguments to
    specify a replacement exception traceback object to be used instead of the
    real traceback and / or the desired number of the innermost call frames to
    hide / not show in the traceback.
    
    Direct subclass of TypeError. Also inherits the traceback analysis
    properties from the ErrorMixin.
    
    Read-only properties:
        Traceback : pos.utils.traceback.ExceptionTraceback
        CallChain : list(str)
        Info : str
    
    Also considered to be virtual sub-class of the CustomError class.
     
    Version 0.0.1.0
    """
    
    def __init__(self, gValue, clsType, objTraceback=None, iSkipFrames=None):
        """
        Initialization. Requires two mandatory arguments which are stored in the
        attribute 'args' (tuple) and are used to form the value of the attribute
        'message' (string).
        
        Optional arguments can be passed as the last positional or the keyword
        arguments (after the positional) to force replacement of the actual
        exception traceback by a replacement object and / or to hide the
        specified number of the last elements in the traceback as the innermost
        call frames.
        
        Signature:
            type A, type type B/, pos.utils.traceback.ExceptionTraceback, int/
                -> None
        
        Args:
            gValue: the 'offending' value, will be used to construct the
                exception message
            clsType: expected to be a reference to the supposed reference class
                or type of this value, but is not checked, will be used to
                construct the exception message
            objTraceback: (optional), a replacement traceback object as an
                instance of pos.utils.traceback.ExceptionTraceback class
            iSkipFrames: (optional), the required number of the innermost call
                stack frames, must be a non-negative integer but not larger than
                the expected length of the traceback
        
        Version 0.0.1.0
        """
        strMessage = '{} of {} is not of {}'.format(gValue, type(gValue),
                                                            clsType.__name__)
        super(CustomTypeError, self).__init__(strMessage)
        self.args = (gValue, clsType)
        self.presetTraceback(objTraceback = objTraceback,
                                                    iSkipFrames = iSkipFrames)

class DCArgumentType(CustomTypeError):
    """
    Specific custom exception class to be raised in the situations related to
    the unexpected / wrong type of an argument of a function / method under the
    Design by Contract control.
    
    Must be raised / instantiated with two mandatory positional arguments as the
    offending object and the reference class (type), which are used to construct
    the error message. Type checks on the arguments are not performed.
    
    May also be raised with the optional (positional or keyword) arguments to
    specify a replacement exception traceback object to be used instead of the
    real traceback and / or the desired number of the innermost call frames to
    hide / not show in the traceback.
    
    Direct subclass of CustomTypeError. Also inherits the traceback analysis
    properties from the ErrorMixin.
    
    Read-only properties:
        Traceback : pos.utils.traceback.ExceptionTraceback
        CallChain : list(str)
        Info : str
    
    Also considered to be virtual sub-class of the DesignContractError class.
     
    Version 0.0.1.0
    """
    
    pass

class DCReturnType(CustomTypeError):
    """
    Specific custom exception class to be raised in the situations related to
    the unexpected / wrong type of the returned value of a function / method
    under the Design by Contract control.
    
    Must be raised / instantiated with two mandatory positional arguments as the
    offending object and the reference class (type), which are used to construct
    the error message. Type checks on the arguments are not performed.
    
    May also be raised with the optional (positional or keyword) arguments to
    specify a replacement exception traceback object to be used instead of the
    real traceback and / or the desired number of the innermost call frames to
    hide / not show in the traceback.
    
    Direct subclass of CustomTypeError. Also inherits the traceback analysis
    properties from the ErrorMixin.
    
    Read-only properties:
        Traceback : pos.utils.traceback.ExceptionTraceback
        CallChain : list(str)
        Info : str
    
    Also considered to be virtual sub-class of the DesignContractError class.
     
    Version 0.0.1.0
    """
    
    pass

class CustomValueError(ValueError, ErrorMixin):
    """
    Generic custom exception class to be raised in the situations related to the
    unexpected / wrong value of data received or generated. Can be used as an
    'umbrella' exception type to catch DCArgumentValue and DCReturnValue type
    errors.
    
    Must be raised / instantiated with two mandatory positional arguments as the
    offending object and the string description of the restriction's violation,
    which are used to construct the error message. Type checks on the arguments
    are not performed.
    
    May also be raised with the optional (positional or keyword) arguments to
    specify a replacement exception traceback object to be used instead of the
    real traceback and / or the desired number of the innermost call frames to
    hide / not show in the traceback.
    
    Direct subclass of ValueError. Also inherits the traceback analysis
    properties from the ErrorMixin.
    
    Read-only properties:
        Traceback : pos.utils.traceback.ExceptionTraceback
        CallChain : list(str)
        Info : str
    
    Also considered to be virtual sub-class of the CustomError class.
     
    Version 0.0.1.0
    """
    
    def __init__(self, gValue, strError, objTraceback=None, iSkipFrames=None):
        """
        Initialization. Requires two mandatory arguments which are stored in the
        attribute 'args' (tuple) and are used to form the value of the attribute
        'message' (string).
        
        Optional arguments can be passed as the last positional or the keyword
        arguments (after the positional) to force replacement of the actual
        exception traceback by a replacement object and / or to hide the
        specified number of the last elements in the traceback as the innermost
        call frames.
        
        Signature:
            type A, str/, pos.utils.traceback.ExceptionTraceback, int/ -> None
        
        Args:
            gValue: the 'offending' value, will be used to construct the
            `exception message
            strError: expected to be a string explaing the reason why the value
                is wrong, but is not checked, will be used to construct the
                exception message
            objTraceback: (optional), a replacement traceback object as an
                instance of pos.utils.traceback.ExceptionTraceback class
            iSkipFrames: (optional), the required number of the innermost call
                stack frames, must be a non-negative integer but not larger than
                the expected length of the traceback
        
        Version 0.0.1.0
        """
        strMessage = "Value {} doesn't match criteria {}".format(gValue,
                                                                    strError)
        super(CustomValueError, self).__init__(strMessage)
        self.args = (gValue, strError)
        self.presetTraceback(objTraceback = objTraceback,
                                                    iSkipFrames = iSkipFrames)

class DCArgumentValue(CustomValueError):
    """
    Specific custom exception class to be raised in the situations related to
    the unexpected / wrong value of an argument of a function / method under the
    Design by Contract control.
    
    Must be raised / instantiated with two mandatory positional arguments as the
    offending object and the string description of the restriction's violation,
    which are used to construct the error message. Type checks on the arguments
    are not performed.
    
    May also be raised with the optional (positional or keyword) arguments to
    specify a replacement exception traceback object to be used instead of the
    real traceback and / or the desired number of the innermost call frames to
    hide / not show in the traceback.
    
    Direct subclass of CustomValueError. Also inherits the traceback analysis
    properties from the ErrorMixin.
    
    Read-only properties:
        Traceback : pos.utils.traceback.ExceptionTraceback
        CallChain : list(str)
        Info : str
    
    Also considered to be virtual sub-class of the DesignContractError class.
     
    Version 0.0.1.0
    """
    
    pass

class DCReturnValue(CustomValueError):
    """
    Specific custom exception class to be raised in the situations related to
    the unexpected / wrong value of the returned value of a function / method
    under the Design by Contract control.
    
    Must be raised / instantiated with two mandatory positional arguments as the
    offending object and the string description of the restriction's violation,
    which are used to construct the error message. Type checks on the arguments
    are not performed.
    
    May also be raised with the optional (positional or keyword) arguments to
    specify a replacement exception traceback object to be used instead of the
    real traceback and / or the desired number of the innermost call frames to
    hide / not show in the traceback.
    
    Direct subclass of CustomValueError. Also inherits the traceback analysis
    properties from the ErrorMixin.
    
    Read-only properties:
        Traceback : pos.utils.traceback.ExceptionTraceback
        CallChain : list(str)
        Info : str
    
    Also considered to be virtual sub-class of the DesignContractError class.
     
    Version 0.0.1.0
    """
    
    pass

#+ virtual subclasses registration

DesignContractError.register(NotInDCError)

DesignContractError.register(DCArgumentType)

DesignContractError.register(DCArgumentValue)

DesignContractError.register(DCReturnType)

DesignContractError.register(DCReturnValue)

ConstantAssignment.register(ConstantAttributeAssignment)
