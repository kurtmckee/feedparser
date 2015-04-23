feedparser - Parse Atom and RSS feeds in Python.

| Copyright 2010-2015 Kurt McKee <contactme@kurtmckee.org>
| Copyright 2002-2008 Mark Pilgrim

feedparser is open source. See the LICENSE file for more information.


Installation
============

Feedparser can be installed using distutils or setuptools by running::

    $ python setup.py install

If you're using Python 3, feedparser will automatically be updated by the 2to3
tool; installation should be seamless across Python 2 and Python 3.

Note: sgmllib3k is a Python 3 dependency. It will be installed automatically.


Documentation
=============

The feedparser documentation is available on the web at:

    https://pythonhosted.org/feedparser/

It is also included in its source format, ReST, in the docs/ directory. To
build the documentation you'll need the Sphinx package, which is available at:

    http://sphinx.pocoo.org/

You can then build HTML pages using a command similar to::

    $ sphinx-build -b html docs/ fpdocs

This will produce HTML documentation in the fpdocs/ directory.


Testing
=======

Feedparser has an extensive test suite that has been growing for a decade. If
you'd like to run the tests yourself, you can run the following command::

    $ python feedparsertest.py

This will spawn an HTTP server that will listen on port 8097. The tests will
fail if that port is in use.
