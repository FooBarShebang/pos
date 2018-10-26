#usr/bin/python
"""
Package pos.utils

Utility / helper modules of the pos library.

Modules:
    attr_info - classes to store and produce a string information on the class'
        attributes
    contracts - ???
    docstring_parsers - extraction or removal of documentation auto-generation
        related data from the docstring
    dynamic_import - import of modules or objects from modules dynamically, i.e.
        using their string names at the runtime
    loggers - custom loggers to the console or to the console and a file, which
        allow dynamic enabling and disabling of the output
    traceback - classes to obtain, store and analyze the stack and exception
        traceback
"""

__version__ = "0.0.1.3"
__date__ = "26-10-2018"
__status__ = "Development"

__all__ = ['traceback', 'attr_info', 'docstring_parsers', 'dynamic_import',
            'loggers']