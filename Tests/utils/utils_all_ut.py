#usr/bin/python
"""
Module pos.Tests.utils.utils_all_ut

Aggregation of the unit tests for all modules within pos.utils package
"""

__version__ = "0.0.1.0"
__date__ = "19-06-2018"
__status__ = "Testing"

#imports

#+ standard libraries

import sys
import unittest

#+ other test modules

import pos.Tests.utils.traceback_ut as tb

#classes

#+ test suite

TestSuite = unittest.TestSuite([tb.TestSuite])

if __name__ == "__main__":
    sys.stdout.write("Conducting pos.utils package tests...\n")
    sys.stdout.flush()
    unittest.TextTestRunner(verbosity = 2).run(TestSuite)