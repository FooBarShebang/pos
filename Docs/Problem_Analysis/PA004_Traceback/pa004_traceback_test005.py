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

def inner():
    raise CustomError('testing')

def middle():
    inner()

def outer():
    middle()

if __name__ == '__main__':
    try:
        outer()
    except CustomError as err:
        err.printTraceback()