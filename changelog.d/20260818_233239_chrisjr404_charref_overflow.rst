Fixed
-----

*   Stop out-of-range numeric character references like ``&#xFFFFFFFF;``,
    ``&#x110000;``, and ``&#xD800;`` from aborting the loose parser, and
    keep them as literal text instead. (#591)
