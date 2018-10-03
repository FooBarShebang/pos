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
    #in try...except
    print "raise CustomException()"
    try:
        raise CustomException()
    except Exception:
        print 'Caught as Exception'
    except:
        print 'Not caught as Exception'
    try:
        raise CustomException()
    except CustomException:
        print 'Caught as CustomException'
    except:
        print 'Not caught as CustomException'
    print "raise DirectChild()"
    try:
        raise DirectChild()
    except Exception:
        print 'Caught as Exception'
    except:
        print 'Not caught as Exception'
    try:
        raise DirectChild()
    except CustomException:
        print 'Caught as CustomException'
    except:
        print 'Not caught as CustomException'
    try:
        raise DirectChild()
    except DirectChild:
        print 'Caught as DirectChild'
    except:
        print 'Not caught as DirectChild'
    try:
        raise DirectChild()
    except VirtualChild:
        print 'Caught as VirtualChild'
    except:
        print 'Not caught as VirtualChild'
    print "raise VirtualChild()"
    try:
        raise VirtualChild()
    except Exception:
        print 'Caught as Exception'
    except:
        print 'Not caught as Exception'
    try:
        raise VirtualChild()
    except CustomException:
        print 'Caught as CustomException'
    except:
        print 'Not caught as CustomException'
    try:
        raise VirtualChild()
    except DirectChild:
        print 'Caught as DirectChild'
    except:
        print 'Not caught as DirectChild'
    try:
        raise VirtualChild()
    except VirtualChild:
        print 'Caught as VirtualChild'
    except:
        print 'Not caught as VirtualChild'
    print "raise IndirectChild()"
    try:
        raise IndirectChild()
    except Exception:
        print 'Caught as Exception'
    except:
        print 'Not caught as Exception'
    try:
        raise IndirectChild()
    except CustomException:
        print 'Caught as CustomException'
    except:
        print 'Not caught as CustomException'
    try:
        raise IndirectChild()
    except DirectChild:
        print 'Caught as DirectChild'
    except:
        print 'Not caught as DirectChild'
    try:
        raise IndirectChild()
    except VirtualChild:
        print 'Caught as VirtualChild'
    except:
        print 'Not caught as VirtualChild'
    print "raise VirtualGrandchild()"
    try:
        raise VirtualGrandchild()
    except Exception:
        print 'Caught as Exception'
    except:
        print 'Not caught as Exception'
    try:
        raise VirtualGrandchild()
    except CustomException:
        print 'Caught as CustomException'
    except:
        print 'Not caught as CustomException'
    try:
        raise VirtualGrandchild()
    except DirectChild:
        print 'Caught as DirectChild'
    except:
        print 'Not caught as DirectChild'
    try:
        raise VirtualGrandchild()
    except VirtualChild:
        print 'Caught as VirtualChild'
    except:
        print 'Not caught as VirtualChild'
