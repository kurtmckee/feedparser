<?xml version='1.0'?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  version='1.0'>
  
<xsl:import href="../docbook/xsl/html/docbook.xsl"/>
<xsl:import href="nonhtmlcommon.xsl"/>

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

<xsl:template match="*" mode="process.root">
  <xsl:variable name="doc" select="self::*"/>
  <html xmlns:o="urn:schemas-microsoft-com:office:office"
        xmlns:w="urn:schemas-microsoft-com:office:word"
        xmlns="http://www.w3.org/TR/REC-html40">
  <head>
    <xsl:call-template name="head.content">
      <xsl:with-param name="node" select="$doc"/>
    </xsl:call-template>
    <xsl:call-template name="user.head.content">
      <xsl:with-param name="node" select="$doc"/>
    </xsl:call-template>
  </head>
  <body>
    <xsl:call-template name="body.attributes"/>
    <xsl:call-template name="user.header.content">
      <xsl:with-param name="node" select="$doc"/>
    </xsl:call-template>
    <xsl:apply-templates select="."/>
    <xsl:call-template name="user.footer.content">
      <xsl:with-param name="node" select="$doc"/>
    </xsl:call-template>
  </body>
  </html>
</xsl:template>

<xsl:template name="user.head.content">
  <xsl:param name="node" select="."/>
  <meta name="ProgId" content="Word.Document"/>
  <meta name="Generator" content="Microsoft Word 9"/>
  <meta name="Originator" content="Microsoft Word 9"/> 

  <!-- Start document properties -->
  <xsl:comment>[if gte mso 9]>&lt;xml>
  &lt;o:DocumentProperties>
    &lt;o:Author>Mark Pilgrim&lt;/o:Author>
  &lt;/o:DocumentProperties>
  &lt;w:WordDocument>
  &lt;w:View>Print&lt;/w:View>
  &lt;w:Zoom>100&lt;/w:Zoom>
  &lt;/w:WordDocument>
  &lt;/xml>&lt;![endif]</xsl:comment>
  <!--End document properties -->
  
  <!--Start styles -->
  <style>
  <xsl:comment>
    /* Font Definitions */
    @font-face
    {font-family:Verdana;
    panose-1:2 11 6 4 3 5 4 4 2 4;
    mso-font-charset:0;
    mso-generic-font-family:swiss;
    mso-font-pitch:variable;
    mso-font-signature:536871559 0 0 0 415 0;}
     /* Style Definitions */
    p.MsoNormal, li.MsoNormal, div.MsoNormal
    {mso-style-parent:"";
    margin:0in;
    margin-bottom:.0001pt;
    mso-pagination:widow-orphan;
    font-size:10.0pt;
    font-family:"Times New Roman";
    mso-fareast-font-family:"Times New Roman";}
    h3
    {mso-style-next:Normal;
    margin:0in;
    margin-bottom:.0001pt;
    mso-pagination:widow-orphan;
    page-break-after:avoid;
    mso-outline-level:3;
    font-size:12.0pt;
    font-family:Arial;
    font-style:italic;}
    @page Section1
    {size:595.3pt 841.9pt;
    margin:1.0in 1.25in 1.0in 1.25in;
    mso-header-margin:.5in;
    mso-footer-margin:.5in;
    mso-paper-source:0;}
    div.Section1
    {page:Section1;}
  </xsl:comment>
  </style>
  <!--End styles -->
</xsl:template>

<xsl:template name="user.header.content">
  <br clear='all' style='page-break-before:always'/>
</xsl:template>

<!-- insert page breaks at appropriate places -->
<xsl:template match="chapter|preface|appendix">
  <br clear='all' style='page-break-before:always'/>
  <xsl:apply-imports/>
</xsl:template>

</xsl:stylesheet>
