VERSION = 4.0.2
XSLTPROC = xsltproc
XMLLINT = xmllint
PYTHON = python
PYTHON21 = c:\python21\python.exe
PYTHON22 = c:\python22\python.exe
PYTHON23 = c:\python23\python.exe

test:
	${PYTHON} feedparsertest.py

testall: test
	${PYTHON23} feedparsertest.py
	${PYTHON22} feedparsertest.py
	${PYTHON21} feedparsertest.py

validate:
	${XMLLINT} --noout --valid docs/xml/feedparser.xml

.PHONY: docs

docs: validate
	cd docs; \
	${XSLTPROC} xsl/html.xsl xml/feedparser.xml; \
	${PYTHON} py/colorize.py . 0; \
	cd ..

clean:
	rm -rf dist
	rm -f *.pyc
	rm -rf docs/dist
	rm -rf docs/py/*.pyc

maintainer-clean: clean
	rm -f docs/*.html

release-check:
	${PYTHON} releasecheck.py

dist: validate
	cd docs; \
	mkdir -p dist/docs/; \
	rsync -rtpvz --exclude=CVS --exclude=directory_listing.css ../css dist/docs/; \
	rsync -rtpvz --exclude=CVS --exclude=atom-logo100px.gif images dist/docs/; \
	rsync -rtpvz --exclude=CVS examples dist/docs/; \
	${XSLTPROC} xsl/htmldist.xsl xml/feedparser.xml; \
	${PYTHON} py/colorize.py dist/docs/ 0; \
	cd ..
	mkdir -p dist
	zip -9r dist/feedparser-${VERSION}.zip LICENSE README feedparser.py setup.py
	cd docs/dist/; \
	zip -9r ../../dist/feedparser-${VERSION}.zip docs; \
	cd ../../
	zip -9r dist/feedparser-tests-${VERSION}.zip LICENSE README-TESTS feedparser.py feedparsertest.py tests -x \*/CVS/\*
	ls -l dist

all: validate release-check maintainer-clean docs dist
