#usr/bin/python
"""
Module pos.base_classes

Abstract Base Classes implementing the modified attributes access scheme and
the classes introspection functionality.

Classes:
    DescriptedABC: support for the data descriptors access methods in the case
        of the instance attributes and the class attributes accessed from a
        class without instantiation; also implements the basic introspection
"""

__version__ = "0.0.1.3"
__date__ = "23-07-2018"
__status__ = "Development"

#imports

#+ standard libraries

import abc
import inspect

#+ this library modules

from pos.utils.attr_info import FieldInfo, MethodInfo

#classes

#+metaclasses

class DescriptedABC_Meta(abc.ABCMeta):
    """
    Meta-class for DescriptedABC. Ensures the usage of the __set__() and
    __delete__() methods upon assignment and deletion of the class attributes
    being data descriptors when the action is performed on the class itself
    without its instantiation. Also ensures that the class attributes (as well
    as any methods) marked as 'private' or 'magic' (i.e. starting with, at
    least, one underscore) are ignored by the built-in functions dir() and
    help().
    
    Version 0.0.1.2
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
        
        Args:
            strAttr: string, name of the attribute to be changed in value
            gValue: any type, value to be assigned to the attribute
        
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
        
        Args:
            strAttr: string, name of the attribute to be deleted.
        
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
    
    def __dir__(self):
        """
        Special (magic) method. Ensures that the class attributes (fields as
        well as any methods) marked as 'private' or 'magic' (i.e. starting with,
        at least, one underscore) are ignored by the built-in functions dir()
        and help(). Returns the sorted alphabetically list of ALL 'public' class
        data fields and class / static / instance methods available at the class
        level (without instantiation), including all inherited ones, but
        excluding the special 'public' instance method onInit().
        
        Signature:
            None -> None
        
        Version 0.0.1.0
        """
        strlstAttributes = []
        for objBase in type.__getattribute__(self, '__mro__'): #go through MRO
            for strName in type.__getattribute__(objBase, '__dict__').keys():
                bCond1 = not strName.startswith('_')
                bCond2 = not (strName in strlstAttributes)
                bCond3 = strName != 'onInit'
                if bCond1 and bCond2 and bCond3:
                    strlstAttributes.append(strName)
        return list(sorted(strlstAttributes))

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
    
    Note: the class / instance attributes (fields and methods) considered to
    be 'private' or special / magic (i.e. with the names starting with, at
    least, one underscore), are hidden from all introspection methods, including
    the built-in functions dir() and help().
    
    Class methods:
        getClassFields(): None -> list(str)
        getClassInfo(): None -> str
        getClassMethods(): None -> list(str)
        inspectClassAttribute(): str -> ???
    
    Methods:
        getFields(): None -> list(str)
        getInfo(): None -> str
        getMethods(): None -> list(str)
        inspectAttribute(): str -> ???
    
    Version 0.0.1.3
    """
    
    #class fields
    
    __metaclass__ = DescriptedABC_Meta
    
    #special methods
    
    def __init__(self, *args, **kwargs):
        """
        Special method - initialization of the class. Simple passes all received
        positional and keyword arguments into the method onInit().
        
        Signature:
            /*args, **kwargs/ -> None
        
        Args:
            *args: (optional), any amount of arguments of any types, passed into
                the method onInit()
            **kwargs: (optional), keyword, any amount of arguments of any types,
                passed into the method onInit()
        
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
            /*args, **kwargs/ -> None
        
            *args: (optional), any amount of arguments of any types, not used
            **kwargs: (optional), keyword, any amount of arguments of any types,
                not used
        
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
        
        Args:
            strAttr: string, name of the attribute to be deleted.
        
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
        
        Args:
            strAttr: string, name of the attribute to be changed in value
            gValue: any type, value to be assigned to the attribute
        
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
        
        Args:
            strAttr: string, name of the attribute to be deleted.
        
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
    
    def __dir__(self):
        """
        Special (magic) method. Ensures that the class and instance attributes
        (fields as well as any methods) marked as 'private' or 'magic' (i.e.
        starting with, at least, one underscore) are ignored by the built-in
        functions dir() and help(). Returns the sorted alphabetically list of
        ALL 'public' class and instance data fields and class / static /
        instance methods available at the instance level, including all the
        inherited ones, excluding the special 'public' method onInit()
        
        Signature:
            None -> None
        
        Version 0.0.1.0
        """
        strlstAttributes = DescriptedABC_Meta.__dir__(self.__class__)
        for strName in object.__getattribute__(self, '__dict__').keys():
            bCond1 = not strName.startswith('_')
            bCond2 = not (strName in strlstAttributes)
            if bCond1 and bCond2:
                strlstAttributes.append(strName)
        return list(sorted(strlstAttributes))
    
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
    
    @classmethod
    def inspectClassAttribute(cls, strAttr):
        """
        
        
        Signature:
            str -> pos.utils.attr_info.FieldInfo
                    OR pos.utils.attr_info.MethodInfo
        
        Args:
            strAttr: string, name of the class attribute to be inspected
        
        Version 0.0.1.0
        """
        for clsBase in cls.__mro__:
            for strAttr, objValue in clsBase.__dict__.items():
                pass
    
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
                bCond4 = not (strAttr.startswith('_') or strAttr == 'onInit')
                bCond5 = not (strAttr in strlstTemp)
                bCond = (bCond1 or bCond2 or bCond3) and bCond4 and bCond5
                if bCond:
                    strlstTemp.append(strAttr)
        return list(sorted(strlstTemp))
