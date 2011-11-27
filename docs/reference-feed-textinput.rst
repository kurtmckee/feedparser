:py:attr:`feed.textinput`
=========================

A text input form.  No one actually uses this.  Why are you?


.. _reference.feed.textinput.title:

:py:attr:`feed.textinput.title`
-------------------------------

The title of the text input form, which would go in the value attribute of the
form's submit button.


.. _reference.feed.textinput.link:

:py:attr:`feed.textinput.link`
------------------------------

The link of the script which processes the text input form, which would go in
the action attirbute of the form.

If this is a relative :abbr:`URI (Uniform Resource Identifier)`, it is
:ref:`resolved according to a set of rules <advanced.base>`.


.. _reference.feed.textinput.name:

:py:attr:`feed.textinput.name`
------------------------------

The name of the text input box in the form, which would go in the name
attribute of the form's input box.


.. _reference.feed.textinput.description:

:py:attr:`feed.textinput.description`
-------------------------------------

A short description of the text input form, which would go in the label element
of the form.


.. rubric:: Annotated example

This is a text input in a feed:
::


    <textInput>
    <title>Go!</title>
    <link>http://example.org/search</link>
    <name>keyword</name>
    <description>Search this site:</description>
    </textInput>


This is how it could be rendered in :abbr:`HTML (HyperText Markup Language)`:
::


    <form method="get" action="http://example.org/search">
    <label for="keyword">Search this site:</label>
    <input type="text" id="keyword" name="keyword" value="">
    <input type="submit" value="Go!">
    </form>


.. rubric:: Comes from

* /rdf:RDF/rdf:textinput
* /rss/channel/textInput
* /rss/channel/textinput
