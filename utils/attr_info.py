#usr/bin/python
"""
Module pos.utils.attr_info

Implements classes to store and produce a string information on the class'
attributes:
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
    """
    
    #special methods
    
    def __init__(self):
        """
        """
        self.Name = None
        self.Type = None
        self.Signature = None
        self.Contract = None

class FieldInfo(AttributeInfo):
    """
    """
    
    #special methods
    
    def __init__(self):
        """
        """
        super(FieldInfo, self).__init__()
        self.RealType = None
        self.Scope = None
        self.Access = None

class MethodInfo(AttributeInfo):
    """
    """
    
    #special methods
    
    def __init__(self):
        """
        """
        super(MethodInfo, self).__init__()
        self.DocString = None