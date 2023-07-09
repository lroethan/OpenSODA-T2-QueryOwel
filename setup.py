#!/usr/bin/env python
import sys
from setuptools import setup

setup_requires = ['requests>2.18']
if sys.argv[-1] in ('sdist', 'bdist_wheel'):
    setup_requires.append('setuptools-markdown')


setup(
    name="ossowel",
    version="0.0.1",
    description="OpenDigger Command Line Tool",
    long_description_markdown_filename='README.md',
    author="Zhicheng Pan",
    author_email="panethan28@gmail.com",
    url="https://github.com/lroethan/OpenSODA-T2-QueryOwel",
    license="GPL",
    package_dir={'': 'src'},
    py_modules=['woel'],
    entry_points={
        'console_scripts': ['owel=owel:main'],
    },
    setup_requires=setup_requires,
    use_scm_version=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: SunOS/Solaris",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Utilities",
    ]
)