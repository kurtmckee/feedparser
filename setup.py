from setuptools import setup

setup(
    name = 'feedparser',
    version = '5.2.1',
    description = 'Universal feed parser, handles RSS 0.9x, RSS 1.0, '
                  'RSS 2.0, CDF, Atom 0.3, and Atom 1.0 feeds',
    author = 'Kurt McKee',
    author_email = 'contactme@kurtmckee.org',
    url = 'https://github.com/kurtmckee/feedparser',
    download_url = 'https://pypi.python.org/pypi/feedparser',
    platforms = ['POSIX', 'Windows'],
    packages = ['feedparser', 'feedparser.datetimes', 'feedparser.namespaces', 'feedparser.parsers'],
    install_requires = [
        'sgmllib3k;python_version>="3.0"',
        'python-dateutil;python_version>="3.0"',
    ],
    keywords = ['atom', 'cdf', 'feed', 'parser', 'rdf', 'rss'],
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Markup :: XML',
    ],
)
