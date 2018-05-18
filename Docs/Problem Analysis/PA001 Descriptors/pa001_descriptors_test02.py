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

class TestClass(object):
    
    #class attributes
    
    A = DescriptorClass('class attribute', 1)
    
    def __init__(self):
        self.B = DescriptorClass('instance attribute', 1)

#testing area

objTest1 = TestClass()
objTest2 = TestClass()
print objTest1.A
print objTest2.A
print objTest1.B
print objTest2.B
objTest1.A = 2
print objTest1.A
print objTest2.A
objTest1.B = 2
print objTest1.B
print objTest2.B