Security
--------

*   Prevent catastrophic regex backtracking when reading the encoding
    from the XML declaration. A feed served as a single line that contains
    many ``encoding="..."`` attributes, such as KaTeX's MathML output,
    could make parsing hang indefinitely.
