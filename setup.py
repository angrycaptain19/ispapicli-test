#!/usr/bin/env python

import os
import io
import re
from setuptools import setup, find_packages


def read(*names, **kwargs):
    with io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf8")
    ) as fp:
        return fp.read()


def find_version(root_path):
    version = ""
    with open(os.path.join(root_path, 'VERSION')) as version_file:
        version = version_file.read().strip()

    if len(version) > 1:
        return version
    raise RuntimeError("Unable to find version string.")


with open("README.md", "r") as fh:
    long_description = fh.read()

PACKAGE = 'hexonet.ispapicli'
VERSION = find_version(os.path.dirname(__file__))

setup(
    name=PACKAGE,
    version=VERSION,
    description=PACKAGE + ' is a command line client library for the insanely fast HEXONET Backend API',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Rashad Jamara',
    author_email='rjamara@hexonet.net',
    maintainer='Rashad Jamara',
    maintainer_email='rjamara@hexonet.net',
    url='https://github.com/hexonet/ispapicli/',
    install_requires=[
        'altgraph==0.17',
        'autopep8==1.5.5',
        'beautifulsoup4==4.9.3',
        'certifi==2020.12.5',
        'chardet==4.0.0',
        'hexonet.apiconnector==3.8.2',
        'idna>=2.5,<4',
        'numpy==1.20.1',
        'pep8==1.7.1',
        'Pillow==8.1.0',
        'pycodestyle==2.6.0',
        'PyQt5==5.15.2',
        'PyQt5-sip==12.8.1',
        'requests==2.25.1',
        'soupsieve==2.2',
        'tabulate==0.8.9',
        'urllib3==1.26.3',
        'twine==3.3.0'
    ],
    setup_requires=[
        'pytest-runner'
    ],
    tests_require=[
        'pytest',
        'pytest-cov'
    ],
    license="MIT",
    scripts=[],
    zip_safe=True,
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ),
    namespace_packages=['hexonet'],
    packages=find_packages(),
    python_requires='>=3.6',
    package_data={
        '': ['*.json', '*.png']
    },
    entry_points=dict(
        console_scripts=['gui=hexonet.ispapicli.ispapicli:startGUI']
    )
)
