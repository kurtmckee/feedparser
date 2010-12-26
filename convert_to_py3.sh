#!/bin/sh

# If the sgmllib3.py file exists, copy it to sgmllib.py
if [ -e feedparser/sgmllib3.py ]; then
    echo "Copying feedparser/sgmllib3.py to feedparser/sgmllib.py"
    cp feedparser/sgmllib3.py feedparser/sgmllib.py
fi

echo "Using the 2to3 tool to convert feedparser.py and feedparsertest.py to Python 3"
2to3 -w feedparser/feedparser.py feedparser/feedparsertest.py

if [ ! -e feedparser/sgmllib3.py ]; then
    echo "No Python 3 version of sgmllib was found. This is a required library."
    echo "See README-PYTHON3 for more details"
fi
