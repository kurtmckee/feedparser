Fixed
-----

*   Report three uncaught exceptions on malformed feeds through
    ``bozo_exception`` instead of raising them out of ``parse()``: a
    namespace declaration that expat reports as a longer name tuple, and
    XML declaration encodings that contain a null byte or are not valid
    UTF-8. (#622)
