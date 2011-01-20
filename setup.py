from distutils.core import setup
import imp
import os.path

path = os.path.join('feedparser', 'feedparser.py')
feedparser = imp.load_source('feedparser', path)

setup(
    name = 'feedparser',
    version = feedparser.__version__,
    description = 'Universal feed parser, handles RSS 0.9x, RSS 1.0, '
                  'RSS 2.0, CDF, Atom 0.3, and Atom 1.0 feeds',
    long_description = feedparser.__doc__.strip(),
    author = 'Mark Pilgrim',
    author_email = 'mark@diveintomark.org',
    url = 'http://feedparser.org/',
    download_url = 'http://code.google.com/p/feedparser/',
    platforms = ['POSIX', 'Windows'],
    package_dir = {'': 'feedparser'},
    py_modules = ['feedparser'],
    keywords = ['atom', 'cdf', 'feed', 'parser', 'rdf', 'rss'],
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.4',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Markup :: XML',
    ]
)
