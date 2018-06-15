#!/usr/bin/python

import sys
import traceback

class ErrorMixin(object):
    
    def printTraceback(self):
        print self.message
        print self.args
        _, _, exc_traceback = sys.exc_info()
        print repr(traceback.extract_tb(exc_traceback))

class CustomError(StandardError, ErrorMixin):
    
    def __init__(self, strMessage):
        super(CustomError, self).__init__(strMessage)

class TestClass(object):
    def inner(self):
        raise CustomError('testing')

    def middle(self):
        self.inner()

    def outer(self):
        self.middle()

if __name__ == '__main__':
    try:
        TestObject = TestClass()
        TestObject.outer()
    except CustomError as err:
        err.printTraceback()