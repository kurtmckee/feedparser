Security
--------

*   Fix quadratic-time backtracking in the HTML sanitizer's CSS style check.
    A hostile feed with a very long ``style`` attribute made of word characters
    could make parsing consume seconds of CPU. Declarations are now validated
    individually instead of with a global substitution. (#610)