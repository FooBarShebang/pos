#!/usr/bin/python

class DescriptorClass(object):
    
    def __init__(self, strName, gValue):
        print 'Initializing {} with {} value'.format(strName, gValue)
        self.Name = strName
        self.Value = gValue
    
    def __get__(self, obj, objType = None):
        if obj is None:
            strName = 'not an instance (None)'
        else:
            strName = 'instance id = {}'.format(id(obj))
        print 'Read access to {} by {} of {}'.format(self.Name, strName,
                                                            objType.__name__)
        return self.Value
    
    def __set__(self, obj, gValue):
        if obj is None:
            strName = 'not an instance (None)'
        else:
            strName = 'instance id = {}'.format(id(obj))
        print 'Updating {} with value {} requested by {} of {}'.format(
                            self.Name, gValue, strName, obj.__class__.__name__)
        self.Value = gValue

class TestClassMeta(type):
    
    def __setattr__(self, strAttr, gValue):
        objOwner = type.__getattribute__(self, '__class__')
        lstMRO = type.__getattribute__(self, '__mro__')
        print 'In metaclass __setattr__() setting {}'.format(strAttr)
        for objTemp in lstMRO:
            dictVars = type.__getattribute__(objTemp, '__dict__')
            if strAttr in dictVars.keys():
                objTemp = dictVars[strAttr]
                if hasattr(objTemp, '__set__'):
                    print 'via descriptor'
                    objTemp.__set__(self, gValue)
                else:
                    print 'directly'
                    objTemp = gValue
                break
        else:
            # doesn't exist yet
            print 'creating class attribute {}'.format(strAttr)
            type.__setattr__(self, strAttr, gValue)

class TestClass(object):
    
    #class attributes
    
    __metaclass__ = TestClassMeta
    
    A = DescriptorClass('class attribute', 1)
    
    def __init__(self):
        self.B = DescriptorClass('instance attribute', 3)
    
    def __getattribute__(self, strAttr):
        objOwner = object.__getattribute__(self, '__class__')
        objTemp = object.__getattribute__(self, strAttr)
        print 'In instance __getattribute__() getting {}'.format(strAttr)
        if hasattr(objTemp, '__get__'):
            print 'via descriptor'
            objResult = objTemp.__get__(self, objOwner)
        else:
            print 'directly'
            objResult = objTemp
        return objResult
    
    def __setattr__(self, strAttr, gValue):
        objOwner = object.__getattribute__(self, '__class__')
        print 'In instance __setattr__() setting {}'.format(strAttr)
        try:
            objTemp = object.__getattribute__(self, strAttr)
            if hasattr(objTemp, '__set__'):
                print 'via descriptor'
                objTemp.__set__(self, gValue)
            else:
                print 'directly'
                objTemp = gValue
        except AttributeError:
            # doesn't exist yet
            print 'creating instance attribute {}'.format(strAttr)
            object.__setattr__(self, strAttr, gValue)

class ChildTestClass(TestClass):
    
    #simple inheritance
    
    pass

#testing area

objTest1 = TestClass()
objTest2 = ChildTestClass()
print objTest1.A
print objTest1.B
print objTest2.A
print objTest2.B
objTest1.A = 2
print objTest1.A
objTest1.B = 4
print objTest1.B
print objTest2.A
print objTest2.B
print TestClass.A
TestClass.A = 6
print TestClass.A
print ChildTestClass.A
ChildTestClass.A = 8
print ChildTestClass.A
print objTest1.A
print objTest1.B
print objTest2.A
print objTest2.B