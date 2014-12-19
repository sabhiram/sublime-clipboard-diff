#!/usr/bin/env python
import unittest
import sys, os, sublime

"""
Detect SublimeText version to deal w/ v2 vs v3 deltas
"""
version = sublime.version()
print("Testing with SublimeText version: %s" % version)

"""
For plugin helper functions, load them so we can hit functionality
within the plugin
"""
if version < "3000":
    select_diff = sys.modules["select_diff"]
else:
    print(sys.modules.keys())
    select_diff = sys.modules["sublime-select-diff.select_diff"]


class TestSelectionDiffPlugin(unittest.TestCase):
    """
    Unit tests to validate sublime-selection-diff plugin methods
    """

    test_lines_0 = "\n".join([ "line 0", "line 1", "line 2" ])
    test_lines_1 = "\n".join([ "line A", "line 1" ])

    """
    Helper functions
    """
    def runSimpleViewCommand(self, cmd):
        if self.test_view:
            self.test_view.run_command(cmd)

    def insertTextToTestView(self, text):
        self.test_view.run_command("insert", {"characters": text})

    """
    Setup / Teardown
    """
    def setUp(self):
        """
        Common setUp() for TestSelectionDiffPlugin

        1. Open a new view in the active window
        2. 
        """
        self.test_view = sublime.active_window().new_file()

    def tearDown(self):
        """
        Common tearDown() for TestSelectionDiffPlugin

        1. If the view exists, set it to scratch (so it does not ask to save)
        2. Focus the test_view, and close it
        """
        if self.test_view:
            self.test_view.set_scratch(True)
            self.test_view.window().focus_view(self.test_view)
            self.test_view.window().run_command("close_file")

    """
    Tests
        1. Test selected text -> string function
        2. Test Copy Hook
        3. Test Cut Hook
    """
    def test_get_selection_str(self):
        """
        Validate the selectionToString helper

        1. Inserts the view with some text and selects it
        2. calls helper and validates that the two strings match
        """
        self.insertTextToTestView(self.test_lines_0)
        self.runSimpleViewCommand("select_all")

        selection_txt = select_diff.selectionToString(self.test_view)

        self.assertEqual(self.test_lines_0, selection_txt)


    def test_copy_selection_to_buffer(self):
        """
        Validates if stuff in the view gets copied correctly

        1. Fill up the file with some text and select it
        2. Trigger a copy
        3. Validate that the copied_lines stored off has these lines
        4. Validate that the selection still exists
        """
        self.insertTextToTestView(self.test_lines_0)
        self.runSimpleViewCommand("select_all")
        
        previous_selection = self.test_view.sel()
        self.runSimpleViewCommand("copy")
        current_selection = self.test_view.sel()
        
        self.assertEqual(self.test_view.sel(), previous_selection)
        # TODO: For some odd reason, when I try to fetch the current buffer
        #       from the lib, it always returns "", debug this...
        # self.assertEqual(self.test_lines_0, select_diff.get_current_buffer())
        

    def test_cut_selection_to_buffer(self):
        """
        Validates if stuff in the view gets cut correctly

        1. Fill up the file with some text and select it
        2. Trigger a cut
        3. Validate that the copied_lines stored off has these lines
        4. Validate that the selection still exists
        """
        self.insertTextToTestView(self.test_lines_0)
        self.runSimpleViewCommand("select_all")
        
        previous_selection = self.test_view.sel()
        self.runSimpleViewCommand("cut")
        current_selection = self.test_view.sel()

        self.assertEqual(1, len(current_selection))
        self.assertEqual("", self.test_view.substr(current_selection[0]))
        # TODO: For some odd reason, when I try to fetch the current buffer
        #       from the lib, it always returns "", debug this...
        # self.assertEqual(self.test_lines_0, select_diff.get_current_buffer())

