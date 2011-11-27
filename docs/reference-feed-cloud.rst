:py:attr:`feed.cloud`
=====================

No one really knows what a cloud is.  It is vaguely documented in `:abbr:`SOAP
(Simple Object Access Protocol)` meets :abbr:`RSS (Rich Site Summary)`
<http://www.thetwowayweb.com/soapmeetsrss>`_.


.. _reference.feed.cloud.domain:

:py:attr:`feed.cloud.domain`
----------------------------

The domain of the cloud.  Should be just the domain name, not including the
http:// protocol.  All clouds are presumed to operate over :abbr:`HTTP
(Hypertext Transfer Protocol)`.  The cloud specification does not support
secure clouds over :abbr:`HTTPS`, nor can clouds operate over other protocols.


.. _reference.feed.cloud.port:

:py:attr:`feed.cloud.port`
--------------------------

The port of the cloud.  Should be an integer, but :program:`Universal Feed
Parser` currently returns it as a string.


.. _reference.feed.cloud.path:

:py:attr:`feed.cloud.path`
--------------------------

The :abbr:`URL (Uniform Resource Locator)` path of the cloud.


.. _reference.feed.cloud.registerProcedure:

:py:attr:`feed.cloud.registerProcedure`
---------------------------------------

The name of the procedure to call on the cloud.


.. _reference.feed.cloud.protocol:

:py:attr:`feed.cloud.protocol`
------------------------------

The protocol of the cloud.  Documentation differs on what the acceptable values
are.  Acceptable values definitely include xml-rpc and soap, although only in
lowercase, despite both being acronyms.

There is no way for a publisher to specify the version number of the protocol
to use.  soap refers to :abbr:`SOAP (Simple Object Access Protocol)` 1.1; the
cloud interface does not support :abbr:`SOAP (Simple Object Access Protocol)`
1.0 or 1.2.

post or http-post might also be acceptable values; nobody really knows for
sure.


.. rubric:: Comes from

* /rss/channel/cloud
