#!/usr/bin/python

from pa004_traceback_test012 import TraceBack

class ErrorMixin(object):
    
    @property
    def Traceback(self):
        if ((not hasattr(self, '_traceback')) or
                                (not isinstance(self._traceback, TraceBack))):
            if not hasattr(self, '_skip') or (self._skip is None):
                self._traceback = TraceBack()
            else:
                self._traceback = TraceBack(self._skip)
        return self._traceback
    
    @property
    def FullInfo(self):
        strInfo = '\n'.join([
                        '{}: {}'.format(self.__class__.__name__, self.message),
                        self.Traceback.FullInfo])
        return strInfo

class CustomError(StandardError, ErrorMixin):
    
    def __init__(self, strMessage, Traceback = None, SkipLast = None):
        if isinstance(Traceback, TraceBack):
            self._traceback = Traceback
            self._skip = None
        else:
            self._traceback = None
            if isinstance(SkipLast, (int, long)) and SkipLast > 0:
                self._skip = SkipLast
            else:
                self._skip = None
        super(CustomError, self).__init__(strMessage)

class UnawareError(StandardError, ErrorMixin):
    pass