#usr/bin/python
"""
Module pos.base_classes

Abstract Base Classes implementing the modified attributes access scheme and
the classes introspection functionality.

Defined classes:
    DescriptedABC - support for the data descriptors access methods in the case
        of the instance attributes and the class attributes accessed from a
        class without instantiation; also implements the basic introspection
"""

__version__ = "0.0.1.2"
__date__ = "06-07-2018"
__status__ = "Development"

#imports

#+ standard libraries

import abc
import inspect

#classes

#+metaclasses

class DescriptedABC_Meta(abc.ABCMeta):
    """
    Meta-class for DescriptedABC. Ensures the usage of the __set__() and
    __delete__() methods upon assignment and deletion of the class attributes
    being data descriptors when the action is performed on the class itself
    without its instantiation.
    
    Version 0.0.1.1
    """
    
    def __setattr__(self, strAttr, gValue):
        """
        Special method. Ensures that the __set__() descriptor is called if
        the attribute to be changed has it. Otherwise, the standard attribute
        resolution scheme is used. Applied to the calls on the class, not on its
        instance.
        
        The side effect is that if the value of the class attribute being a data
        descriptor inherited from a super class is changed, a 'local' copy of
        that attribute is created in the subclass, and only its value is
        changed, so the change does not propagate upwards. The downwards
        propagation of the change happens only down to a subclass, which has
        already 'decoupled' that class attribute.
        
        Signature:
            str, type A -> None
        
        Input:
            strAttr - string, name of the attribute to be changed in value
            
            gValue - any type, value to be assigned to the attribute
        
        Version 0.0.1.1
        """
        lstMRO = type.__getattribute__(self, '__mro__')
        for objBase in lstMRO: #go through the MRO
            dictVars = type.__getattribute__(objBase, '__dict__')
            if strAttr in dictVars: #found in a dictionary (own or super)
                objTemp = dictVars[strAttr]
                if hasattr(objTemp, '__set__'): #via descriptor
                    if objBase is lstMRO[0]: #own
                        objTemp.__set__(self, gValue)
                    elif not isinstance(objTemp, property):
                        #inherited data descriptor but not a property
                        #-> copy into own class and try to set
                        type.__setattr__(self, strAttr,
                                objTemp.__class__(objTemp.__get__(self, self)))
                        objTrial = type.__getattribute__(
                                                    self, '__dict__')[strAttr]
                        objTrial.__set__(self, gValue)
                else: #via usual way, not a data descriptor / property
                    type.__setattr__(self, strAttr, gValue)
                break
        else: # doesn't exist yet -> create own class field
            type.__setattr__(self, strAttr, gValue)
    
    def __delattr__(self, strAttr):
        """
        Special method. Ensures that the __delete__() descriptor is called if
        the attribute to be deleted has it. Otherwise, the standard attribute
        resolution scheme is used. Applied to the calls on the class, not on its
        instance.
        
        Signature:
            str -> None
        
        Input:
            strAttr - string, name of the attribute to be deleted.
        
        Version 0.0.1.0
        """
        dictVars = type.__getattribute__(self, '__dict__')
        if strAttr in dictVars: #found in the class dictionary
            objTemp = dictVars[strAttr]
            if hasattr(objTemp, '__delete__'): #via descriptor
                objTemp.__delete__(self)
            else: #via usual way
                type.__delattr__(self, strAttr)
        else: #not in the class dictionary -> will lead to AttributeError
            type.__delattr__(self, strAttr)

#+ ABCs

class DescriptedABC(object):
    """
    Abstract Base Class that ensures that the __get__(), __set__() and
    __delete__() methods of the data descriptors are called upon read and write
    access as well as upon the deletion of such attributes. This modified
    attribute resolution scheme is applied to the instance attributes and
    class attributes accessed from an instance as well as from the class itself
    without instantiation.
    
    The subclasses which are supposed to be instantiated must override the
    method onInit(), where they are supposed to create the required instance
    attributes.
    
    Also implements the basic introspection functionality. Use methods
    getClassInfo() and getInfo() - for non-abstract subclasses only - in order
    to get more detailed information on the class / instance.
    
    Version 0.0.1.2
    """
    
    #class fields
    
    __metaclass__ = DescriptedABC_Meta
    
    #special methods
    
    def __init__(self, *args, **kwargs):
        """
        Special method - initialization of the class. Simple passes all received
        positional and keyword arguments into the method onInit().
        
        Signature:
            *args, **kwargs -> None
        
        Version 0.0.1.0
        """
        self.onInit(*args, **kwargs)
    
    @abc.abstractmethod
    def onInit(self, *args, **kwargs):
        """
        Abstract method. Does nothing but prevents the class from being
        instantiated. The non-abstract subclasses are supposed to override this
        method and to use it for creation of the instance attributes. Receives
        all positional and keyword arguments from the initialization method.
        
        Signature:
            *args, **kwargs -> None
        
        Version 0.0.1
        """
        pass
    
    def __getattribute__(self, strAttr):
        """
        Special method. Ensures that the __get__() descriptor is called if the
        attribute to be deleted has it, otherwise the standard attribute
        resolution scheme is used.
        
        Signature:
            str -> type A
        
        Input:
            strAttr - string, name of the attribute to be deleted.
        
        Version 0.0.1.1
        """
        objOwner = object.__getattribute__(self, '__class__')
        objTemp = object.__getattribute__(self, strAttr)
        if inspect.ismethod(objTemp) or inspect.isfunction(objTemp):
            #static, class and normal functions
            objResult = objTemp
        elif hasattr(objTemp, '__get__'):
            #properties and custom defined data descriptors
            objResult = objTemp.__get__(self, objOwner)
        else:
            objResult = objTemp
        return objResult
    
    def __setattr__(self, strAttr, gValue):
        """
        Special method. Ensures that the __set__() descriptor is called if
        the attribute to be changed has it. Otherwise, the standard attribute
        resolution scheme is used.
        
        Signature:
            str, type A -> None
        
        Input:
            strAttr - string, name of the attribute to be changed in value
            
            gValue - any type, value to be assigned to the attribute
        
        Version 0.0.1.1
        """
        if strAttr in object.__getattribute__(self, '__dict__'):#instance field
            objTemp = object.__getattribute__(self, strAttr)
            if hasattr(objTemp, '__set__'): #data descriptor
                objTemp.__set__(self, gValue)
            else: #usual type
                object.__setattr__(self, strAttr, gValue)
        else: #check if it is a class field
            if hasattr(self.__class__, strAttr):
                for clsBase in self.__class__.__mro__:
                    dictVars = type.__getattribute__(clsBase, '__dict__')
                    if strAttr in dictVars:
                        objTemp = dictVars[strAttr]
                        if isinstance(objTemp, property): #property
                            object.__setattr__(self, strAttr, gValue)
                        else: #another type of the class attribute
                            setattr(self.__class__, strAttr, gValue)
                        break
            else: # doesn't exist yet -> create
                object.__setattr__(self, strAttr, gValue)
    
    def __delattr__(self, strAttr):
        """
        Special method. Ensures that the __delete__() descriptor is called if
        the attribute to be deleted has it. Otherwise, the standard attribute
        resolution scheme is used.
        
        Signature:
            str -> None
        
        Input:
            strAttr - string, name of the attribute to be deleted.
        
        Version 0.0.1.1
        """
        if strAttr in object.__getattribute__(self, '__dict__'):#instance field
            objTemp = object.__getattribute__(self, strAttr)
            if hasattr(objTemp, '__delete__'): #data descriptor ?
                objTemp.__delete__(self)
            else: #usual type
                object.__delattr__(self, strAttr)
        else: #check if it is a class field
            if hasattr(self.__class__, strAttr): #class field
                for clsBase in self.__class__.__mro__:
                    dictVars = type.__getattribute__(clsBase, '__dict__')
                    if strAttr in dictVars:
                        objTemp = dictVars[strAttr]
                        if isinstance(objTemp, property): #property
                            object.__delattr__(self, strAttr)
                        else: #another type of the class attribute
                            delattr(self.__class__, strAttr)
                        break
            else: # doesn't exist yet, should raise attribute error exception
                object.__delattr__(self, strAttr)
    
    def __del__(self):
        """
        Special method. Ensures proper deletion of the instance attributes,
        even those that are 'constant' (being data descriptors).
        
        Signature:
            None -> None
        
        Version 0.0.1.0
        """
        dictDict = object.__getattribute__(self, '__dict__')
        strlstTemp = dictDict.keys()
        for strAttr in strlstTemp:
            del dictDict[strAttr]
        del strlstTemp
        del dictDict
    
    #public class methods
    
    @classmethod
    def getClassFields(cls):
        """
        Returns as a list of strings the names of all 'public' class data fields
        (attributes, which are not class or static methods and can be called
        from the class without instantiation). An attribute is considered to be
        'public' only if name doesn't start with an underscore (including the
        special / magic attributes). The returned list is sorted alphabetically.
        
        Signature:
            None -> list(str)
        
        Version 0.0.1.0
        """
        strlstTemp = []
        for clsBase in cls.__mro__:
            for strAttr, objValue in clsBase.__dict__.items():
                bCond1 = not isinstance(objValue, (staticmethod, classmethod))
                bCond2 = not inspect.isfunction(objValue)
                bCond3 = not isinstance(objValue, property)
                bCond4 = not strAttr.startswith('_')
                bCond5 = not (strAttr in strlstTemp)
                bCond = bCond1 and bCond2 and bCond3 and bCond4 and bCond5
                if bCond:
                    strlstTemp.append(strAttr)
        return list(sorted(strlstTemp))
    
    @classmethod
    def getClassMethods(cls):
        """
        Returns as a list of strings the names of all 'public' class methods
        (attributes, which are either class or static methods and can be called
        from the class without instantiation). An attribute is considered to be
        'public' only if name doesn't start with an underscore (including the
        special / magic attributes). The returned list is sorted alphabetically.
        
        Signature:
            None -> list(str)
        
        Version 0.0.1.0
        """
        strlstTemp = []
        for clsBase in cls.__mro__:
            for strAttr, objValue in clsBase.__dict__.items():
                bCond1 = isinstance(objValue, (staticmethod, classmethod))
                bCond2 = not strAttr.startswith('_')
                bCond3 = not (strAttr in strlstTemp)
                bCond = bCond1 and bCond2 and bCond3
                if bCond:
                    strlstTemp.append(strAttr)
        return list(sorted(strlstTemp))
    
    #public instance methods
    
    def getFields(self):
        """
        Returns as a list of strings the names of all 'public' data fields
        (attributes, which are not methods are functions, but class or instance
        data attributes or properties) which can be called from an instance of
        a class. An attribute is considered to be 'public' only if name doesn't
        start with an underscore (including the special / magic attributes).
        The returned list is sorted alphabetically.
        
        Signature:
            None -> list(str)
        
        Version 0.0.1.0
        """
        strlstTemp = []
        for strAttr, objValue in self.__dict__.items():
            bCond1 = not inspect.ismethod(objValue)
            bCond2 = not inspect.isfunction(objValue)
            bCond3 = not inspect.isbuiltin(objValue)
            bCond4 = not strAttr.startswith('_')
            bCond5 = not (strAttr in strlstTemp)
            bCond = bCond1 and bCond2 and bCond3 and bCond4 and bCond5
            if bCond:
                strlstTemp.append(strAttr)
        for clsBase in self.__class__.__mro__:
            for strAttr, objValue in clsBase.__dict__.items():
                bCond1 = not isinstance(objValue, (staticmethod, classmethod))
                bCond2 = not inspect.isfunction(objValue)
                bCond3 = not strAttr.startswith('_')
                bCond4 = not (strAttr in strlstTemp)
                bCond = bCond1 and bCond2 and bCond3 and bCond4
                if bCond:
                    strlstTemp.append(strAttr)
        return list(sorted(strlstTemp))
    
    def getMethods(self):
        """
        Returns as a list of strings the names of all 'public' methods
        (class, static or instance methods, as well as function of foreign class
        methods references stored as instance attributes) which can be called
        from an instance of a class. An attribute is considered to be 'public'
        only if name doesn't start with an underscore (including the special /
        magic attributes). The returned list is sorted alphabetically.
        
        Signature:
            None -> list(str)
        
        Version 0.0.1.0
        """
        strlstTemp = []
        for strAttr, objValue in self.__dict__.items():
            bCond1 = inspect.ismethod(objValue)
            bCond2 = inspect.isfunction(objValue)
            bCond3 = inspect.isbuiltin(objValue)
            bCond4 = not strAttr.startswith('_')
            bCond5 = not (strAttr in strlstTemp)
            bCond = (bCond1 or bCond2 or bCond3) and bCond4 and bCond5
            if bCond:
                strlstTemp.append(strAttr)
        for clsBase in self.__class__.__mro__:
            for strAttr, objValue in clsBase.__dict__.items():
                bCond1 = isinstance(objValue, (staticmethod, classmethod))
                bCond2 = inspect.ismethod(objValue)
                bCond3 = inspect.isfunction(objValue)
                bCond4 = not strAttr.startswith('_')
                bCond5 = not (strAttr in strlstTemp)
                bCond = (bCond1 or bCond2 or bCond3) and bCond4 and bCond5
                if bCond:
                    strlstTemp.append(strAttr)
        return list(sorted(strlstTemp))