import os
import pathlib
import re
import sys


content = (pathlib.Path(__file__).parent.parent / 'pyproject.toml').read_text()
match = re.search(r'''version *= *"(?P<version>.+?)"''', content)
version = match.group('version')
release = version

# Project information
project = 'feedparser'
copyright = '2010-2022 Kurt McKee, 2004-2008 Mark Pilgrim'
language = 'en'

# General configuration
root_doc = 'index'
exclude_patterns = ['_build']
nitpicky = True

# HTML options
# Files in `html_static_path` will be copied to `_static/` when compiled.
html_static_path = ['_static']

# Use a custom extension to make Sphinx add a <link> to `feedparser.css`.
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
extensions = ['add_custom_css']
