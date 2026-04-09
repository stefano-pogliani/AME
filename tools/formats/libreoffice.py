"""Read LibreOffice autocorrect files to allow importing into AME autocorrect format."""
from xml.etree import ElementTree
from zipfile import ZipFile


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
