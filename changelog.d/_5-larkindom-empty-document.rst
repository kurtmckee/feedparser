Fixed
-----

*   Set ``bozo`` and ``bozo_exception`` (to a new ``EmptyDocument`` error)
    when parsing empty input, instead of silently returning a result that
    looks like a valid, empty feed. (#461)
