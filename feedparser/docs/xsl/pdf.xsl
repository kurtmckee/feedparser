<?xml version='1.0'?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  version='1.0'>
  
<xsl:import href="../docbook/xsl/html/docbook.xsl"/>
<xsl:import href="nonhtmlcommon.xsl"/>

<xsl:output indent="yes" doctype-public="-//W3C//DTD HTML 4.01 Transitional//EN" doctype-system="http://www.w3.org/TR/html4/loose.dtd"/>

<xsl:param name="generate.toc">
appendix  
article   
book      
chapter   
part      
preface   
qandadiv  
qandaset  
reference 
sect1     
sect2     
sect3     
sect4     
sect5     
section   
set       
</xsl:param>

<!-- This stylesheet assumes that the output will be run through HTMLDoc to produce PDF.
     http://easysw.com/htmldoc/
-->

<xsl:template match="chapter/section[position()!=1]">
  <xsl:comment> PAGE BREAK </xsl:comment>
  <xsl:apply-imports/>
</xsl:template>

<!-- HTMLDoc incorrectly converts the trademark character and several other special
     characters, so spell them out or use simpler characters -->
<xsl:template name="dingbat.characters">
  <xsl:param name="dingbat">bullet</xsl:param>
  <xsl:choose>
    <xsl:when test="$dingbat='bullet'">&#x2022;</xsl:when>
    <xsl:when test="$dingbat='copyright'">&#x00A9;</xsl:when>
    <xsl:when test="$dingbat='trademark'">(tm)</xsl:when>
    <xsl:when test="$dingbat='trade'">(tm)</xsl:when>
    <xsl:when test="$dingbat='registered'">&#x00AE;</xsl:when>
    <xsl:when test="$dingbat='service'">(SM)</xsl:when>
    <xsl:when test="$dingbat='nbsp'">&#x00A0;</xsl:when>
    <xsl:when test="$dingbat='ldquo'">"</xsl:when>
    <xsl:when test="$dingbat='rdquo'">"</xsl:when>
    <xsl:when test="$dingbat='lsquo'">'</xsl:when>
    <xsl:when test="$dingbat='rsquo'">'</xsl:when>
    <xsl:when test="$dingbat='em-dash'">&#x2014;</xsl:when>
    <xsl:when test="$dingbat='mdash'">&#x2014;</xsl:when>
    <xsl:when test="$dingbat='en-dash'">&#x2013;</xsl:when>
    <xsl:when test="$dingbat='ndash'">&#x2013;</xsl:when>
    <xsl:otherwise>
      <xsl:text>&#x2022;</xsl:text>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>

<!-- HTMLDoc incorrectly converts curly quotes, and I don't know how to override
     the dingbat characters given in the internationalization files of the
     DocBook stylesheets, so this is a hack to get quotes to show up properly
     in my PDFs by using the straight quote characters defined in my customized
     dingbat.characters template above.  This breaks internationalization (several
     languages use some character other than quotes to represent a quotation),
     but we'll worry about that when somebody translates it.
-->
<xsl:template name="gentext.startquote">
  <xsl:call-template name="dingbat.characters">
    <xsl:with-param name="dingbat">ldquo</xsl:with-param>
  </xsl:call-template>
</xsl:template>

<xsl:template name="gentext.endquote">
  <xsl:call-template name="dingbat.characters">
    <xsl:with-param name="dingbat">rdquo</xsl:with-param>
  </xsl:call-template>
</xsl:template>

</xsl:stylesheet>
