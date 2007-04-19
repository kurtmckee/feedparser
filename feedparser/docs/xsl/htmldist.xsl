<?xml version='1.0'?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  version='1.0'>
  
<xsl:import href="../docbook/xsl/html/chunk.xsl"/>
<xsl:import href="html.xsl"/>
<xsl:param name="html.stylesheet">feedparser.css</xsl:param>
<xsl:param name="base.dir">dist/docs/</xsl:param>

<xsl:template name="chunk-element-content">
  <xsl:param name="prev"/>
  <xsl:param name="next"/>
  <xsl:param name="nav.context"/>
  <xsl:param name="content">
    <xsl:apply-imports/>
  </xsl:param>
  <html>
    <xsl:attribute name="lang">
      <xsl:value-of select="//book/@lang"/>
    </xsl:attribute>
    <xsl:call-template name="html.head">
      <xsl:with-param name="prev" select="$prev"/>
      <xsl:with-param name="next" select="$next"/>
    </xsl:call-template>
    <body id="feedparser-org" class="docs">
      <xsl:call-template name="body.attributes"/>
      <xsl:call-template name="header.navigation">
	<xsl:with-param name="prev" select="$prev"/>
	<xsl:with-param name="next" select="$next"/>
	<xsl:with-param name="nav.context" select="$nav.context"/>
      </xsl:call-template>
      <div id="main">
        <div id="mainInner">
          <p id="breadcrumb"><xsl:text>You are here: </xsl:text>
            <xsl:call-template name="breadcrumb.trail"/>
          </p>
          <xsl:call-template name="user.header.content"/>
          <xsl:copy-of select="$content"/>
          <xsl:call-template name="user.footer.content"/>
          <xsl:call-template name="footer.navigation">
            <xsl:with-param name="prev" select="$prev"/>
            <xsl:with-param name="next" select="$next"/>
            <xsl:with-param name="nav.context" select="$nav.context"/>
          </xsl:call-template>
          <xsl:call-template name="user.footer.navigation"/>
        </div>
      </div>
    </body>
  </html>
</xsl:template>

<xsl:template name="header.navigation">
  <xsl:param name="prev" select="/foo"/>
  <xsl:param name="next" select="/foo"/>

<div class="z" id="intro">
<div class="sectionInner">
<div class="sectionInner2">

<div class="s" id="pageHeader">
<h1><a href="/"><span>Universal Feed Parser</span></a></h1>
<p><span>Parse RSS and Atom feeds in Python.  4000 unit tests.  Open source.</span></p>
</div> <!-- pageHeader -->

<div class="s" id="quickSummary">
<ul>
  <li class="li1"><a href="http://code.google.com/p/feedparser/downloads/list"><span>Download</span></a> &#183;</li>
  <li class="li2"><a href="http://feedparser.org/docs/"><span>Documentation</span></a> &#183;</li>
  <li class="li3"><a href="http://feedparser.org/tests/"><span>Unit tests</span></a> &#183;</li>
  <li class="li4"><a href="http://code.google.com/p/feedparser/issues/list"><span>Report a bug</span></a></li>
</ul>
</div> <!-- quickSummary -->
</div>
</div>
</div> <!-- intro -->

</xsl:template>

</xsl:stylesheet>
