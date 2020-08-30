import os
import sys

# project information
project = u'feedparser'
copyright = u'2010-2020 Kurt McKee, 2004-2008 Mark Pilgrim'
version = u'6.0.0b2'
release = u'6.0.0b2'
language = u'en'

# documentation options
master_doc = 'index'
exclude_patterns = ['_build']

# use a custom extension to make Sphinx add a <link> to feedparser.css
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
extensions = ['add_custom_css']

# customize the html
# files in html_static_path will be copied into _static/ when compiled
html_static_path = ['_static']
