# AME: Accessible Markdown Editor for Screen Readers

It is a simple accessible markdown editor designed for screen readers.

## Shortcuts

On Mac, press command instead of control.

* Open: Ctrl+O
* New: Ctrl+N
* Export to HTML: Ctrl+E
* Copy HTML to Clipboard: Ctrl+Shift+C
* View Markdown: Ctrl+1
* View HTML: Ctrl+2

## Jonathan's additions

Import and export using [pandoc](https://pandoc.org/) is achieved using pypandoc, the Python wrapper to pandoc. This requires an installation of pandoc.

Import is sorted. The user does not need to specify the file type, but Pandoc only imports a small range of files. Hot key is CTRL+SHIFT+O

Export to HTML via pandoc is available. This should allow maths to be included. N.B. the math will not be rendered correctly using just Python alone, or in the AME HTML pane, which is really just a preview pane if any equations are included.

Protection against the user not having Pandoc visible is in need of testing. It needs to be run on a machine that does not have pandoc installed, both for import and export.

Created an installer for the Windows version. This puts a date-based version number in a text file within the installation folder.

### Other updates and alterations to the original AME

Hints and corrections offered using pylint and blacken tools have been incorporated. Pylint still throws warnings about a few things but they of low significance. Most relate to pylint not knowing about the wx use of `(self, e)` style in function definitions.

Small alterations:

1. added a small help note with hotkey `f1`
2. added switch view menu item in the View menu (hotkey is `f4`) and reordered the original items.
3. did a bit of re-factoring on reused code snippets.

## Stefano's additions

* Introduce an autocorrect system into the editor.
* Tweak UI focus on Windows so the text area is selected at start.
* [Development] Add a `pyproject.toml` file to manage dependencies.
* [Development] Add a `CONTRIBUTING.md` file to move development docs from this readme.

## Autocorrect

Autocorrect can replace configured words with longer words or full sentences to speed up typing.

Autocorrect triggers when a word separating character is typed. Replacement is considered only if a full word matches to ensure that replacement do not happen mid-word.

The list of characters that count as word separator is configurable and defaults the combination of
Python's [`string.punctuation`](https://docs.python.org/3/library/string.html#string.punctuation)
and [`string.whitespace`](https://docs.python.org/3/library/string.html#string.whitespace).

AME now looks for autocorrect configuration files in two places:

* A user wide configuration file, loaded every time the editor is opened.
  * On Linux: `$HOME/.local/share/AME/ame.autocorrect.toml`.
  * On MacOS: `$HOME/Library/Application Support/AME/ame.autocorrect.toml`.
  * On Windows: `%AppData%/AME/ame.autocorrect.toml`.

* A project local configuration file, loaded when a file is opened or a new file is first saved.

This local configuration file is called `ame.autocorrect.toml` and located in the same directory as the file being opened.

For example,

If you want an autocorrect string to apply to certain works,

1. Put the 'ame.autocorrect.toml' file in the same directory as your manuscript/project.
2. Customize that particular 'ame.autocorrect.toml' file.
3. When you open your manuscript using the file, open, dialog box, in that directory or save a file for the first time in that directory, the 'ame.autocorrect.toml' file in that directory will apply to that project.

The project local file takes precedence over the user wide configuration file.

This allows users to set up some always useful rules and enrich them or replace them with rules specific to the file (or files) being edited right now.

As an example, here is a configuration file:

```toml
# Characters to mark the beginning/ending of a word.
# Mainly intended as a way to self-fix bugs, the default should work in most cases.
[terminals]
# Characters to add to the current set of terminals.
add = []
# Characters to remove from the current set of terminals.
remove = []
# Full list of characters that indicate the beginning/ending of a word.
set = [' ', '\r', '\n', '.']

# Correction rules mapping typed sequences (on the left) to their extended text (on the right).
[corrections]
from = "to"
ie = "for example"
etc = "etcetera"
```

### Import Office Autocorrect Files

The project comes with a small command line tool to convert LibreOffice autocorrect data files into an autocorrect configuration file that AME can load.
Microsoft Office autocorrect data files are processed but with no guarantee it will work as the format is undocumented.

To import LibreOffice or MS Office autocomplete files you call the `conf-import` to with the file names after it.
ACL files are assumed to be MS Office, DAT files are assumed to be LibreOffice.

Multiple files can be specified, in which case their rules are merged into one set.
If two files have the same rule the merged configuration will use the rule from the latest file, which means files order is important if merging files that correct the same input to different values.

For example if you run `conf-import MSO1033.acl acor_en-US.dat` you will get a `new-ame.autocorrect.toml` file with all the replacement rules of both input files.
The file to save the new configuration in can be set with the `--ame-target` option and uses a `new-` prefix by default so existing configurations are not replaced automatically.
