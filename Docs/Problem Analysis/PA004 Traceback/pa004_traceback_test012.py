#!/usr/bin/python

import inspect

class TraceBack(object):
    
    ConsoleWidth = 72
    
    ContextLenght = 3
    
    def __init__(self, iSkipLastEntries = None):
        try:
            tblstTemp = inspect.trace(self.ContextLenght)
            if (isinstance(iSkipLastEntries, (int, long))
                                        and iSkipLastEntries > 0
                                        and iSkipLastEntries < len(tblstTemp)):
                self._tblstTraceback = tblstTemp[ : -iSkipLastEntries]
            else:
                self._tblstTraceback = tblstTemp
        except:
            self._tblstTraceback = None
    
    def __del__(self):
        if not (self._tblstTraceback is None):
            iLen = len(self._tblstTraceback)
            try:
                for iIdx in range(iLen):
                    for iOtherIdx in range(6):
                        del self._tblstTraceback[iIdx][iOtherIdx]
                del self._tblstTraceback
                self._tblstTraceback = None
            except:
                del self._tblstTraceback
                self._tblstTraceback = None
    
    @property
    def CallChain(self):
        strlstCallers = []
        if not (self._tblstTraceback is None):
            for tupItem in self._tblstTraceback:
                objFrame = tupItem[0]
                strModule = inspect.getmodule(objFrame).__name__
                strCaller = tupItem[3]
                if strCaller == '<module>':
                    strlstCallers.append(strModule)
                else:
                    dictLocals = objFrame.f_locals
                    if 'self' in dictLocals:
                        strClass = dictLocals['self'].__class__.__name__
                        strlstCallers.append('.'.join([strModule, strClass,
                                                                    strCaller]))
                    elif 'cls' in dictLocals:
                        strClass = dictLocals['cls'].__name__
                        strlstCallers.append('.'.join([strModule, strClass,
                                                                    strCaller]))
                    else:
                        strlstCallers.append('.'.join([strModule, strCaller]))
        return strlstCallers
    
    @property
    def FullInfo(self):
        strInfo = ''
        strlstCallers = self.CallChain
        if len(strlstCallers):
            for iIdx, tupItem in enumerate(self._tblstTraceback):
                strFilePath = tupItem[1]
                iLineNum = tupItem[2]
                strCaller = tupItem[3]
                strFullCaller = strlstCallers[iIdx]
                strlstCodeLines = tupItem[4]
                iLineIndex = tupItem[5]
                iMaxDigits = len(str(iLineNum + iLineIndex))
                if strCaller == '<module>':
                    strCallerInfo = 'In module {}'.format(strFullCaller)
                else:
                    strCallerInfo = 'Caller {}()'.format(strFullCaller)
                strFileInfo = 'Line {} in {}'.format(iLineNum, strFilePath)
                strlstCodeInfo = []
                for iLineIdx, _strLine in enumerate(strlstCodeLines):
                    strLine = _strLine.rstrip()
                    iRealLineNum = iLineNum - iLineIndex + iLineIdx
                    strLineNum = str(iRealLineNum)
                    while len(strLineNum) < iMaxDigits:
                        strLineNum = '0{}'.format(strLineNum)
                    if iRealLineNum == iLineNum:
                        strLineNum = '>{} '.format(strLineNum)
                    else:
                        strLineNum = ' {} '.format(strLineNum)
                    if len(strLine) > (self.ConsoleWidth - 2 - iMaxDigits):
                        strFullLine = '{}{}...'.format(strLineNum,
                                strLine[ : self.ConsoleWidth - 5 - iMaxDigits])
                    else:
                        strFullLine = '{}{}'.format(strLineNum, strLine)
                    strlstCodeInfo.append(strFullLine)
                strCodeInfo = '\n'.join(strlstCodeInfo)
                strInfo = '\n'.join([strInfo, strCallerInfo, strFileInfo,
                                                                strCodeInfo])
        if len(strInfo):
            strInfo = strInfo.lstrip()
        return strInfo