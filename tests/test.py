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
        test_window = self.test_view.window()
        test_window.focus_view(self.test_view)
        test_window.run_command("close_file")
            

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

    if version < "3000":
        def test_write_to_view(self):
            """
            Validates writing to a view

            This is limited to < ST3 because the edit object is only
            passed into the TextCommand, and view.begin_edit() does 
            not exist anymore.
            """
            lines = clipboard_diff.getLinesHelper(self.test_lines_0)
            edit = self.test_view.begin_edit()
            clipboard_diff.writeLinesToViewHelper(self.test_view, edit, lines)
            self.test_view.end_edit(edit)

            self.runSimpleViewCommand("select_all")
            current_selection = self.test_view.sel()
            selected_text = clipboard_diff.selectionToString(self.test_view)

            self.assertEqual(self.test_lines_0 + "\n", selected_text)


    """
    Plugin Tests:
    """
    def test_clipboard_diff_view_syntax(self):
        """
        Validates that the newly opened tab is of the `Diff` syntax
        """
        self.runSimpleViewCommand("clipboard_diff")

        diff_view = sublime.active_window().active_view()
        diff_syntax = diff_view.settings().get('syntax')

        self.assertEqual("Packages/Diff/Diff.tmLanguage", diff_syntax)

    def test_clipboard_diff(self):
        """
        Validates the `clipboard_diff` command 
        """
        self.insertTextToTestView(self.test_lines_0)
        self.runSimpleViewCommand("select_all")
        self.runSimpleViewCommand("cut")
        self.insertTextToTestView(self.test_lines_1)
        self.runSimpleViewCommand("select_all")

        self.runSimpleViewCommand("clipboard_diff")
        diff_view = sublime.active_window().active_view()
        diff_text = diff_view.substr(sublime.Region(0, diff_view.size()))
        diff_view.window().run_command("close_file")

        self.assertEqual(self.expected_diff_text, diff_text)

    def test_clipboard_diff_same_selection(self):
        """
        Validates the `clipboard_diff` command when run 
        with the same selection
        """
        self.insertTextToTestView(self.test_lines_0)
        self.runSimpleViewCommand("select_all")
        self.runSimpleViewCommand("copy")

        self.runSimpleViewCommand("clipboard_diff")
        diff_view = sublime.active_window().active_view()
        diff_text = diff_view.substr(sublime.Region(0, diff_view.size()))
        diff_view.window().run_command("close_file")

        self.assertEqual("", diff_text)
