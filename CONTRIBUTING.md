# Contributing to AME

This version of AME was forked from a fork of the original.
I'm now trying to add some features that an author has specifically asked for but would welcome
any contributions to the project.

This document provides some development specific notes.

## Development - Linux

Start by installing the needed OS and python dependencies.
For the OS it will depend on what you use: I use Fedora so noted that here.
Python dependencies are managed with [uv](https://docs.astral.sh/uv/) instead.

```shell
sudo dnf install gtk3-devel python3-devel webkit2gtk4.1-devel uv
uv sync
```

Run the editor with `uv run python AME.py`.

## Development - Windows

Setting up Windows for development was easier then expected:

1. Install Python using the [Python Install Manager](https://www.python.org/downloads/).
2. Install `git` with `winget install --id Git.Git -e --source winget`.
3. Install `uv`:
   1. Download the install script with your browser: <https://astral.sh/uv/install.ps1>.
   2. Review the script to ensure it is safe to execute (it is at the time of writing but this may change).
   3. Execute the install script: `powershell -ExecutionPolicy ByPass -c Downloads\install.ps1`.

Install project dependencies with `uv sync`.

Run the editor with `uv run python AME.py`.

## Release

Releasing new versions is easy thanks to `pyinstaller`.
The process has to happen on the OS you are releasing for (so on Windows for Windows releases).

1. Ensure you have the latest changes: `git pull origin`.
2. Run pyinstaller: `uv run pyinstaller -F --onefile --noconsole AME.py`.
3. Copy the `README.md`, `LICENSE` and the example config file into the `dist/` directory.
4. If you want to include the autocomplete configuration import tool also run: `uv run pyinstaller -F --onefile tools/conf-import.py`.
5. Zip up all the files in the `dist/` directory.
6. Upload the zip file to GitHub as a new release.
