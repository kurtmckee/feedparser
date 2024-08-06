import pathlib
import re
import sys

content = (pathlib.Path(__file__).parent.parent / "pyproject.toml").read_text()
match = re.search(r'''version *= *"(?P<version>.+?)"''', content)
version = match.group("version")
release = version

# Project information
project = "feedparser"
copyright = "2010-2024 Kurt McKee, 2004-2008 Mark Pilgrim"
language = "en"

# General configuration
root_doc = "index"
exclude_patterns = ["_build"]
nitpicky = True

# HTML options
# Files in `html_static_path` will be copied to `_static/` when compiled.
html_static_path = ["_static"]
html_theme = "sphinx_rtd_theme"
# Example feeds that will be hosted by Read the Docs.
# The files are double-nested in 'examples/examples/'
# because they're copied to the root of the drive.
html_extra_path = ["examples"]

sys.path.append(str(pathlib.Path(__file__).parent / "extensions"))
extensions = [
    # Make Sphinx add a <link> to `feedparser.css`.
    "add_custom_css",
    # Unconditionally replace $XYZ variables in .rst sources.
    "variable_substitutions",
]
