feedparser - Parse Atom and RSS feeds in Python.

| Copyright 2010-2020 Kurt McKee <contactme@kurtmckee.org>
| Copyright 2002-2008 Mark Pilgrim

feedparser is open source. See the LICENSE file for more information.

![PyPI](https://img.shields.io/pypi/v/feedparser.svg?style=flat-square) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/feedparser?style=flat-square)

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

Installation
============

feedparser can be installed by running pip:

..  code-block:: shell

    $ pip install feedparser


Documentation
=============

The feedparser documentation is available on the web at:

    https://pythonhosted.org/feedparser/

It is also included in its source format, ReST, in the ``docs/`` directory.
To build the documentation you'll need the Sphinx package, which is available at:

    https://www.sphinx-doc.org/

You can then build HTML pages using a command similar to:

..  code-block:: shell

    $ sphinx-build -b html docs/ fpdocs

This will produce HTML documentation in the ``fpdocs/`` directory.

Development
===========

Install developement dependencies:

..  code-block:: shell

    $ python -m pip install -U -r requirements.txt

Install pre-commit hooks:

..  code-block:: shell

    $ pre-commit install


Testing
=======

Feedparser has an extensive test suite, powered by tox. To run it, type this:

..  code-block:: shell

    $ python -m venv venv
    $ source venv/bin/activate  # or "venv\bin\activate.bat" on Windows
    (venv) $ pip install tox
    (venv) $ tox

This will spawn an HTTP server that will listen on port 8097. The tests will
fail if that port is in use.
