#usr/bin/python
"""
Module pos.exceptions

Custom exceptions with the added functionality of the exception traceback and
'IS A' relations build on the direct / indirect subclasses as well as virtual
subclasses.

Implemented classes (real inheritance):
    CustomError(StandardError --|> Exception)
        <|-- DesignContractError
        <|-- ConstantAssignment
    #
    CustomAttributeError(AttributeError --|> StandardError --|> Exception)
        <|-- ConstantAttributeAssignment
        <|-- NotExistingAttribute
        <|-- PrivateAttributeAccess
    #
    NotInDCError(SyntaxError --|> StandardError --|> Exception)
    #
    CustomTypeError(TypeError --|> StandardError --|> Exception)
        <|-- DCArgumentType
        <|-- DCReturnType
    #
    CustomValueError(ValueError --|> StandardError --|> Exception)
        <|-- DCArgumentValue
        <|-- DCReturnValue

Added 'virtual subclass' relations:
    CustomError
        <|.. CustomAttributeError
        <|.. CustomTypeError
        <|.. CustomValueError
    #
    DesignContractError
        <|.. DCArgumentType
        <|.. DCArgumentValue
        <|.. DCReturnType
        <|.. DCReturnValue
        <|.. NotInDCError
    #
    ConstantAssignment
        <|.. ConstantAttributeAssignment

The exception traceback functionality is implemented via composition wuth the
mix-in class ErrorMixin.
"""

__version__ = "0.0.1.0"
__date__ = "21-06-2018"
__status__ = "Development"

#imports

#+ standard libraries

from abc import ABCMeta

#+ my libraries

from pos.utils.traceback import ExceptionTraceback

#classes

#+ mix-in

class ErrorMixin(object):
    """
    """
    
    @property
    def Traceback(self):
        """
        """
        return None
    
    @property
    def CallChain(self):
        """
        """
        return None
    
    @property
    def Info(self):
        """
        """
        return None

#+ exceptions

class CustomError(StandardError, ErrorMixin):
    """
    """
    
    __metaclass__ = ABCMeta
    
    @classmethod
    def __subclasshook__(cls, clsOther):
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

class DesignContractError(CustomError):
    """
    """
    
    pass

class ConstantAssignment(CustomError):
    """
    """
    
    pass

class CustomAttributeError(AttributeError, ErrorMixin):
    """
    """
    
    pass

class ConstantAttributeAssignment(CustomAttributeError):
    """
    """
    
    pass

class NotExistingAttribute(CustomAttributeError):
    """
    """
    
    pass

class PrivateAttributeAccess(CustomAttributeError):
    """
    """
    
    pass

class NotInDCError(SyntaxError, ErrorMixin):
    """
    """
    
    pass

class CustomTypeError(TypeError, ErrorMixin):
    """
    """
    
    pass

class DCArgumentType(CustomTypeError):
    """
    """
    
    pass

class DCReturnType(CustomTypeError):
    """
    """
    
    pass

class CustomValueError(ValueError, ErrorMixin):
    """
    """
    
    pass

class DCArgumentValue(CustomValueError):
    """
    """
    
    pass

class DCReturnValue(CustomValueError):
    """
    """
    
    pass

#+ virtual subclasses registration

DesignContractError.register(NotInDCError)

DesignContractError.register(DCArgumentType)

DesignContractError.register(DCArgumentValue)

DesignContractError.register(DCReturnType)

DesignContractError.register(DCReturnValue)

ConstantAssignment.register(ConstantAttributeAssignment)