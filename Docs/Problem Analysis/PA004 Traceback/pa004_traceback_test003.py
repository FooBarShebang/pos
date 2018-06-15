#!/usr/bin/python

import traceback

class CustomError(StandardError):
    
    def __init__(self, strMessage):
        super(CustomError, self).__init__(strMessage)
        self._traceback = traceback.extract_stack()
    
    def printTraceback(self):
        print self.message
        print self.args
        print repr(self._traceback)

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