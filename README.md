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
* [Development] Add a `pyproject.toml` file to manage dependencies.

### Autocorrect

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
3. When you open your manuscript in that directory or save a file for the first time in that directory, the 'ame.autocorrect.toml' file in that directory will apply to that project.

The project local file takes precedence over the user wide configuration file.

This allows users to set up some always useful rules and enrich them or replace them with rules specific to the file (or files) being edited right now.

As an example, here is a configuration file:

```toml
# List of characters that represent the beginning/ending of a word.
# Mainly intended as a way to self-fix bugs, the default should work in most cases.
terminals = [' ', '\r', '\n', '.']

# Correction rules mapping typed sequences (on the left) to their extended text (on the right).
[corrections]
from = "to"
ie = "for example"
etc = "etcetera"
```

### Development - Linux

Start by installing the needed OS and python dependencies.
For the OS it will depend on what you use: I use Fedora so noted that here.
Python dependencies are managed with [uv](https://docs.astral.sh/uv/) instead.

```shell
sudo dnf install gtk3-devel python3-devel webkit2gtk4.1-devel uv
uv sync
```

Run the editor with `uv run python AME.py`.

### Development - Windows

Setting up Windows for development was easier then expected:

1. Install Python using the [Python Install Manager](https://www.python.org/downloads/).
2. Install `git` with `winget install --id Git.Git -e --source winget`.
3. Install `uv`:
   1. Download the install script with your browser: <https://astral.sh/uv/install.ps1>.
   2. Review the script to ensure it is safe to execute (it is at the time of writing but this may change).
   3. Execute the install script: `powershell -ExecutionPolicy ByPass -c Downloads\install.ps1`.

Install project dependencies with `uv sync`.

Run the editor with `uv run python AME.py`.

### Release

Releasing new versions is easy thanks to `pyinstaller`.
The process has to happen on the OS you are releasing for (so on Windows for Windows releases).

1. Ensure you have the latest changes: `git pull origin`.
2. Run pyinstaller: `uv run pyinstaller -F --onefile --noconsole AME.py`.
3. Copy the `README.md` and the example config file into the `dist/` directory.
4. Zip up all the files in the `dist/` directory.
5. Upload the zip file to GitHub as a new release.
