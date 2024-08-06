``requirements/``
#################

This directory contains the files that manage dependencies for the project.

At the time of writing, Poetry supports discrete dependency groups
but always resolves dependencies coherently across all groups.
However, in some cases, dependencies do not need to be coherently resolved;
for example, mypy's dependencies do not need to be resolved
together with Sphinx's dependencies.

Each subdirectory in this directory contains a ``pyproject.toml`` file
with purpose-specific dependencies listed.


How it's used
=============

Tox is configured to use the exported ``requirements.txt`` files as needed.
In addition, Read the Docs is configured to use ``docs/requirements.txt``.
This helps ensure reproducible testing, linting, and documentation builds.


How it's updated
================

A tox label, ``update``, ensures that dependencies can be easily updated,
and that ``requirements.txt`` files are consistently re-exported.

This can be invoked by running:

..  code-block::

    tox run -m update


How to add dependencies
=======================

New dependencies can be added to a given subdirectory's ``pyproject.toml``
by either manually modifying the file, or by running a command like:

..  code-block::

    poetry add --lock --directory "requirements/$DIR" $DEPENDENCY_NAME

Either way, the dependencies must be re-exported:

..  code-block::

    tox run -m update
