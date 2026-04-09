"""
A standalone python tool to convert autocorrect configuration files for Office suites
into `ame.autocorrect.toml` configurations.
"""
from argparse import ArgumentParser
from collections import OrderedDict
from pathlib import Path

import tomli_w

from formats.libreoffice import read_libreoffice_data
from formats.msoffice import read_msoffice_data


# Map config file extension to a supported Office program.
FORMATS = {
    "acl": read_msoffice_data,
    "dat": read_libreoffice_data,
}


def parser_factory() -> ArgumentParser:
    """Configure CLI parser for this helper tool."""
    parser = ArgumentParser(
        description="Convert LibreOffice or MS Office configs into an AME autocorrect config",
    )
    parser.add_argument(
        "FILE",
        nargs="+",
        help="LibreOffice or MS Office autocorrect config to convert",
    )
    parser.add_argument(
        "--ame-target",
        default="new-ame.autocorrect.toml",
        help="File to save the generated AME autocorrect config to",
    )
    return parser


def save_ame_data(replacements: dict[str, str], location: str) -> None:
    """Save the loaded replacements as an AME autocorrect TOML file."""
    data = {"corrections": replacements}
    with Path(location).open(mode="wb") as fd:
        tomli_w.dump(data, fd)


def main() -> None:
    """Run the conversion tool."""
    parser = parser_factory()
    args = parser.parse_args()

    replacements = {}
    for source in args.FILE:
        ext = source.split(".")[-1]
        read_fn = FORMATS.get(ext)
        if read_fn is None:
            print(f"Unable to read data from {ext} files, ignoring")
            continue

        data = read_fn(source)
        replacements.update(data)

    replacements = dict(sorted(replacements.items()))
    save_ame_data(replacements, args.ame_target)
    print("Conversion process complete")


if __name__ == "__main__":
    main()
