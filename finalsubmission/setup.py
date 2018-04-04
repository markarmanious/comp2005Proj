"""Stolen from Dr. Brown.The setup file for the 2005 group project
"""

from setuptools import setup, find_packages
setup(
    name="flaskr",
    version="0.1",
    packages=['flaskr', 'flaskr/flaskr'],

    # Check that a package for install is available from PyPI
    install_requires=['flask>=0.12'], # PyPI package

    package_data={
        # If any package contains *.txt or *.pdf files, include them:
        '': ['*.txt', '*.pdf', '*.sql', '*.css', '*.db', '.html'],
        # And everything in the test, doc, static and jinja folders:
        'flaskr': ['flaskr/docs/*', 'flaskr/templates/*', 'flaskr/tests/*', 'flaskr/static/*'],
#		'flaskr/flaskr': [],
#		'flaskr/flaskr': ['docs/*', 'templates/*', 'tests/*', 'static/*'],
    },

    # metadata for upload to PyPI
    author="Our Groups",
    author_email="d99jdp@mun.ca",
    description="This is the groups project for 2005",
    license="COMP2005 students", # this is incorrect usage
    keywords="flask",
    url="http://www.cs.mun.ca/~brown/2005",   # project home page, if any

    # could also include project_urls, long_description, download_url, classifiers, etc.

    # setup_requires=['pytest-runner',], # suggested from flaskr tutorial - but not needed
    # tests_require=['pytest',], # suggested from flaskr tutorial - but not needed
)


