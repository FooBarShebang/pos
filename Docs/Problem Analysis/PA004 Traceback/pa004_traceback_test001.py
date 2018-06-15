#!/usr/bin/python

import sys
import traceback

class CustomError(StandardError):
    
    def printTraceback(self):
        print self.message
        print self.args
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print exc_type, exc_value
        print repr(traceback.extract_tb(exc_traceback))
        print repr(traceback.extract_stack())

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