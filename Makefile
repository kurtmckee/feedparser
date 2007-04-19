VERSION = 4.2
XSLTPROC = xsltproc
XMLLINT = xmllint
PYTHON = python
PYTHON21 = c:\python21\python.exe
PYTHON22 = c:\python22\python.exe
PYTHON23 = c:\python23\python.exe

test:
	cd feedparser; \
	${PYTHON} feedparsertest.py; \
	cd ..

testall: test
	cd feedparser; \
	${PYTHON23} feedparsertest.py; \
	${PYTHON22} feedparsertest.py; \
	${PYTHON21} feedparsertest.py; \
	cd ..

validate:
	cd feedparser; \
	${XMLLINT} --noout --valid docs/xml/feedparser.xml; \
	cd ..

.PHONY: docs

docs: validate
	${XSLTPROC} feedparser/docs/xsl/html.xsl feedparser/docs/xml/feedparser.xml
	${PYTHON} util/colorize.py www/docs/ 0

clean:
	rm -rf dist
	rm -f feedparser/*.pyc
	rm -rf util/*.pyc

maintainer-clean: clean
	rm -f www/docs/*.html

release-check:
	${PYTHON} util/releasecheck.py

dist: validate release-check
	mkdir -p dist/docs
	rsync -a --exclude=.svn --exclude=directory_listing.css www/css dist/docs/
	rsync -a --exclude=.svn --exclude=atom-logo100px.gif www/docs/images dist/docs/
	rsync -a --exclude=.svn www/docs/examples dist/docs/
	${XSLTPROC} feedparser/docs/xsl/htmldist.xsl feedparser/docs/xml/feedparser.xml
	${PYTHON} util/colorize.py dist/docs/ 0
	mkdir -p dist/feedparser-${VERSION}
	mv dist/docs dist/feedparser-${VERSION}/
	rsync -a LICENSE dist/feedparser-${VERSION}/
	rsync -a README dist/feedparser-${VERSION}/
	rsync -a feedparser/feedparser.py dist/feedparser-${VERSION}/
	rsync -a feedparser/setup.py dist/feedparser-${VERSION}/
	cd dist; \
	zip -9rq feedparser-${VERSION}.zip feedparser-${VERSION}; \
	cd ..
	mv dist/feedparser-${VERSION} dist/feedparser-tests-${VERSION}
	rsync -a README-TESTS dist/feedparser-tests-${VERSION}
	rsync -a feedparser/feedparsertest.py dist/feedparser-tests-${VERSION}
	rsync -a --exclude=.svn feedparser/tests dist/feedparser-tests-${VERSION}
	cd dist; \
	zip -9rq feedparser-tests-${VERSION}.zip feedparser-tests-${VERSION} -x \*/.svn/\*; \
	cd ..
	rm -rf dist/feedparser-tests-${VERSION}
	ls -l dist

all: validate release-check maintainer-clean docs dist
