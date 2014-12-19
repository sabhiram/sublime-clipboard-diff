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
    clipboard_diff = sys.modules["clipboard_diff"]
else:
    clipboard_diff = sys.modules["sublime-clipboard-diff.clipboard_diff"]


"""
Python 2 vs Python 3 - Compatibility:
  * reduce() is functools.reduce
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
                        clipboard_diff.getLinesHelper(test_lines_0),
                        clipboard_diff.getLinesHelper(test_lines_1),
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
        """
        self.test_view = sublime.active_window().new_file()
        self.test_view.set_name("Test View")
        self.test_view.set_scratch(True)

    def tearDown(self):
        """
        Common tearDown() for TestSelectionDiffPlugin
        """
        if self.test_view:
            test_window = self.test_view.window()
            test_window.focus_view(self.test_view)
            test_window.run_command("close_file"),


    """
    Helper Function Tests:
    """
    def test_get_selection_str(self):
        """
        Validate the selectionToString helper
        """
        self.insertTextToTestView(self.test_lines_0)
        self.runSimpleViewCommand("select_all")

        selection_txt = clipboard_diff.selectionToString(self.test_view)

        self.assertEqual(self.test_lines_0, selection_txt)

    def test_line_helper(self):
        """
        Validates the line helper
        """
        lines = clipboard_diff.getLinesHelper(self.test_lines_0)

        self.assertEqual(len(lines), 3)
        self.assertEqual(lines[0], "line 0\n")
        self.assertEqual(lines[1], "line 1\n")
        self.assertEqual(lines[2], "line 2\n")

    def test_write_to_view(self):
        """
        Validates writing to a view
        """
        lines = clipboard_diff.getLinesHelper(self.test_lines_0)
        clipboard_diff.writeLinesToViewHelper(self.test_view, lines)

        self.runSimpleViewCommand("select_all")
        current_selection = self.test_view.sel()
        selected_text = clipboard_diff.selectionToString(self.test_view)

        self.assertEqual(self.test_lines_0, selected_text)

    """
    Plugin Tests:
    """
    def test_copy_selection_to_buffer(self):
        """
        Validates if stuff in the view gets copied correctly when
        a user triggers a `clipboard_diff_copy` command
        """
        self.insertTextToTestView(self.test_lines_0)
        self.runSimpleViewCommand("select_all")
        
        previous_selection = self.test_view.sel()
        self.runSimpleViewCommand("clipboard_diff_copy")
        current_selection = self.test_view.sel()
        
        self.assertEqual(self.test_view.sel(), previous_selection)
        self.assertEqual(self.test_lines_0, clipboard_diff.getCurrentBuffer())
        
    def test_cut_selection_to_buffer(self):
        """
        Validates if stuff in the view gets copied correctly when
        a user triggers a `clipboard_diff_cut` command
        """
        self.insertTextToTestView(self.test_lines_0)
        self.runSimpleViewCommand("select_all")
        
        previous_selection = self.test_view.sel()
        self.runSimpleViewCommand("clipboard_diff_cut")
        current_selection = self.test_view.sel()

        self.assertEqual(1, len(current_selection))
        self.assertEqual("", self.test_view.substr(current_selection[0]))
        self.assertEqual(self.test_lines_0, clipboard_diff.getCurrentBuffer())

    def test_clipboard_diff(self):
        """
        Validates the `clipboard_diff` command 
        """
        self.insertTextToTestView(self.test_lines_0)
        self.runSimpleViewCommand("select_all")
        self.runSimpleViewCommand("clipboard_diff_cut")
        self.insertTextToTestView(self.test_lines_1)
        self.runSimpleViewCommand("select_all")

        self.runSimpleViewCommand("clipboard_diff")
        diff_view = sublime.active_window().active_view()
        diff_text = diff_view.substr(sublime.Region(0, diff_view.size()))
        diff_view.window().run_command("close_file")

        self.assertEqual(self.expected_diff_text, diff_text)