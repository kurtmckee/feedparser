<?xml version='1.0'?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  version='1.0'>
  
<xsl:import href="../docbook/xsl/html/docbook.xsl"/>
<xsl:import href="nonhtmlcommon.xsl"/>

<xsl:param name="callout.list.table" select="0"/>
<xsl:param name="generate.toc">
appendix  
article   
book      toc
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

<xsl:template name="dingbat.characters">
  <xsl:param name="dingbat">bullet</xsl:param>
  <xsl:variable name="lang">
    <xsl:call-template name="l10n.language"/>
  </xsl:variable>
  <xsl:choose>
    <xsl:when test="$dingbat='bullet'">*</xsl:when>
    <xsl:when test="$dingbat='copyright'">(c)</xsl:when>
    <xsl:when test="$dingbat='trademark'">(tm)</xsl:when>
    <xsl:when test="$dingbat='trade'">(tm)</xsl:when>
    <xsl:when test="$dingbat='registered'">(r)</xsl:when>
    <xsl:when test="$dingbat='service'">(SM)</xsl:when>
    <xsl:when test="$dingbat='nbsp'"> </xsl:when>
    <xsl:when test="$dingbat='ldquo'"><xsl:choose><xsl:when test="$lang='fr'">&lt;&lt;</xsl:when><xsl:otherwise>"</xsl:otherwise></xsl:choose></xsl:when>
    <xsl:when test="$dingbat='rdquo'"><xsl:choose><xsl:when test="$lang='fr'">&gt;&gt;</xsl:when><xsl:otherwise>"</xsl:otherwise></xsl:choose></xsl:when>
    <xsl:when test="$dingbat='lsquo'">'</xsl:when>
    <xsl:when test="$dingbat='rsquo'">'</xsl:when>
    <xsl:when test="$dingbat='em-dash'">-</xsl:when>
    <xsl:when test="$dingbat='mdash'">-</xsl:when>
    <xsl:when test="$dingbat='en-dash'">-</xsl:when>
    <xsl:when test="$dingbat='ndash'">-</xsl:when>
    <xsl:otherwise>
      <xsl:text>*</xsl:text>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>

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

<xsl:template match="ulink">
  <a>
    <xsl:if test="@id">
      <xsl:attribute name="name"><xsl:value-of select="@id"/></xsl:attribute>
    </xsl:if>
    <xsl:attribute name="href"><xsl:value-of select="@url"/></xsl:attribute>
    <xsl:if test="$ulink.target != ''">
      <xsl:attribute name="target">
        <xsl:value-of select="$ulink.target"/>
      </xsl:attribute>
    </xsl:if>
    <xsl:choose>
      <xsl:when test="count(child::node())=0">
	<xsl:value-of select="@url"/>
      </xsl:when>
      <xsl:otherwise>
	<xsl:apply-templates/>
        <xsl:text> [</xsl:text>
        <xsl:value-of select="@url"/>
        <xsl:text>]</xsl:text>
      </xsl:otherwise>
    </xsl:choose>
  </a>
</xsl:template>

</xsl:stylesheet>
