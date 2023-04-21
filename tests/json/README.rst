JSON feed tests
===============

The files in this directory exercise the JSON feed parser.


``*.json``
----------

Files in this directory contain JSON objects.
They will contain a ``__tests`` key with a list of expected conditions.
Each condition will be evaluated after parsing the feed.

For example:

..  code-block:: json

    {
      "__tests": [
        "version == 'json11'"
      ],
      "version": "https://jsonfeed.org/version/1.1"
    }

Files in this directory are automatically found, parsed, and tested.

When writing tests please consider the following:

*   Test incorrect value types that do not match the JSON feed requirements.
    For example, test null values where a string is required.

*   Test incorrect value types that are not hashable in Python.
    For example, test lists where a string is required.

*   Test incorrect value types that are also iterable in Python.
    For example, test a JSON object where a list is required.

*   Write ``eval()`` strings using Unicode escape sequences as needed.
    This forces the test and JSON feed content to agree.
    For example,

    ..  code-block:: json

        {
          "__tests": ["title == '\ud83d\ude0e'"],
          "title": "😎"
        }
