#!/usr/bin/env python
import sys, os, time
import difflib
import unittest

import sublime


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


    """
    Helper functions
    """
    def getDiffExpectedResult(self, diff_fn, str_a, str_b, file_a, file_b):
        result = diff_fn(
                    clipboard_diff.getLinesHelper(str_a),
                    clipboard_diff.getLinesHelper(str_b),
                    file_a, file_b)
        return _reduce(lambda acc, x: acc + x, result, "")

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

        self.settings = sublime.load_settings("clipboard_diff.sublime-settings")


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
        """
        Tests ST2 only stuff
        """
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

    else:
        """
        > ST 2 Tests
        """
        def test_clipboard_diff_view_syntax(self):
            """
            Validates that the newly opened tab is of the `Diff` syntax
            """
            self.runSimpleViewCommand("clipboard_diff")

            diff_view = sublime.active_window().active_view()
            diff_syntax = diff_view.settings().get('syntax')
            diff_view.window().run_command("close_file")

            self.assertEqual("Packages/Diff/Diff.tmLanguage", diff_syntax)


    """
    Plugin Tests:
    """
    def test_clipboard_unified_diff(self):
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

        expected_diff_text = self.getDiffExpectedResult(difflib.unified_diff,
                                    self.test_lines_0, self.test_lines_1,
                                    "Clipboard", "Selection")
        self.assertEqual(expected_diff_text, diff_text)

    def test_clipboard_unified_diff_same_selection(self):
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

    def test_clipboard_context_diff(self):
        """
        Validates that we can change the diff type to context
        diff (from difflib)
        """
        self.insertTextToTestView(self.test_lines_0)
        self.runSimpleViewCommand("select_all")
        self.runSimpleViewCommand("cut")
        self.insertTextToTestView(self.test_lines_1)
        self.runSimpleViewCommand("select_all")

        old_type = self.settings.get("diff_type")
        self.settings.set("diff_type", "context")
        self.runSimpleViewCommand("clipboard_diff")
        self.settings.set("diff_type", old_type)

        diff_view = sublime.active_window().active_view()
        diff_text = diff_view.substr(sublime.Region(0, diff_view.size()))
        diff_view.window().run_command("close_file")

        expected_diff_text = self.getDiffExpectedResult(difflib.context_diff,
                                    self.test_lines_0, self.test_lines_1,
                                    "Clipboard", "Selection")
        self.assertEqual(expected_diff_text, diff_text)

    def test_clipboard_setting_file_names(self):
        """
        Validates that clipboard_file_name and selection_file_name
        can be set to success
        """
        self.insertTextToTestView(self.test_lines_0)
        self.runSimpleViewCommand("select_all")
        self.runSimpleViewCommand("cut")
        self.insertTextToTestView(self.test_lines_1)
        self.runSimpleViewCommand("select_all")

        old_clipboard_file_name = self.settings.get("clipboard_file_name")
        old_selection_file_name = self.settings.get("selection_file_name")
        self.settings.set("clipboard_file_name", "CLIPBOARD IS FUN")
        self.settings.set("selection_file_name", "SELECTION IS BETTER")
        self.runSimpleViewCommand("clipboard_diff")
        self.settings.set("clipboard_file_name", old_clipboard_file_name)
        self.settings.set("selection_file_name", old_selection_file_name)

        diff_view = sublime.active_window().active_view()
        diff_text = diff_view.substr(sublime.Region(0, diff_view.size()))
        diff_view.window().run_command("close_file")


        expected_diff_text = self.getDiffExpectedResult(difflib.unified_diff,
                                    self.test_lines_0, self.test_lines_1,
                                    "CLIPBOARD IS FUN", "SELECTION IS BETTER")
        self.assertEqual(expected_diff_text, diff_text)


