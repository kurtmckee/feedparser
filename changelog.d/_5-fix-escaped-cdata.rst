Fixed
-----

*   Extract the contents of an escaped CDATA section instead of dropping
    them. Previously, a value like ``&lt;![CDATA[text]]&gt;`` (a CDATA
    section that a feed has XML-escaped) was parsed as an empty string
    because the HTML processor discarded the marked section. (#440)
