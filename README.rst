feedparser - Parse Atom and RSS feeds in Python.

| Copyright 2010-2022 Kurt McKee <contactme@kurtmckee.org>
| Copyright 2002-2008 Mark Pilgrim

feedparser is open source. See the LICENSE file for more information.


Installation
============

feedparser can be installed by running pip:

..  code-block:: shell

    $ pip install feedparser


Documentation
=============

The feedparser documentation is available on the web at:

    https://feedparser.readthedocs.io/en/latest/

It is also included in its source format, ReST, in the ``docs/`` directory.
To build the documentation you'll need the Sphinx package, which is available at:

    https://www.sphinx-doc.org/

You can then build HTML pages using a command similar to:

..  code-block:: shell

    $ sphinx-build -b html docs/ fpdocs

This will produce HTML documentation in the ``fpdocs/`` directory.


Testing
=======

Feedparser has an extensive test suite, powered by tox. To run it, type this:

..  code-block:: shell

    $ python -m venv venv
    $ source venv/bin/activate  # or "venv\bin\activate.ps1" on Windows
    (venv) $ pip install -r requirements-dev.txt
    (venv) $ tox

This will spawn an HTTP server that will listen on port 8097. The tests will
fail if that port is in use.
