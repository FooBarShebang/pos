#usr/bin/python
"""
Module pos.utils.loggers

Custom loggers to the console or to the console and a file, which allow dynamic
enabling and disabling of the output. Emulates 'virtual inheritance' from the
logging.Logger class by redirecting the attribute access; thus the implemented
classes provide direct access to all methods and data fields expected from an
instance of the logging.Logger class.

Implements the support of the loggers ancestor - descendant hierarchy: the names
of the loggers with the dots are supposed to indicate such relation: logger
'parent.child.grandchild' is descendant of 'parent.child', which is descendant
of 'parent' logger, even if it does not exist. The actual existence of the
supposed ancestors affects only the message propagation, but not the creation of
a logger, which can easily be 'orphan'.

The dynamic enabling / disabling of the console logging has an effect only on
the 'root' logger of the hierarchy and affects all its descendant; whereas
enabling / disabling of the console logging of a descendant logger has no effect
at all. The file logging can be enabled / disabled for each of the logger in the
hierarchy independently.

Classes:
    ConsoleLogger
        DualLogger

Warning:
    Due to the implementation of the 'virtual inheritance' the behavior of the
    function logging.getLogger() may be confusing. Suppose, that the class
    ConsoleLogger is instantiated as MyLoggger = ConsoleLogger('LoggerMy'). The
    call logging.getLogger('MyLogger') will return the reference to an instance
    of logging.Logger class, namely the value of MyLogger._logger, and not the
    instance MyLogger itself.
"""

__version__ = "0.0.1.0"
__date__ = "15-08-2018"
__status__ = "Production"

#imports

#+standard libraries

import logging
import datetime

#classes

class ConsoleLogger(object):
    """
    Custom logger class implementing logging into the console, which can be
    suppressed or re-enabled dynamically.
    
    Note that due to the support of the loggers ancestor - descendant hierarchy
    the names of the loggers with the dots are supposed to indicate such
    relation: logger 'parent.child.grandchild' is descendant of 'parent.child',
    which is descendant of 'parent' logger, even if it does not exist. The
    actual existence of the supposed ancestors affects only the message
    propagation, but not the creation of a logger, which can easily be 'orphan'.
    
    The dynamic enabling / disabling of the console logging has an effect only
    on the 'root' logger of the hierarchy and affects all its descendant;
    whereas enabling / disabling of the console logging of a descendant logger
    has no effect at all.
    
    By default, the logger event logging level is set to logging.DEBUG, but it
    can be changed at any moment using inherited method setLevel() as well as
    during the instantiation. The logging into console is enabled at the level
    logging.INFO. The console logging level can be changed, as well as the
    console logging may be entirely suppressed and then re-enabled.
    
    Any class instance has a hidden 'dummy' handler of NullHandler class, thus
    the real console logging handler can be disabled without complains from the
    logging module.
    
    The default format of a log entry is a 3-lines string:
        * logging level, date and time in ASCII format, name of the module, name
            of the logger (not its class), name of the calling function
        * line number within and the path to the module, where the logging entry
            is issued
        * actual message sent the logger
    
    Virtually 'inherits' all API from the class logging.Logger by attribute
    resolution redirection, and adds new data fields and methods.
    
    Attributes:
        console: instance of logging.StreamHandler class, can be used for the
            direct access to the console logger handler
        formatter: instance of logging.Formatter class, can be used for the
            changing of the log entries format
    
    Methods:
        setConsoleLoggingLevel()
            int -> None
        enableConsoleLogging()
            None -> None
        disableConsoleLogging()
            None -> None
    
    Version 0.0.1.0
    """
    
    #special methods
    
    def __init__(self, strName, level = logging.DEBUG):
        """
        Initialization method, which sets the logger instance name and logging
        level.
        
        Note that due to the support of the loggers ancestor - descendant
        hierarchy the names with the dots are supposed to indicate such relation
        as logger 'parent.child.grandchild' is descendant of 'parent.child',
        which is descendant of 'parent' logger, even if it does not exist.
        
        Signature:
            str/, int/ -> None
        
        Args:
            strName: string, the name of the logger to be created; it will be
                displayed as a part of the log entries, and it determines the
                loggers hierarchy (ancestor - descendant)
            level: (optional) non-negative integer, the logging level, e.g.
                logging.DEBUG, logging.WARNING, etc.
        
        Version 0.0.1.0
        """
        self.__dict__['_logger'] = logging.getLogger(strName)
        self._logger.setLevel(level)
        self.formatter = logging.Formatter('\n'.join([
            '<<%(levelname)s>> %(asctime)s @%(module)s.%(name)s.%(funcName)s',
                'Line %(lineno)d in %(pathname)s', '%(message)s']),
                                                        '%Y-%m-%d %H:%M:%S')
        self.addHandler(logging.NullHandler()) #dummy
        self.console = logging.StreamHandler()
        self.console.setLevel(logging.INFO)
        self.console.setFormatter(self.formatter)
        self.enableConsoleLogging()
    
    def __getattribute__(self, strName):
        """
        Modified getter method of the attributes resolution. Redirects the
        resolution scheme such, that the attributes of an instance of the class
        logging.Logger (referenced by the instance attribute self._logger) can
        be accessed directly, e.g. the call self.info(msg) is equivalent to the
        call self._logger.info(msg).
        
        Signature:
            str -> type A
        
        Args:
            strName: string, name of an attribute to obtain
        
        Returns:
            type A: the value of an attribute self._logger.strName (if exists)
                or self.strName (if exists, but not within self._logger)
        
        Raises:
            AttributeError: an attribute with this name is not found within
                the current object (or its ancestors) nor within the attribute
                _logger of the current object
        
        Version 0.0.1.0
        """
        if strName == '__dict__':
            #walk around for the initial assignment to self._logger via
            #+ self.__dict__['_logger'] = ...
            objResult = object.__getattribute__(self, '__dict__')
        else:
            objTemp = object.__getattribute__(self, '_logger')
            if hasattr(objTemp, strName):
                objResult = object.__getattribute__(self._logger, strName)
            else:
                objResult = object.__getattribute__(self, strName)
        return objResult
    
    def __setattr__(self, strName, gValue):
        """
        Modified setter method of the attributes resolution. Redirects the
        resolution scheme such, that the attributes of an instance of the class
        logging.Logger (referenced by the instance attribute self._logger) can
        be accessed directly, e.g. the call self.info(msg) is equivalent to the
        call self._logger.info(msg).
        
        Signature:
            str, type A -> None
        
        Args:
            strName: string, name of an attribute to assign to
            gValue: any type, the value to be assigned
        
        Version 0.0.1.0
        """
        if hasattr(self._logger, strName):
            object.__setattr__(self._logger, strName, gValue)
        else:
            object.__setattr__(self, strName, gValue)
    
    #public instance methods
    
    def enableConsoleLogging(self):
        """
        Method to enable logging into the console.
        
        The dynamic enabling / disabling of the console logging has an effect
        only on the 'root' logger of the hierarchy and affects all its
        descendant; it has no effect at all on a descendant logger.
        
        Signature:
            None -> None
        
        Version 0.0.1.0
        """
        if isinstance(self.parent, logging.RootLogger):
            self._logger.addHandler(self.console)
    
    def disableConsoleLogging(self):
        """
        Method to disable logging into the console.
        
        The dynamic enabling / disabling of the console logging has an effect
        only on the 'root' logger of the hierarchy and affects all its
        descendant; it has no effect at all on a descendant logger.
        
        Signature:
            None -> None
        
        Version 0.0.1.0
        """
        self._logger.removeHandler(self.console)
    
    def setConsoleLoggingLevel(self, level):
        """
        Method to change the logging level of the handler for the logging into
        the console. Basically, an alias for self.console.setLevel(level).
        
        Signature:
            int -> None
        
        Args:
            level: non-negative integer, the logging level, e.g. logging.DEBUG,
                logging.WARNING, etc
        
        Version 0.0.1.0
        """
        self.console.setLevel(level)

class DualLogger(ConsoleLogger):
    """
    Custom logger class implementing logging into the console and / or into a
    file, which can be suppressed or re-enabled dynamically.
    
    Note that due to the support of the loggers ancestor - descendant hierarchy
    the names of the loggers with the dots are supposed to indicate such
    relation: logger 'parent.child.grandchild' is descendant of 'parent.child',
    which is descendant of 'parent' logger, even if it does not exist. The
    actual existence of the supposed ancestors affects only the message
    propagation, but not the creation of a logger, which can easily be 'orphan'.
    
    The dynamic enabling / disabling of the console logging has an effect only
    on the 'root' logger of the hierarchy and affects all its descendant;
    whereas enabling / disabling of the console logging of a descendant logger
    has no effect at all. The file logging can be enabled / disabled for each
    of the logger in the hierarchy independently.
    
    By default, the logger event logging level is set to logging.DEBUG, but it
    can be changed at any moment using inherited method setLevel() as well as
    during the instantiation. The logging into console is enabled at the level
    logging.INFO. The console logging level can be changed, as well as the
    console logging may be entirely suppressed and then re-enabled.
    
    The logging into a file is disabled initially unless explicitly asked
    otherwise during the instantiation, whilst the default file logging level is
    set to logging.WARNING. If the name of the log file to be used is not
    specified, its created automatically by the date and time of instantiation
    and the logger instance name, even if the file logging is disabled.
    
    Implementation details:
        * has a hidden 'dummy' handler of NullHandler class, thus the both real
            handlers can be disabled without complains from the logging
            functionality
        * actual log file is not created / re-opened until the file logging is
            enabled implicitly (or by setting the flag to True during the
            instantiation)
        * call to the method changeLogFile() automatically enables the file
            logging, thus log file is created / re-opened
        * the log files are created / re-opened in the 'w' mode, thus clearing
            their previous content, but disabling / suppressing of the file
            logging doesn't actually closes the log file, therefore the re-
            enabling of the file logging doesn't delete the previously made
            entries
    
    The default format of a log entry is a 3-lines string:
        * logging level, date and time in ASCII format, name of the module, name
            of the logger (not its class), name of the calling function
        * line number within and the path to the module, where the logging entry
            is issued
        * actual message sent the logger
    
    Virtually 'inherits' all API from the class logging.Logger by attribute
    resolution redirection via its direct super class ConsoleLogger, and adds
    new data fields and methods.
    
    Attributes:
        console: instance of logging.StreamHandler class, can be used for the
            direct access to the console logger handler
        file_logging: instance of logging.FileHandler or logging.NullHandler
            class, can be used for the direct access to the file logger handler
        formatter: instance of logging.Formatter class, can be used for the
            changing of the log entries format
    
    Methods:
        setConsoleLoggingLevel()
            int -> None
        enableConsoleLogging()
            None -> None
        disableConsoleLogging()
            None -> None
        setFileLoggingLevel()
            int -> None
        enableFileLogging()
            None -> None
        disableFileLogging()
            None -> None
        changeLogFile()
            /str/ -> None
    
    Version 0.0.1.0
    """
    
    #special methods
    
    def __init__(self, strName, bLogToFile = False, strFileName = None,
                    level = logging.DEBUG):
        """
        Initialization method, which sets the logger instance name, logging
        level and log file (even if the logging into a file is suppressed).
        
        Note that due to the support of the loggers ancestor - descendant
        hierarchy the names with the dots are supposed to indicate such relation
        as logger 'parent.child.grandchild' is descendant of 'parent.child',
        which is descendant of 'parent' logger, even if it does not exist.
        
        If optional file name is not passed during instantiation of the class,
        it is defined automatically from the current date and time as well as
        the 'name' of the logger instance with the extension '.log'. Otherwise,
        the file name passed during instantiation of the class is remembered
        with the standard convention on absolute / relative to the current
        working directory path being applied.
        
        Note that the log file is not created / opened immediately if the
        second (optional) argument - boolean flag - is False, i.e. the logging
        into a file is suppressed. However, if the file logging is enabled, the
        actual log file is created or re-opened in 'w' mode using the filename
        passed into this method or automatically defined during the
        instantiation.
        
        Signature:
            str/, bool, str, int/ -> None
        
        Args:
            strName: string, the name of the logger to be created; it will be
                displayed as a part of the log entries, and can be used for the
                (de-) selection of this particular logger from the pool of the
                available ones, see function logging.getLogger()
            bLogToFile: (optional) boolean flag, if the file logging is to be
                initially enabled
            strFileName: (optional) string, filename to be used for the log file
                if the file logging is enabled
            level: (optional) non-negative integer, the logging level, e.g.
                logging.DEBUG, logging.WARNING, etc.
        
        Version 0.0.1.0
        """
        super(DualLogger, self).__init__(strName, level = level)
        if strFileName is None:
            self.log_file = '{}_{}.log'.format(
                datetime.datetime.now().strftime('%Y-%m-%d %H_%M_%S'), strName)
        else:
            self.log_file = str(strFileName)
        if bLogToFile:
            self.file_logging = logging.FileHandler(self.log_file, mode = 'w')
        else:
            self.file_logging = logging.NullHandler()
        self.file_logging.setLevel(logging.WARNING)
        self.file_logging.setFormatter(self.formatter)
        if bLogToFile and isinstance(self.parent, logging.RootLogger):
            self.enableFileLogging()
    
    #public instance methods
    
    def enableFileLogging(self):
        """
        Method to enable logging into a file. If the logging into the file was
        not enabled upon instantiation of the class, a log file is created;
        otherwise the existing log file is 're-used'.
        
        If optional file name is not passed during instantiation of the class,
        it is defined automatically from the date and time of instantiation as
        well as the 'name' of the logger instance with the extension '.log'.
        Otherwise, the file name passed during instantiation of the class is
        used with the standard convention on absolute / relative to the current
        working directory path being applied.
        
        Note that the file logging can be enabled / disabled for each of the
        logger in the hierarchy independently.
        
        Signature:
            None -> None
        
        Version 0.0.1.0
        """
        if isinstance(self.file_logging, logging.NullHandler):
            iCurrentLevel = self.file_logging.level
            self._logger.removeHandler(self.file_logging)
            del self.file_logging
            self.file_logging = logging.FileHandler(self.log_file, mode = 'w')
            self.file_logging.setLevel(iCurrentLevel)
            self.file_logging.setFormatter(self.formatter)
        self._logger.addHandler(self.file_logging)
    
    def disableFileLogging(self):
        """
        Method to disable logging into a file. Note that the active log file is
        not actually closed, its handler is simply removed from the list of
        handlers. Therefore, is the file logging is re-enabled later, the
        already made log entries are not removed.
        
        Note that the file logging can be enabled / disabled for each of the
        logger in the hierarchy independently.
        
        Signature:
            None -> None
        
        Version 0.0.1.0
        """
        if isinstance(self.file_logging, logging.FileHandler):
            self._logger.removeHandler(self.file_logging)
    
    def setFileLoggingLevel(self, level):
        """
        Method to change the logging level of the handler for the logging into
        a file. Basically, an alias for self.file_logging.setLevel(level).
        
        Signature:
            int -> None
        
        Args:
            level: non-negative integer, the logging level, e.g. logging.DEBUG,
            logging.WARNING, etc.
        
        Version 0.0.1.0
        """
        self.file_logging.setLevel(level)
    
    def changeLogFile(self, strFileName = None):
        """
        Method to change the active log file. If logging to a file was disabled
        this method automatically enables it. Otherwise, the log file used
        before is closed, and the new log file is created.
        
        If optional file name is not passed, it is defined automatically from
        the current date and time as well as the 'name' of the logger instance
        with the extension '.log'. Note that in this case the log file is
        created in the current working directory.
        
        Signature:
            /str/ -> None
        
        Args:
            strFileName: (optional) string, or any type convertible to a string,
                the filename of a log file to switch to; the standard convention
                on absolute / relative to the current working directory path is
                applied.
        
        Version 0.0.1.0
        """
        iCurrentLevel = self.file_logging.level
        if strFileName is None:
            self.log_file = '{}_{}.log'.format(
                datetime.datetime.now().strftime('%Y-%m-%d %H_%M_%S'),
                    self.name)
        else:
            self.log_file = str(strFileName)
        self.file_logging.close()
        self._logger.removeHandler(self.file_logging)
        del self.file_logging
        self.file_logging = logging.FileHandler(self.log_file, mode = 'w')
        self.file_logging.setLevel(iCurrentLevel)
        self.file_logging.setFormatter(self.formatter)
        self._logger.addHandler(self.file_logging)