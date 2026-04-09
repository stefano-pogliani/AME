# MS Office Autocorrect file format

I've gotten an MS Office autocorrect file from Rob as he would like it to be converted.

Exploring this with a HEX editor (and having an example string from his Libre Office version)
I have so far deduced:

- As expected this is a binary file and UTF-16 encoded.
- It appears to have a header of some kind? Maybe?
  - The first 7 UTF16 units (18 bytes) appear unique. What could they mean?
  - Followed by a `0000 00??` which may indicate the total count of maps (68? sounds low for this).
  - From UTF16 unit 10 onwards we start the mapping pattern.
- The mapping format follows the pattern `\0{source len}{source-utf16}\0{target len}{source-utf16}`.
- The file ends with `\0\0\0` (always?).
- Sometimes there are extra null units (`0000`) before the next pair of strings.
  - Discovered after the first implementation attempt.

Example of reading a unit:

```python
In [9]: unit = bytes([0xA9, 0x0])

In [10]: unit
Out[10]: b'\xa9\x00'

In [11]: unit.decode("UTF16")
Out[11]: '©'
```

Some notes: the bytes need inverting: file has `0x00, 0xA9` but must be decoded swapped.
It is important to note the pattern lengths do not appear inverted.

Python can help reading the big endian UTF16.

```python
In [21]: unit = bytes([0x00, 0xA9])

In [22]: unit.decode("utf-16le")
Out[22]: '꤀'

In [23]: unit.decode("utf-16be")
Out[23]: '©'
```
