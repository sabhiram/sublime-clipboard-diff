#!/usr/bin/env python
import unittest
import difflib
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
    select_diff = sys.modules["sublime-select-diff.select_diff"]


"""
Python 2 vs Python 3 - Compatibility - reduce() is functools.reduce
"""
try:
    # Python 2
    _reduce = reduce
except NameError:
    # Python 3
    import functools
    _reduce = functools.reduce

class TestSelectionDiffPlugin(unittest.TestCase):
    """
    Unit tests to validate sublime-selection-diff plugin methods
    """

    test_lines_0 = "line 0\nline 1\nline 2"
    test_lines_1 = "line A\nline 1"
    diff_result  = difflib.unified_diff(
                        select_diff.getLinesHelper(test_lines_0),
                        select_diff.getLinesHelper(test_lines_1),
                        "Clipboard", "Selection")

    expected_diff_text = _reduce(lambda acc, x: acc + x, diff_result, "")
    

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
        self.test_view.set_name("Test View")
        self.test_view.set_scratch(True)

    def tearDown(self):
        """
        Common tearDown() for TestSelectionDiffPlugin

        1. If the view exists, set it to scratch (so it does not ask to save)
        2. Focus the test_view, and close it
        """
        if self.test_view:
            test_window = self.test_view.window()
            test_window.focus_view(self.test_view)
            test_window.run_command("close_file"),
            

    """
    Tests:
    
    1. Test selected text -> string function
    2. Test line helper 
    3. Test line writer to view
    4. Test Copy Hook
    5. Test Cut Hook
    6. Test Select-Diff Hook
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


    def test_line_helper(self):
        """
        Validates the line helper
        """
        lines = select_diff.getLinesHelper(self.test_lines_0)

        self.assertEqual(len(lines), 3)
        self.assertEqual(lines[0], "line 0\n")
        self.assertEqual(lines[1], "line 1\n")
        self.assertEqual(lines[2], "line 2\n")


    def test_write_to_view(self):
        """
        Validates writing to a view
        """
        lines = select_diff.getLinesHelper(self.test_lines_0)

        # TODO: Enable this once we figure out how to pass mock "edit" objects
        # select_diff.writeLinesToViewHelper(self.test_view, { "edit_token": 0 }, lines)

        self.runSimpleViewCommand("select_all")
        current_selection = self.test_view.sel()
        selected_text = select_diff.selectionToString(self.test_view)

        # TODO: Enable this once we figure out how to pass mock "edit" objects
        # self.assertEqual(self.test_lines_0, selected_text)


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
        self.runSimpleViewCommand("select_diff_copy")
        current_selection = self.test_view.sel()
        
        self.assertEqual(self.test_view.sel(), previous_selection)
        self.assertEqual(self.test_lines_0, select_diff.getCurrentBuffer())
        

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
        self.runSimpleViewCommand("select_diff_cut")
        current_selection = self.test_view.sel()

        self.assertEqual(1, len(current_selection))
        self.assertEqual("", self.test_view.substr(current_selection[0]))
        self.assertEqual(self.test_lines_0, select_diff.getCurrentBuffer())


    def test_select_diff(self):
        """
        Validates the `select_diff` command 

        1. Fill up a selection buffer
        2. Select some other stuff
        3. Diff them and check for match
        """
        self.insertTextToTestView(self.test_lines_0)
        self.runSimpleViewCommand("select_all")
        self.runSimpleViewCommand("select_diff_cut")
        self.insertTextToTestView(self.test_lines_1)
        self.runSimpleViewCommand("select_all")

        self.runSimpleViewCommand("select_diff")
        diff_view = sublime.active_window().active_view()
        diff_text = diff_view.substr(sublime.Region(0, diff_view.size()))
        diff_view.window().run_command("close_file")

        self.assertEqual(self.expected_diff_text, diff_text)