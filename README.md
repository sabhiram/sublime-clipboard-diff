# sublime-clipboard-diff
[![Build Status](https://travis-ci.org/sabhiram/sublime-clipboard-diff.svg?branch=master)](https://travis-ci.org/sabhiram/sublime-clipboard-diff)

SublimeText plugin to diff your clipboard against the current selection

![](https://raw.githubusercontent.com/sabhiram/public-images/master/sublime-clipboard-diff/sublime-clipboard-diff.gif)

## Usage:

1. Copy something to the clipboard
2. Select something you want to compare the clipboard to
3. Press:

|    OS   | Key Combination           |
| ------- | ---------------           |
| Linux   | ctrl + alt + D            |
| Mac     | super(⌘) + alt + ctrl + D |
| Windows | ctrl + alt + D            |

## Installation

Currently only the manual install is supported. Hopefully I can add this to package control soon

### Manual Install 

From SublimeText `Packages` folder:
```sh
git clone git@github.com:sabhiram/sublime-clipboard-diff.git clipboard-diff
```

### ... for Contributors

Some folks prefer to clone the git repo right into their SublimeText `Packages` folder. While this is probably ok for most users, I prefer to create a symbolic link to the package so that I can point to the plugin from both flavors of SublimeText (for testing and the like...)

```sh
cd ~/dev
git clone git@github.com:sabhiram/sublime-clipboard-diff.git clipboard-diff
ln -s clipboard-diff ~/Library/Application\ Support/Sublime\ Text\ 3/Packages/clipboard-diff
```

### Package Control Install (Not yet supported...)

If you have [Package Control](https://sublime.wbond.net/installation) installed, then simply naviagte to `Package Control: Install Package` and select the `Clipboard Diff` plugin and you are done!

## Settings & Default Key Mapping

There is only one configurable command for this plugin, and it invokes a diff between your clipboard and the current selection.




## Running Tests & CI

This project, and any pull requests will automatically be run against Travis CI. For local development, the test assume the following are installed and configured:

Hopefully you have [Sublime Text](http://www.sublimetext.com/3) installed

Next make sure you have [Package Control](https://sublime.wbond.net/installation) installed as well (and you really should, its awesome!)

Via the SublimeText Package Control, install the `UnitTesting` package. You can do this by hitting `ctrl + shift + p`, then select `Package Control: Install Package`. Once the menu loads, choose the `UnitTesting` package.

To run the tests: `ctrl + shift + p` then select `UnitTesting: Run any project test suite` and type in the name of this package (in my case, and typically `sublime-clipboard-diff` but is basically the name of the folder which you chose to clone the repo into).

## TODO

TODO: Document how we can go about binding a custom key to running tests for a particular package / plugin.

TODO: Figure out how to hook up auto code coverage to this