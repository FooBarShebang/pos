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
    #at class level
    print 'At class level - issubclass()'
    print "CustomException -|> Exception ?", issubclass(CustomException, Exception)
    print "CustomException -|> CustomException ?", issubclass(CustomException, CustomException)
    print "MyMixin -|> Exception ?", issubclass(MyMixin, Exception)
    print "MyMixin -|> CustomException ?", issubclass(MyMixin, CustomException)
    print "VirtualChild -|> Exception ?", issubclass(VirtualChild, Exception)
    print "VirtualChild -|> CustomException ?", issubclass(VirtualChild, CustomException)
    print "DirectChild -|> Exception ?", issubclass(DirectChild, Exception)
    print "DirectChild -|> CustomException ?", issubclass(DirectChild, CustomException)
    print "VirtualGrandchild -|> Exception ?", issubclass(VirtualGrandchild, Exception)
    print "VirtualGrandchild -|> CustomException ?", issubclass(VirtualGrandchild, CustomException)
    print "IndirectChild -|> Exception ?", issubclass(IndirectChild, Exception)
    print "IndirectChild -|> CustomException ?", issubclass(IndirectChild, CustomException)
    print "VirtualGrandchild -|> VirtualChild ?", issubclass(VirtualGrandchild, VirtualChild)
    print "VirtualGrandchild -|> DirectChild ?", issubclass(VirtualGrandchild, DirectChild)
    print "IndirectChild -|> VirtualChild ?", issubclass(IndirectChild, VirtualChild)
    print "IndirectChild -|> DirectChild ?", issubclass(IndirectChild, DirectChild)
