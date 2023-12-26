Fixed
-----

*   If the metadata of a feed explicitly indicates that the encoding is UTF-8,
try decode it with ``errors="replace"`` when decoding fails. This prevents
feeds from being decoded with wrong encodings when they are mostly UTF-8 but
contain a few invalid bytes.
