<?xml version='1.0'?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  version='1.0'>
  
<xsl:import href="../docbook/xsl/html/chunk.xsl"/>
<xsl:import href="htmlcommon.xsl"/>
<xsl:param name="html.stylesheet">../css/feedparser.css</xsl:param>

<xsl:param name="using.chunker" select="1"/>
<xsl:param name="base.dir">www/docs/</xsl:param>
<xsl:param name="admon.graphics.path">images/</xsl:param>
<xsl:param name="callout.graphics.path">images/callouts/</xsl:param>
<xsl:param name="chunk.first.sections" select="1"/>
<xsl:param name="chunk.quietly" select="0"/>

<xsl:param name="generate.toc">
appendix  toc
article   toc
book      toc
chapter   toc
part      toc
preface   toc
qandadiv  toc
qandaset  toc
reference toc
sect1     toc
sect2     toc
sect3     toc
sect4     toc
sect5     toc
section   toc
set       toc
</xsl:param>

<xsl:param name="chunker.output.method" select="'html'"/>
<xsl:param name="chunker.output.encoding" select="'utf-8'"/>
<xsl:param name="chunker.output.indent" select="'yes'"/>
<xsl:param name="chunker.output.omit-xml-declaration" select="'yes'"/>
<xsl:param name="chunker.output.standalone" select="'no'"/>
<!--
<xsl:param name="chunker.output.doctype-public" select="'-//W3C//DTD HTML 4.01 Transitional//EN'"/>
<xsl:param name="chunker.output.doctype-system" select="'http://www.w3.org/TR/html4/loose.dtd'"/>
-->

<xsl:param name="chunker.output.doctype-public" select="'-//W3C//DTD HTML 4.01//EN'"/>
<xsl:param name="chunker.output.doctype-system" select="'http://www.w3.org/TR/html4/strict.dtd'"/>

<!--
<xsl:param name="chunker.output.doctype-public" select="'-//W3C//DTD XHTML 1.0 Strict//EN'"/>
<xsl:param name="chunker.output.doctype-system" select="'http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd'"/>
-->
<xsl:param name="chunker.output.media-type"/>
<xsl:param name="chunker.output.cdata-section-elements"/>

<!--
<xsl:param name="rootid">basic</xsl:param>
-->

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
            <a href="../">
              <xsl:call-template name="gentext">
                <xsl:with-param name="key">nav-home</xsl:with-param>
              </xsl:call-template>
            </a>
            <xsl:call-template name="breadcrumb.trail.separator"/>
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

<!-- provide breadcrumb-style navigation back to chapter/main TOC -->
<xsl:template name="breadcrumb.trail.separator">
  <xsl:text> &#8594; </xsl:text>
</xsl:template>

<xsl:template name="breadcrumb.trail">
  <xsl:param name="node" select="."/>
  <xsl:param name="link" select="0"/>

  <xsl:variable name="title">
    <xsl:apply-templates select="$node" mode="title.markup.textonly"/>
  </xsl:variable>
  
  <xsl:if test="$node!=/*[1]">
    <xsl:call-template name="breadcrumb.trail">
      <xsl:with-param name="node" select="$node/.."/>
      <xsl:with-param name="link" select="1"/>
    </xsl:call-template>
  </xsl:if>
  
  <xsl:choose>
    <xsl:when test="$link!='0'">
      <a>
        <xsl:attribute name="href">
          <xsl:call-template name="href.target">
            <xsl:with-param name="object" select="$node"/>
          </xsl:call-template>
        </xsl:attribute>
        <xsl:value-of select="$title"/>
      </a>
      <xsl:call-template name="breadcrumb.trail.separator"/>
    </xsl:when>
    <xsl:otherwise>
      <span class="thispage">
        <xsl:apply-templates select="$node" mode="title.markup.textonly"/>
      </span>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>

<xsl:template name="header.navigation">
  <xsl:param name="prev" select="/foo"/>
  <xsl:param name="next" select="/foo"/>

  <xsl:comment>#include virtual="/inc/header.html"</xsl:comment>

</xsl:template>

<xsl:template name="footer.navigation">
  <xsl:param name="prev" select="/foo"/>
  <xsl:param name="next" select="/foo"/>
  <div style="float: left">
    <xsl:if test="count($prev)>0">
      <xsl:text>&#8592;&#160;</xsl:text>
      <a class="NavigationArrow">
        <xsl:attribute name="href">
          <xsl:call-template name="href.target">
            <xsl:with-param name="object" select="$prev"/>
          </xsl:call-template>
        </xsl:attribute>
        <xsl:apply-templates select="$prev" mode="title.markup.textonly"/>
      </a>
    </xsl:if>
  </div>
  <div style="text-align: right">
    <xsl:if test="count($next)>0">
      <a class="NavigationArrow">
        <xsl:attribute name="href">
          <xsl:call-template name="href.target">
            <xsl:with-param name="object" select="$next"/>
          </xsl:call-template>
        </xsl:attribute>
        <xsl:apply-templates select="$next" mode="title.markup.textonly"/>
      </a>
      <xsl:text>&#160;&#8594;</xsl:text>
    </xsl:if>
  </div>
  <hr style="clear:both"/>
  <div class="footer">
    <xsl:apply-templates select="//bookinfo//copyright" mode="titlepage.mode"/>
  </div>
</xsl:template>
    
<!-- utility template used by navigation links to produce plain-text version of link target titles -->
<xsl:template match="*" mode="title.markup.textonly">
  <xsl:variable name="markup">
    <xsl:apply-templates select="." mode="title.markup"/>
  </xsl:variable>
  <xsl:value-of select="$markup"/>
</xsl:template>

<!-- display "further reading" and other lists with stylized caption -->
<xsl:template match="itemizedlist">
  <xsl:variable name="customclass">
    <xsl:choose>
      <xsl:when test="@role='furtherreading'">furtherreading</xsl:when>
      <xsl:when test="@role='reference-from'">reference-from</xsl:when>
      <xsl:when test="@role='seealso'">seealso</xsl:when>
      <xsl:otherwise><xsl:value-of select="name(.)"/></xsl:otherwise>
    </xsl:choose>
  </xsl:variable>
  <div class="{$customclass}">
    <xsl:apply-templates select="title"/>
    <ul>
      <xsl:apply-templates select="listitem"/>
    </ul>
  </div>
</xsl:template>

<xsl:template match="itemizedlist/title">
  <h3>
    <xsl:apply-templates/>
  </h3>
</xsl:template>

<!-- display revision history with stylized caption -->
<xsl:template match="revhistory" mode="titlepage.mode">
  <div class="{name(.)}">
    <xsl:apply-templates mode="titlepage.mode"/>
  </div>
</xsl:template>

<xsl:template match="revhistory/revision" mode="titlepage.mode">
  <xsl:param name="numcols" select="'2'"/>
  <xsl:variable name="revnumber" select=".//revnumber"/>
  <xsl:variable name="revdate"   select=".//date"/>
  <xsl:variable name="revauthor" select=".//authorinitials"/>
  <xsl:variable name="revremark" select=".//revremark|.//revdescription"/>
  <a>
    <xsl:attribute name="name"><xsl:apply-templates select="$revnumber[1]" mode="titlepage.mode"/></xsl:attribute>
  </a>
  <h3 class="revdate">
    <xsl:apply-templates select="$revdate[1]" mode="titlepage.mode"/>
    <xsl:text> (</xsl:text>
    <xsl:apply-templates select="$revnumber[1]" mode="titlepage.mode"/>
    <xsl:text>)</xsl:text>
  </h3>
  <xsl:if test="$revremark">
    <xsl:apply-templates select="$revremark[1]" mode="titlepage.mode"/>
  </xsl:if>
</xsl:template>

<!-- display custom header on table of contents -->
<xsl:template name="book.titlepage.recto">
  <xsl:apply-templates mode="book.titlepage.recto.auto.mode" select="bookinfo/releaseinfo"/>
  <xsl:apply-templates mode="book.titlepage.recto.auto.mode" select="bookinfo/pubdate"/>
  <xsl:apply-templates mode="book.titlepage.recto.auto.mode" select="bookinfo/abstract"/>
  <xsl:apply-templates mode="book.titlepage.recto.auto.mode" select="bookinfo/copyright"/>
  <xsl:apply-templates mode="book.titlepage.recto.auto.mode" select="bookinfo/legalnotice"/>
</xsl:template>

<!-- customize page title (bleah, wish there were a better way to do this -->
<xsl:template name="head.content">
  <xsl:param name="node" select="."/>
  <xsl:param name="title">
    <xsl:apply-templates select="$node" mode="object.title.markup.textonly"/>
  </xsl:param>

  <title>
    <!-- this is the only line that has changed -->
    <xsl:copy-of select="$title"/><xsl:text> [Universal Feed Parser]</xsl:text>
  </title>

  <xsl:if test="$html.stylesheet != ''">
    <xsl:call-template name="output.html.stylesheets">
      <xsl:with-param name="stylesheets" select="normalize-space($html.stylesheet)"/>
    </xsl:call-template>
  </xsl:if>

  <xsl:if test="$link.mailto.url != ''">
    <link rev="made"
          href="{$link.mailto.url}"/>
  </xsl:if>

  <xsl:if test="$html.base != ''">
    <base href="{$html.base}"/>
  </xsl:if>

  <meta name="generator" content="DocBook XSL Stylesheets V{$VERSION}"/>

  <xsl:if test="$generate.meta.abstract != 0">
    <xsl:variable name="info" select="(articleinfo
                                      |bookinfo
                                      |prefaceinfo
                                      |chapterinfo
                                      |appendixinfo
                                      |sectioninfo
                                      |sect1info
                                      |sect2info
                                      |sect3info
                                      |sect4info
                                      |sect5info
                                      |referenceinfo
                                      |refentryinfo
                                      |partinfo
                                      |info
                                      |docinfo)[1]"/>
    <xsl:if test="$info and $info/abstract">
      <meta name="description">
        <xsl:attribute name="content">
          <xsl:for-each select="$info/abstract[1]/*">
            <xsl:value-of select="."/>
            <xsl:if test="position() &lt; last()">
              <xsl:text> </xsl:text>
            </xsl:if>
          </xsl:for-each>
        </xsl:attribute>
      </meta>
    </xsl:if>
  </xsl:if>

  <xsl:if test="($draft.mode = 'yes' or
                ($draft.mode = 'maybe' and
                ancestor-or-self::*[@status][1]/@status = 'draft'))
                and $draft.watermark.image != ''">
    <style type="text/css"><xsl:text>
body { background-image: url('</xsl:text>
<xsl:value-of select="$draft.watermark.image"/><xsl:text>');
       background-repeat: no-repeat;
       background-position: top left;
       /* The following properties make the watermark "fixed" on the page. */
       /* I think that's just a bit too distracting for the reader... */
       /* background-attachment: fixed; */
       /* background-position: center center; */
     }</xsl:text>
    </style>
  </xsl:if>
  <xsl:apply-templates select="." mode="head.keywords.content"/>
</xsl:template>

<!-- add permalink icon to all anchors -->
<xsl:template name="anchor">
  <xsl:param name="node" select="."/>
  <xsl:param name="conditional" select="1"/>
  <xsl:variable name="id">
    <xsl:call-template name="object.id">
      <xsl:with-param name="object" select="$node"/>
    </xsl:call-template>
  </xsl:variable>
  <xsl:if test="$conditional = 0 or $node/@id">
    <xsl:variable name="title">
      <xsl:choose>
        <xsl:when test="local-name($node)='title'"><xsl:value-of select="local-name(parent::*)"/></xsl:when>
        <xsl:otherwise><xsl:value-of select="local-name($node)"/></xsl:otherwise>
      </xsl:choose>
    </xsl:variable>
    <a name="{$id}" class="skip" href="#{$id}" title="link to this {$title}">
      <img src="{$admon.graphics.path}permalink.gif" alt="[link]" title="link to this {$title}" width="8" height="9"/>
    </a>
    <xsl:text> </xsl:text>
  </xsl:if>
</xsl:template>

</xsl:stylesheet>
