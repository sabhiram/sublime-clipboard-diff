#!/usr/bin/env python
import unittest
import sys, os, sublime

"""
Detect SublimeText version to deal w/ v2 vs v3 deltas
"""
version = sublime.version()
print("Testing with SublimeText version: %s" % version)


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
        self.assertTrue(True)


"""
For plugin helper functions, load them so we can hit functionality
within the plugin
"""
if version < "3000":
    select_diff = sys.modules["select_diff"]
else:
    print(sys.modules.keys())
    select_diff = sys.modules["sublime-select-diff.select_diff"]

class TestSelectionDiffHelpers(unittest.TestCase):
    """
    Unit tests to validate sublime-selection-diff helper methods
    """

    def setUp(self):
        """
        Common setUp() for TestSelectionDiffHelpers
        """
        pass

    def tearDown(self):
        """
        Common tearDown() for TestSelectionDiffHelpers
        """
        pass

    def test_helper_method(self):
        """
        Validates True === True
        """
        self.assertTrue(select_diff.helper_fn(True))



def run_unit_tests():
    """
    Helper function which sets up and executes the tests in the event
    that this script is executed from the command line directly

    * Responsible for setting up the test verbosity
    * Controls which `TestCase`s can be run in what order
    """
    test_loader = unittest.TestLoader()
    test_runner = unittest.TextTestRunner(verbosity = 2)
    
    plugin_test_suite = test_loader.loadTestsFromTestCase(TestSelectionDiffPlugin)
    helper_test_suite = test_loader.loadTestsFromTestCase(TestSelectionDiffHelpers)
    test_runner.run(plugin_test_suite)
    test_runner.run(helper_test_suite)

"""
Allow tests to be run from the command line:
`python test`
"""
if __name__ == "__main__":
    run_unit_tests()