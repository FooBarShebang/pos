#!/usr/bin/python

from abc import ABCMeta

class CustomException(Exception):
    
    __metaclass__ = ABCMeta
    
    @classmethod
    def __subclasshook__(cls, clsOther):
        if cls is CustomException:
            bCond1 = hasattr(clsOther, 'traceback')
            bCond2 = issubclass(clsOther, Exception)
            if bCond1 and bCond2:
                print 'case 1'
                gResult = True
            elif not bCond2:
                print 'case 2'
                gResult = False
            else:
                print 'case 3'
                gResult = NotImplemented
        else:
            print 'case 4'
            gResult = NotImplemented
        return gResult

class MyMixin(object):
    
    def traceback(self):
        pass

class VirtualChild(Exception, MyMixin):
    pass

class DirectChild(CustomException):
    pass

class VirtualGrandchild(VirtualChild):
    pass

class IndirectChild(DirectChild):
    pass

if __name__ == "__main__":
    #at instance level
    print 'At instance level - isinstance()'
    objTest = CustomException()
    print "CustomException() -> Exception ?", isinstance(objTest, Exception)
    print "CustomException() -> CustomException ?",isinstance(objTest, CustomException)
    objTest = MyMixin()
    print "MyMixin() -> Exception ?", isinstance(objTest, Exception)
    print "MyMixin() -> CustomException ?", isinstance(objTest, CustomException)
    objTest = VirtualChild()
    print "VirtualChild() -> Exception ?", isinstance(objTest, Exception)
    print "VirtualChild() -> CustomException ?", isinstance(objTest, CustomException)
    objTest = DirectChild()
    print "DirectChild() -> Exception ?", isinstance(objTest, Exception)
    print "DirectChild() -> CustomException ?", isinstance(objTest, CustomException)
    objTest = VirtualGrandchild()
    print "VirtualGrandchild() -> Exception ?", isinstance(objTest, Exception)
    print "VirtualGrandchild() -> CustomException ?", isinstance(objTest, CustomException)
    print "VirtualGrandchild() -> VirtualChild ?", isinstance(objTest, VirtualChild)
    print "VirtualGrandchild() -> DirectChild ?", isinstance(objTest, DirectChild)
    objTest = IndirectChild()
    print "IndirectChild() -> Exception ?", isinstance(objTest, Exception)
    print "IndirectChild() -> CustomException ?", isinstance(objTest, CustomException)
    print "IndirectChild() -> VirtualChild ?", isinstance(objTest, VirtualChild)
    print "IndirectChild() -> DirectChild ?", isinstance(objTest, DirectChild)
