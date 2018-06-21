#usr/bin/python
"""
Module pos.Tests.pos_all_ut

Aggregation of the unit tests for all modules within pos library
"""

__version__ = "0.0.1.1"
__date__ = "21-06-2018"
__status__ = "Testing"

#imports

#+ standard libraries

import sys
import unittest

#+ other test modules

import pos.Tests.utils.utils_all_ut as ut
import pos.Tests.exceptions_ut as exceptions

#classes

#+ test suite

TestSuite = unittest.TestSuite([ut.TestSuite, exceptions.TestSuite])

if __name__ == "__main__":
    sys.stdout.write("Conducting pos library tests...\n")
    sys.stdout.flush()
    unittest.TextTestRunner(verbosity = 2).run(TestSuite)