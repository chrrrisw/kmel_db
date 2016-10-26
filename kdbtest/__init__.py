"""
Extends Python's unittest to include coverage
"""

__all__ = ['TestResult', 'TestCase', 'TestSuite',
           'TextTestRunner', 'TestLoader', 'FunctionTestCase', 'main',
           'defaultTestLoader', 'SkipTest', 'skip', 'skipIf', 'skipUnless',
           'expectedFailure', 'TextTestResult', 'installHandler',
           'registerResult', 'removeResult', 'removeHandler']

# Expose obsolete functions for backwards compatibility
__all__.extend(['getTestCaseNames', 'makeSuite', 'findTestCases'])

__unittest = True

from unittest.result import TestResult
from unittest.case import (
    TestCase, FunctionTestCase, SkipTest, skip, skipIf,
    skipUnless, expectedFailure)
from unittest.suite import BaseTestSuite, TestSuite
from unittest.loader import (
    TestLoader, defaultTestLoader, makeSuite, getTestCaseNames,
    findTestCases)
from unittest.main import TestProgram, main
from unittest.runner import TextTestRunner, TextTestResult
from unittest.signals import installHandler, registerResult, removeResult, removeHandler

# deprecated
_TextTestResult = TextTestResult
