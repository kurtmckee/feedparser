Security
--------

*   Bound the length of author values passed to the author-email regex.
    The pattern backtracks quadratically, so a hostile feed with a very long
    ``<author>`` or ``dc:creator`` value could make parsing consume seconds of
    CPU. Long values now skip the email match instead.
