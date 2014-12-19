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
Define the current buffer of lines we wish to compare against.

Note that this will get overwritten any time we hit a copy or cut
command from the user
"""
class StoredBuffer(object):
    """
    Constructor takes string construction args and forwards it
    to the internal buffer

    Reset will re-assign the buffer

    Get will fetch the current one
    """
    def __init__(self, *args, **kwargs):
        self.buffer = str(*args, **kwargs)

    def reset_buffer(self, s):
        self.buffer = s

    def get_buffer(self):
        return self.buffer


storedBuffer = StoredBuffer("")


"""
Helper functions
"""
def selectionToString(view):
    """
    Iterates over a view's current selection and reutrns a aggregated
    string of the same
    """
    return _reduce(lambda acc, r : acc + view.substr(r), view.sel(), "")

def getLinesHelper(line):
    """
    Given a buffer of text, splits it into the appropriate lines while
    maintaining the line break per line
    """
    all_lines = [l for l in line.split("\n")]
    lines = [l + "\n" for l in all_lines]
    return lines

def writeLinesToViewHelper(view, edit, lines, index=0):
    """
    Helper function to walk a list of lines and emit them to the given view
    starting at the `index`. Default value of index is 0
    """
    for line in lines:
        index += view.insert(edit, index, line)

def getCurrentBuffer():
    """
    Test helper function which returns the current buffer of stored text
    """
    return storedBuffer.get_buffer()


"""
Sublime commands that this plugin implements
"""
class ClipboardDiffCopyCommand(sublime_plugin.TextCommand):
    """
    Fired when the user issues a `copy` so we can remember
    the buffer so we can compare it with whatever is the 
    selection buffer
    """
    def run(self, edit):
        """
        1. Fetch the current selection
        2. Store it to the `storedBuffer`
        3. Run the real copy command...
        """
        text = selectionToString(self.view)
        storedBuffer.reset_buffer(text)
        self.view.run_command("copy")


class ClipboardDiffCutCommand(sublime_plugin.TextCommand):
    """
    Fired when the user issues a `cut` so we can remember
    the buffer so we can compare it with whatever is the
    selection buffer
    """
    def run(self, edit):
        """
        1. Fetch the current selection
        2. Store it to the `storedBuffer`
        3. Run the real cut command...
        """
        text = selectionToString(self.view)
        storedBuffer.reset_buffer(text)
        self.view.run_command("cut")


class ClipboardDiffCommand(sublime_plugin.TextCommand):
    """
    Fired when the select-diff key is triggered, will grab
    the current selection, and open a new tab with a diff
    """
    def run(self, edit):
        """
        1. Fetch the current selection
        2. Fetch the `storedBuffer`
        3. Use difflib to compare them
        4. Output this to a new tab (scratch)
        """
        current_window = self.view.window()
        diff_view = current_window.new_file()
        diff_view.set_scratch(True)
        diff_view.set_name("Select Diff")
        current_window.focus_view(diff_view)

        current_selection = selectionToString(self.view)
        previous_selection = storedBuffer.get_buffer()
        diff = difflib.unified_diff(
                    getLinesHelper(previous_selection),
                    getLinesHelper(current_selection),
                    "Clipboard", "Selection")

        writeLinesToViewHelper(diff_view, edit, diff, index = 0)