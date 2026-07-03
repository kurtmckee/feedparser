Project development
-------------------

*   Pass a sorted list of JSON test paths to ``@pytest.mark.parametrize``
    instead of the lazy ``rglob()`` iterator, which pytest 10 will reject.
