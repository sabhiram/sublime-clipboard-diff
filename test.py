#!/usr/bin/env python

import unittest
import select_diff

class TestSelectionDiffPlugin(unittest.TestCase):
    """
    Unit tests to validate sublime-selection-diff plugin methods
    """

    def setUp(self):
        """
        Common setUp() for TestSelectionDiffPlugin
        """
        pass

    def tearDown(self):
        """
        Common tearDown() for TestSelectionDiffPlugin
        """
        pass

    def test_initial(self):
        """
        Validates True === True
        """
        self.assertTrue(select_diff.some_method())


def run_unit_tests():
    """
    Helper function which sets up and executes the tests in the event
    that this script is executed from the command line directly

    * Responsible for setting up the test verbosity
    * Controls which `TestCase`s can be run in what order
    """
    test_loader = unittest.TestLoader()
    test_runner = unittest.TextTestRunner(verbosity = 2)
    
    test_suite = test_loader.loadTestsFromTestCase(TestSelectionDiffPlugin)
    test_runner.run(test_suite)

"""
Allow tests to be run from the command line:
`python test`
"""
if __name__ == "__main__":
    run_unit_tests()