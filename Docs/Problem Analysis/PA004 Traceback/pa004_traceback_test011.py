#!/usr/bin/python

from pa004_traceback_test010 import TestClass, CustomError

if __name__ == '__main__':
    try:
        TestObject = TestClass()
        TestObject.outer()
    except CustomError as err:
        err.printTraceback()