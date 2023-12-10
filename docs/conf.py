import os
import pathlib
import re
import sys


content = (pathlib.Path(__file__).parent.parent / 'feedparser/__init__.py').read_text()
match = re.search(r"""__version__ = ['"](?P<version>.+?)['"]""", content)
version = match.group('version')
release = version

# project information
project = 'feedparser'
copyright = '2010-2023 Kurt McKee, 2004-2008 Mark Pilgrim'
language = 'en'

# documentation options
master_doc = 'index'
exclude_patterns = ['_build']

# use a custom extension to make Sphinx add a <link> to feedparser.css
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
extensions = ['add_custom_css']

# customize the html
# files in html_static_path will be copied into _static/ when compiled
html_static_path = ['_static']
