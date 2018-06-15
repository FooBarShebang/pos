#!/usr/bin/python

import traceback

class ErrorMixin(object):
    
    def __init__(self, *args, **kwargs):
        super(ErrorMixin, self).__init__(*args, **kwargs)
        self._traceback = traceback.extract_stack()
    
    def printTraceback(self):
        print self.message
        print self.args
        print repr(self._traceback)

class CustomError(ErrorMixin, StandardError):
    
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