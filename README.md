# sublime-clipboard-diff
[![Build Status](https://travis-ci.org/sabhiram/sublime-clipboard-diff.svg?branch=master)](https://travis-ci.org/sabhiram/sublime-clipboard-diff)

SublimeText plugin to diff your clipboard against the current selection

![](https://raw.githubusercontent.com/sabhiram/public-images/master/sublime-clipboard-diff/sublime-clipboard-diff.gif)

[Clipboard Diff](https://packagecontrol.io/packages/Clipboard%20Diff) on Package Control

## Usage:

1. Copy something to the clipboard
2. Select something you want to compare the clipboard to
3. Press:

|    OS   | Key Combination           |
| ------- | ---------------           |
| Linux   | ctrl + alt + D            |
| Mac     | super(⌘) + alt + ctrl + D |
| Windows | ctrl + alt + D            |

You can also run it from the Command Palette (`ctrl + shift + P`) followed by `"Clipboard Diff"`. The same command is also available from the "Context Menu" (right clicking on a text area).

## Installation

The easiest way to install `Clipboard Diff` is to install it from Package Control

### Package Control Install

If you have [Package Control](https://sublime.wbond.net/installation) installed, then simply naviagte to `Package Control: Install Package` and select the `Clipboard Diff` plugin and you are done!

### Manual Install

From SublimeText `Packages` folder:
```sh
git clone git@github.com:sabhiram/sublime-clipboard-diff.git sublime-clipboard-diff
```

## Settings & Default Key Mapping

Here is a list of settings exposed by Clipboard Diff:

```javascript

    // Setting the `diff_type` will allow the user to toggle the type
    // of diff used in Clipboard Diff
    //
    // Here is a list of supported types as of now:
    //
    // 1. [Default] unified - Uses difflib.unified_diff(...)
    // 2.           context - Uses difflib.context_diff(...)
    "diff_type": "unified",

    // Setting the `clipboard_file_name` will allow the user to change the
    // file name which shows up when the diff is run for the Clipboard
    // contents.
    "clipboard_file_name": "Clipboard",

    // Setting the `selection_file_name` will allow the user to change the
    // file name which shows up when the diff is run for the Selection
    // contents.
    "selection_file_name": "Selection"
```

To override any of these settings, simply create a file called `clipboard_diff.sublime-settings` in the `Packages\User` folder. Here is a sample:

```sh
more ~/Library/Application\ Support/Sublime\ Text\ 3/Packages/User/clipboard_diff.sublime-settings
{
    "diff_type": "context",
    "clipboard_file_name": "Clipboard contents",
    "selection_file_name": "Selected stuff..."
}
```

The above User specific setting file overrides the names which will be displayed when a diff is computed. It also demonstrates how we can change the `diff_type` to a `difflib.context_diff` as opposed to the default `difflib.unified_diff`

## Developers

Appreciate the help! Here is stuff you should probably know:

### Install for both Sublime Text 2 and 3:

Some folks prefer to clone the git repo right into their SublimeText `Packages` folder. While this is probably ok for most users, I prefer to create a symbolic link to the package so that I can point to the plugin from both flavors of SublimeText (for testing and the like...)

```sh
cd ~/dev
git clone git@github.com:sabhiram/sublime-clipboard-diff.git sublime-clipboard-diff
ln -s sublime-clipboard-diff ~/Library/Application\ Support/Sublime\ Text\ 2/Packages/sublime-clipboard-diff
ln -s sublime-clipboard-diff ~/Library/Application\ Support/Sublime\ Text\ 3/Packages/sublime-clipboard-diff
```

### Running Tests & CI

This project, and any pull requests will automatically be run against Travis CI. For local development, the tests assume that the following are installed and configured:

Hopefully you have [Sublime Text](http://www.sublimetext.com/3) installed

Next make sure you have [Package Control](https://sublime.wbond.net/installation) installed as well (and you really should, it's awesome!)

Via the SublimeText Package Control, install the `UnitTesting` package. You can do this by hitting `ctrl + shift + p`, then select `Package Control: Install Package`. Once the menu loads, choose the `UnitTesting` package.

To run the tests: `ctrl + shift + p` then select `UnitTesting: Run any project test suite` and type in the name of this package (in my case, and typically `sublime-clipboard-diff` but is basically the name of the folder which you chose to clone the repo into).

### Sublime Text API Reference

[Sublime Text 2 API](https://www.sublimetext.com/docs/2/api_reference.html)

[Sublime Text 3 API](https://www.sublimetext.com/docs/3/api_reference.html)

## Versions Released

#### 1.2.0 - Future Release

1. Add external diff tool
2. ... What would **you** like to see?

#### 1.1.4 - Current Release

1. Display appropriate message when the selection and clipboard match

#### 1.1.3

1. Adds Context menu item for "Clipboard Diff"
2. Adds Command Palette entry for "Clipboard Diff"

#### 1.1.2

1. Minor update: add package control messages
2. Prettify the plugin settings in the readme

#### 1.1.1

1. Minor bugfix with diff output view

#### 1.1.0

1. Adds syntax highlighting to diff output view
2. Exposes settings to change `diff_type` and source / destination file names
3. Small bugfixes in helper functions which were never tested
4. More tests to validate the above

#### 1.0.0 - Initial Release

1. Implements basic diff feature
2. Adds simple tests for plugin functionality
3. Ready for package control deployment
