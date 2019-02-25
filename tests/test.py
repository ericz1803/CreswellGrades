""" Main Test file, runs all tests """
import unittest

#Include individual tests
from test_models import TestUsers, TestWholeClass

def suite():
    """ Gather up all tests """
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(TestUsers))
    test_suite.addTest(unittest.makeSuite(TestWholeClass))
    return test_suite

if __name__ == '__main__':
    test_suite = suite()
    runner = unittest.TextTestRunner()
    runner.run(test_suite)