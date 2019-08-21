""" Main Test file, runs all tests """
import sys
import unittest

#Include individual tests
from test_models import TestUsers, TestWholeClass
from test_app import TestUsernameExistsJson, TestHome, TestAdminInterfacePrivileges

def suite():
    """ Gather up all tests """
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(TestUsers))
    test_suite.addTest(unittest.makeSuite(TestWholeClass))
    test_suite.addTest(unittest.makeSuite(TestUsernameExistsJson))
    test_suite.addTest(unittest.makeSuite(TestHome))
    test_suite.addTest(unittest.makeSuite(TestAdminInterfacePrivileges))
    return test_suite

if __name__ == '__main__':
    test_suite = suite()
    runner = unittest.TextTestRunner()
    ret = not runner.run(suite).wasSuccessful()
    sys.exit(ret)