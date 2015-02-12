#!/usr/bin/env python

import sublime
import sublime_plugin

import os
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
    return index

def validateSettings():
    """
    Helper function which loads our settings file and ensures that it does not
    contain bad values:

        1. The clipboard_file_name should be set
        2. The selection_file_name should be set
        3. The diff_type should be set, and either be unified or context
    """
    settings = sublime.load_settings("clipboard_diff.sublime-settings")
    needs_flush = False

    if not settings.has("clipboard_file_name"):
        settings.set("clipboard_file_name", "Clipboard")
        needs_flush = True

    if not settings.has("selection_file_name"):
        settings.set("selection_file_name", "Selection")
        needs_flush = True

    if not settings.has("diff_type"):
        settings.set("diff_type", "unified")
        needs_flush = True
    elif settings.get("diff_type") not in ["unified", "context"]:
        settings.set("diff_type", "unified")
        needs_flush = True

    if needs_flush:
        print("Settings updated - needs flush...")
        sublime.save_settings("clipboard_diff.sublime-settings")

"""
Sublime commands that this plugin implements
"""
class ClipboardDiffCommand(sublime_plugin.TextCommand):
    """
    Fired when the "clipboard-diff" command is triggered, will
    grab the current selection, and open a new tab with a diff
    """
    def run(self, edit):
        """
        0. Validate any settings that might be set badly
        1. Add a diff view to the window (scratch)
        2. Set its properties (name / syntax etc)
        3. Fetch the current selection and the clipboard
        4. Use difflib to compare them
        5. Write the diff to the view
        """
        validateSettings()

        current_window = self.view.window()
        diff_view = current_window.new_file()
        diff_view.set_scratch(True)

        diff_view.set_name("Clipboard Diff")
        diff_view.set_syntax_file("Packages/Diff/Diff.tmLanguage")

        current_selection = selectionToString(self.view)
        previous_selection = sublime.get_clipboard()

        settings = sublime.load_settings("clipboard_diff.sublime-settings")
        diff_type = settings.get("diff_type")

        diff_function = difflib.unified_diff
        if diff_type == "context":
            diff_function = difflib.context_diff

        diff = diff_function(getLinesHelper(previous_selection),
                             getLinesHelper(current_selection),
                             settings.get("clipboard_file_name"),
                             settings.get("selection_file_name"))

        current_window.focus_view(diff_view)
        writeLinesToViewHelper(diff_view, edit, diff, index = 0)


class ApplyDiffToSelectionCommand(sublime_plugin.TextCommand):
    """
    Fired when the "apply-diff" command is triggered, will grab
    the current selection, and apply a diff to it (assuming that)
    a diff hunk has been copied
    """
    def run(self, edit):
        """
        0. Validate any settings that might be set badly
        1. Grab the selection
        2. Apply diff from clipboard to the selection
        3. Replace selection if it is applicable to the hunk
        """
        validateSettings()
        print("Apply diff to selection called")

        source_text = selectionToString(self.view)
        diff_hunk   = sublime.get_clipboard()

        print("Source:")
        print(source_text)

        print("\nHunk:")
        print(diff_hunk)
