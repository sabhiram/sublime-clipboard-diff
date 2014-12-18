#!/usr/bin/env python

import sublime
import sublime_plugin

class SampleCommand(sublime_plugin.TextCommand):
    """
    Sample Command to play w/ sublime text stuffs
    """

    def run(self, edit):
        new_view = sublime.active_window().new_file()
        new_view.insert(edit, 0, "Hello")


def helper_fn(x):
    """
    Dummy helper function, to help validate that the
    tests can also hit non-sublime_plugin classes
    """
    return x