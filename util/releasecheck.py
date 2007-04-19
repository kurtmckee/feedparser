import sys, re, time, os
sys.path.insert(0, os.path.join(os.getcwd(), 'feedparser'))
import feedparser
import feedparsertest

if feedparser._debug:
    sys.stderr.write('feedparser._debug == 1\n')
    sys.exit(1)

if feedparsertest._debug:
    sys.stderr.write('feedparsertest._debug == 1\n');
    sys.exit(1)

makefile_version = None
feedparser_version = None
docs_version = None
setup_version = None
docs_date = None

makefile_re = re.compile(r'^VERSION\s*=\s*(.*?)$')
for line in file('Makefile'):
    m = makefile_re.search(line)
    if m:
        makefile_version = m.group(1)
        break
if not makefile_version:
    sys.stderr.write('could not determine Makefile version\n')
    sys.exit(1)

feedparser_version = feedparser.__version__
if not feedparser_version:
    sys.stderr.write('could not determine feedparser.py version\n')
    sys.exit(1)

docs_re = re.compile(r'^<!ENTITY\s*feedparser_version\s*["\'](.*?)["\']>$')
for line in file('feedparser/docs/xml/feedparser.xml'):
    m = docs_re.search(line)
    if m:
        docs_version = m.group(1)
        break
if not docs_version:
    sys.stderr.write('could not determine feedparser docs version\n')
    sys.exit(1)

setup_re = re.compile(r'^\s*version\s*=\s*["\'](.*?)["\']\s*,\s*$')
for line in file('feedparser/setup.py'):
    m = setup_re.search(line)
    if m:
        setup_version = m.group(1)
        break
if not setup_version:
    sys.stderr.write('could not determine setup.py version\n')
    sys.exit(1)
    
if makefile_version != feedparser_version:
    sys.stderr.write('Makefile version = %s, but feedparser.py version = %s\n' % (makefile_version, feedparser_version))
    sys.exit(1)

if makefile_version != docs_version:
    sys.stderr.write('Makefile version = %s, but docs version = %s\n' % (makefile_version, docs_version))
    sys.exit(1)

if makefile_version != setup_version:
    sys.stderr.write('Makefile version = %s, but setup.py version = %s\n' % (makefile_version, setup_version))
    sys.exit(1)

if feedparser_version != docs_version:
    sys.stderr.write('feedparser.py version = %s, but docs version = %s\n' % (feedparser_version, docs_version))
    sys.exit(1)

if feedparser_version != setup_version:
    sys.stderr.write('feedparser.py version = %s, but setup.py version = %s\n' % (feedparser_version, setup_version))
    sys.exit(1)

if setup_version != docs_version:
    sys.stderr.write('setup.py version = %s, but docs version = %s\n' % (setup_version, docs_version))
    sys.exit(1)

date_re = re.compile(r'^<!ENTITY\s*fileversion\s*["\'](.*?)["\']>$')
for line in file('feedparser/docs/xml/version.xml'):
    m = date_re.search(line)
    if m:
        docs_date = m.group(1)
if not docs_date:
    sys.stderr.write('could not determine feedparser docs date\n')
    sys.exit(1)

todays_date = time.strftime('%Y-%m-%d')
if docs_date != todays_date:
    sys.stderr.write('docs date = %s but today is %s\n' % (docs_date, todays_date))
    sys.exit(1)
