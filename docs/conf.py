import pathlib
import re
import sys

content = (pathlib.Path(__file__).parent.parent / "pyproject.toml").read_text()
match = re.search(r'''version *= *"(?P<version>.+?)"''', content)
version = match.group("version")
release = version

# Project information
project = "feedparser"
copyright = "2010-2026 Kurt McKee, 2004-2008 Mark Pilgrim"
language = "en"

# General configuration
root_doc = "index"
exclude_patterns = ["_build"]
nitpicky = True

# HTML options
# Files in `html_static_path` will be copied to `_static/` when compiled.
html_theme = "alabaster"
html_static_path = [
    "_static",
]
html_theme_options = {
    "logo": "logo.png",
    "logo_name": True,
    "description": "Parse RSS/Atom/JSON feeds in Python.",
    # Link to GitHub
    "github_user": "kurtmckee",
    "github_repo": "feedparser",
    "github_button": True,
    "github_type": "star",
    "github_count": False,
    # Don't show "Powered by" text.
    "show_powered_by": False,
}
templates_path = ["_templates"]
html_sidebars = {
    "index": [
        "about-no-logo.html.jinja",  # Custom
        "donate.html",
        "navigation.html",
        "relations.html",
        "searchbox.html",
    ],
    "**": [
        "about.html.jinja",  # Custom
        "searchfield.html",
        "navigation.html",
        "relations.html",
        "donate.html",
    ],
}
html_extra_path = ["examples"]


# Don't copy source .rst files into the built documentation.
html_copy_source = False

sys.path.append(str(pathlib.Path(__file__).parent / "extensions"))
extensions = [
    # Make Sphinx add a <link> to `feedparser.css`.
    "add_custom_css",
    # Unconditionally replace $XYZ variables in .rst sources.
    "variable_substitutions",
]
