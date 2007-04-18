"""
Colorize Python program listings embedded in HTML pages

This script is used during the build process of "Dive Into Python"
(http://diveintopython.org/) to recreate syntax highlighting of the Python
program listings and code examples embedded in the HTML pages by wrapping
Python keywords in <span> or <font> tags.  The following
tags are presumed to contain Python code:
  <pre class="programlisting">...</pre>
  <span class="userinput">...</span>
(These tags are generated automatically by the DocBook XSL stylesheets when
the book is transformed from XML to HTML.)

Looks for 2 arguments on the command line.  The first argument is a file or directory.
If a file, the file is processed; if a directory, all .html files in the directory
are processed.

The second argument, if given, is a flag for the type of tags to wrap around
keywords.
  0 (default) - use <span class="xxx"> tags, where xxx in
        ('comment', 'string', 'keyword', 'function', 'class').  Actual
        syntax highlighting must be defined in a <style> definition
        elsewhere in the document, or in an external style sheet.
  1 - use <font> tags.  See ColorizeParser.fontDataMap for the color values.
  
If no arguments are given, a test suite is performed on a hard-coded test file
which saves the output to a temporary file and opens it in a web browser locally.

Not safe to run on the same file(s) more than once, since it does not check for
existing <span> or <font> tags in the program listings.
"""

__author__ = "Mark Pilgrim (mark@diveintopython.org)"
__version__ = "$Revision$"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2001 Mark Pilgrim"
__license__ = "Python"

import sys
import os
from BaseHTMLProcessor import BaseHTMLProcessor
import pyfontify

class ColorizeParser(BaseHTMLProcessor):
  fontDataMap = {"comment":("<font color='green'><i>", "</i></font>"),
           "string":("<font color='olive'>", "</font>"),
           "keyword":("<font color='navy'><b>", "</b></font>"),
           "function":("<font color='teal'><b>", "</b></font>"),
           "class":("<font color='blue'><b>", "</b></font>")}

  def __init__(self, usefonts=0):
    BaseHTMLProcessor.__init__(self)
    self.usefonts = usefonts

  def reset(self):
    BaseHTMLProcessor.reset(self)
    self.colorindex = 0
    self.needcolor = 0
    
  def HTMLfontify(self, text):
    fontmap = pyfontify.fontify(text)
    fontmap.reverse()
    for token, start, end, dummy in fontmap:
      if self.usefonts:
        text = "%s%s%s%s%s" % (text[:start], self.fontDataMap[token][0], text[start:end], \
                     self.fontDataMap[token][1], text[end:])
      else:
        text = "%s<span class='py%s'>%s</span>%s" % (text[:start], token, text[start:end], text[end:])
    return text

  def flushcolor(self):
    if self.colorindex:
      buffer = "".join(self.pieces[self.colorindex:])
      self.pieces = self.pieces[:self.colorindex]
      self.colorindex = 0
      BaseHTMLProcessor.handle_data(self, self.HTMLfontify(buffer))

  def unknown_starttag(self, tag, attrs):
    self.flushcolor()
    BaseHTMLProcessor.unknown_starttag(self, tag, attrs)
    if self.needcolor:
      self.colorindex = len(self.pieces)

  def unknown_endtag(self, tag):
    self.flushcolor()
    BaseHTMLProcessor.unknown_endtag(self, tag)
    if self.needcolor:
      self.colorindex = len(self.pieces)

  def start_pre(self, attrs):
    self.unknown_starttag("pre", attrs)
    if ("class", "programlisting python") in attrs:
      self.needcolor = 1
      self.colorindex = len(self.pieces)

  def end_pre(self):
    self.needcolor = 0
    self.unknown_endtag("pre")
    
  def start_span(self, attrs):
    self.unknown_starttag("span", attrs)
    if ("class", "userinput") in attrs:
      self.needcolor = 1
      self.colorindex = len(self.pieces)

  def end_span(self):
    self.needcolor = 0
    self.unknown_endtag("span")
    
def process(filename, usefonts=0, outfile=None):
  if not outfile:
    outfile = filename
  sock = open(filename, "r")
  parser = ColorizeParser(usefonts)
  parser.feed(sock.read())
  output = parser.output()
  sock.close()
  sock = open(outfile, "w")
  sock.write(output)
  sock.close()
  return output

def test(filename, usefonts=0, outfile="c:\\out.html"):
  output = process(filename, usefonts, outfile)
##  print output
  import webbrowser
  webbrowser.open(outfile)

if __name__ == "__main__":
  if sys.argv[1:]:
    filedir = sys.argv[1]
    usefonts = sys.argv[2:] and sys.argv[2] or 0
    if os.path.isdir(filedir):
      import glob
      for f in glob.glob(os.path.join(filedir, '*.html')):
        print "Colorizing %s" % f.replace('\\', '/')
        process(f, usefonts)
    else:
      print "Colorizing %s" % os.path.basename(filedir)
      process(filedir, usefonts)
  else:
    print 'usage: colorize.py directory-or-file'
