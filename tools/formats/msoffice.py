"""
Read Microsoft Office autocorrect files to allow importing into AME autocorrect format.

As the MS Office autocorrect format is proprietary and undocumented this is a best effort reader
created by eyeballing a single configuration file.

This solution expects a fixed "header" of some kind to be of known length.
I then guessed what the mapping pattern is (there is a doc in here about it) but no way to confirm.

Finally this was build and tested using one file that was sent to me.
I have no way of knowing if this would even work with other files.
"""
from pathlib import Path
import logging


# Unknown bytes found at the start of the file.
# What do they mean? Can they change? Who knows, but maybe we don't care.
UNKNOWN_HEADER_BYTES: [int] = [
    0x04, 0x01, 0x96, 0x00, 0xA1, 0x78, 0xBF, 0x0E, 0xE4, 0xFC,
    0x09, 0x00, 0xC0, 0x43, 0x00, 0x00, 0x44, 0x00,
]
LIKELY_END_BYTES: [int] = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00]


def read_msoffice_data(location: str) -> dict[str, str]:
    """Read a replacement map from a Microsoft Word data file.

    Returns
    -------
        A map from typed text to its configured replacement.
    """
    # Read the whole file in memory for easier scanning.
    data = bytes()
    location = Path(location)
    with location.open("rb") as fd:
        data = fd.read()

    # Check there is enough data for it to make sense.
    offset = len(UNKNOWN_HEADER_BYTES)
    size = len(data)
    if offset > size:
        logging.error("MS Office file shorter than expected header, cannot process it")
        return {}

    # Iterate over data file to read replacements.
    corrections = {}
    while offset + 2 < size:
        # Check source marker.
        marker = (data[offset], data[offset + 1])
        if marker != (0x00, 0x00):
            logging.error(f"Expected replacement source marker not found at {offset}")
            return corrections
        offset += 2

        # Read source string.
        source_len = data[offset] * 2
        source_payload = data[offset + 2: offset + 2 + source_len]
        source_str = source_payload.decode('utf-16le')
        offset += 2 + source_len

        # Check target marker.
        marker = (data[offset], data[offset + 1])
        if marker != (0x00, 0x00):
            logging.error(f"Expected replacement target marker not found at {offset}")
            return corrections
        offset += 2

        # Read target string.
        target_len = data[offset] * 2
        target_payload = data[offset + 2: offset + 2 + target_len]
        target_str = target_payload.decode('utf-16le')
        offset += 2 + target_len

        # Sometimes we get multiple `0000` bytes before the next replacement entry.
        # This means we have the "fun" task to figure them out and skip them.
        # But keep the last one as the marker for the new replacement pair.
        while _is_null_unit(data, offset) and _is_null_unit(data, offset + 2):
            offset += 2

        # Save to dictionary.
        corrections[source_str] = target_str
    return corrections


def _is_null_unit(data: bytes, offset: int) -> bool:
    """Check if the current UTF16 sequence is a null."""
    unit = data[offset:offset + 2]
    return unit == b'\x00\x00'
