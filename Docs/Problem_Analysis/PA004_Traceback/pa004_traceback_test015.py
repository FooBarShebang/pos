#!/usr/bin/python

from pa004_traceback_test013 import CustomError, UnawareError
from pa004_traceback_test014 import TestClass, outer_func

if __name__ == '__main__':
    TestObject = TestClass()
    try:
        TestObject.outer()
    except CustomError as err:
        print err.FullInfo, '\n'
    try:
        TestClass.outer_class()
    except CustomError as err:
        print err.FullInfo, '\n'
    try:
        TestObject.call_outside()
    except CustomError as err:
        print err.FullInfo, '\n'
    try:
        TestObject.outer_class()
    except CustomError as err:
        try:
            raise CustomError('Caught and raised simple')
        except CustomError as err_inner:
            print err_inner.FullInfo, '\n'
    try:
        TestObject.outer_class()
    except CustomError as err:
        try:
            objTraceback = err.Traceback
            raise CustomError('Caught and raised smart', Traceback=objTraceback)
        except CustomError as err_inner:
            print err_inner.FullInfo, '\n'
    try:
        raise UnawareError('some generic error')
    except UnawareError as err:
        print err.FullInfo