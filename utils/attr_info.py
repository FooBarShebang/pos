#usr/bin/python
"""
Module pos.utils.attr_info

Implements classes to store and produce a string information on the class'
attributes.

Classes:
    AttributeInfo
        FieldInfo
        MethodInfo
"""

__version__ = "0.0.1.0"
__date__ = "10-07-2018"
__status__ = "Development"

#classes

class AttributeInfo(object):
    """
    Prototype class for storage of the information on an attribute of a class.
    
    Attributes:
        Name: str OR None, name of an attribute
        Type: type type A OR None, 'return' type of an attribute
        Signature: str OR None, method / property signature, e.g. 'int -> str'
        Contract: ??? OR None,
            design contract associated with this method / property
    
    Version 0.0.1.0
    """
    
    #special methods
    
    def __init__(self):
        """
        Initialization methods. Sets all instance attributes to None.
        
        Signature:
            None -> None
        
        Version 0.0.1.0
        """
        self.Name = None
        self.Type = None
        self.Signature = None
        self.Contract = None
    
    def __repr__(self):
        """
        Returns a string representation as the class name and the name of an
        attribute: 'ClassName(AttrName)'
        
        Signature:
            None -> str
        
        Version 0.0.1.0
        """
        return '{}({})'.format(self.__class__.__name__, self.Name)

class FieldInfo(AttributeInfo):
    """
    Class for storage of the information on a data attribute (field) of a class,
    including the properties. Subclass of AttributeInfo.
    
    Attributes:
        Name: str OR None, name of an attribute
        Type: type type A OR None, 'return' type of an attribute
        Signature: str OR None, method / property signature, e.g. 'int -> str'
        Contract: ??? OR None,
            design contract associated with this method / property
        RealType: type type A OR None, actual type of the data container, how
            it is stored internally, e.g. property or another data descriptor
            class
        Access: str OR None, if this attribute is considered to be a public one,
            i.e. read and write access, or a 'protected' / 'restricted' one with
            only read access
        Scope: str OR None, if this field is a class or instance attribute
    
    Version 0.0.1.0
    """
    
    #special methods
    
    def __init__(self):
        """
        Initialization methods. Sets all instance attributes to None.
        
        Signature:
            None -> None
        
        Version 0.0.1.0
        """
        super(FieldInfo, self).__init__()
        self.RealType = None
        self.Access = None
        self.Scope = None

class MethodInfo(AttributeInfo):
    """
    Class for storage of the information on a method of a class - class, static
    or instance method. Subclass of AttributeInfo.
    
    Attributes:
        Name: str OR None, name of an attribute
        Type: type type A OR None, 'return' type of an attribute
        Signature: str OR None, method / property signature, e.g. 'int -> str'
        Contract: ??? OR None,
            design contract associated with this method / property
        DocString: str OR None, reduced docstring of the method, ideally, with
            all data related to the auto-generation of documentation being
            removed
    
    Version 0.0.1.0
    """
    
    #special methods
    
    def __init__(self):
        """
        Initialization methods. Sets all instance attributes to None.
        
        Signature:
            None -> None
        
        Version 0.0.1.0
        """
        super(MethodInfo, self).__init__()
        self.DocString = None