#!/usr/bin/env python

import sublime
import sublime_plugin

import difflib


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


"""
Fetch sublime version
"""
version = sublime.version()


"""
Helper functions
"""
def selectionToString(view):
    """
    Iterates over a view's current selection and reutrns a aggregated
    string of the same
    """
    return _reduce(lambda acc, r : acc + view.substr(r), view.sel(), "")

def getLinesHelper(s):
    """
    Given a buffer of text, splits it into the appropriate lines while
    maintaining the line break per line
    """
    all_lines = [l for l in s.split("\n")]
    lines = [l + "\n" for l in all_lines]
    return lines

def writeLinesToViewHelper(view, edit, lines, index=0):
    """
    Helper function to walk a list of lines and emit them to the given view
    starting at the `index`. Default value of index is 0
    """
    for line in lines:
        index += view.insert(edit, index, line)


"""
Sublime commands that this plugin implements
"""
class ClipboardDiffCommand(sublime_plugin.TextCommand):
    """
    Fired when the select-diff key is triggered, will grab
    the current selection, and open a new tab with a diff
    """
    def run(self, edit):
        """
        1. Fetch the current selection
        2. Fetch the clipboard
        3. Use difflib to compare them
        4. Output this to a new tab (scratch)
        """
        current_window = self.view.window()
        diff_view = current_window.new_file()
        diff_view.set_scratch(True)
        diff_view.set_name("Clipboard Diff")
        current_window.focus_view(diff_view)

        current_selection = selectionToString(self.view)
        previous_selection = sublime.get_clipboard()

        diff = difflib.unified_diff(
                    getLinesHelper(previous_selection),
                    getLinesHelper(current_selection),
                    "Clipboard", "Selection")

        writeLinesToViewHelper(diff_view, edit, diff, index = 0)