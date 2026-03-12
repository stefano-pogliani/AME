"""
A standalone python tool to convert LibreOffice autocorrect `acor_$LANG-$GEO.dat` files
into `ame.autocorrect.toml` files.
"""
from argparse import ArgumentParser
from pathlib import Path
from xml.etree import ElementTree
from zipfile import ZipFile

import tomli_w


def parser_factory() -> ArgumentParser:
    """Configure CLI parser for this helper tool."""
    parser = ArgumentParser(
        description="Convert LibreOffice acor_*.dat files into ame.autocorrect.toml files",
    )
    parser.add_argument("LO_FILE", help="LibreOffice autocorrect file to convert")
    parser.add_argument(
        "AME_FILE",
        nargs="?",
        default="from-lo-ame.autocorrect.toml",
        help="File to save the generated AME autocorrect config file",
    )
    return parser


def read_libreoffice_data(location: str) -> dict[str, str]:
    """Read a replacement map from a LibreOffice data file.

    Returns
    -------
        A map from typed text to its configured replacement.
    """
    # Read the XML out of the ZIP file.
    archive = ZipFile(location, mode="r")
    doc_file = archive.open("DocumentList.xml", mode="r")
    doc_xml = ElementTree.fromstring(doc_file.read())

    # Grab corrections out of XML
    corrections = {}
    for entry in doc_xml:
        source = entry.attrib.get("{http://openoffice.org/2001/block-list}abbreviated-name")
        replacement = entry.attrib.get("{http://openoffice.org/2001/block-list}name")
        corrections[source] = replacement
    return corrections


def save_ame_data(replacements: dict[str, str], location: str) -> None:
    """Save the loaded replacements as an AME autocorrect TOML file."""
    data = {"corrections": replacements}
    with Path(location).open(mode="wb") as fd:
        tomli_w.dump(data, fd)


def main() -> None:
    """Run the conversion tool."""
    parser = parser_factory()
    args = parser.parse_args()
    replacements = read_libreoffice_data(args.LO_FILE)
    save_ame_data(replacements, args.AME_FILE)
    print("Conversion process complete")


if __name__ == "__main__":
    main()
