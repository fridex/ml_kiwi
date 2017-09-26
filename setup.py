#!/usr/bin/env python3

import sys
import os
from setuptools import setup


NAME = 'ml_kiwi'


def get_requirements():
    with open('requirements.txt') as fd:
        content = fd.read().splitlines()

    # Assuming deps are locked using pipenv
    return [line.split('==', 1)[0] for line in content]


def get_version():
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'ml_kiwi', '__init__.py')) as f:
        while True:
            line = f.readline()
            if line.startswith('__version__ = '):
                version = line[len('__version__ = ') + 1:-2]  # also remove quotes
                break
        else:
            raise ValueError("Cannot parse version information from main __init__.py")

    return version


if sys.version_info[0] != 3:
    sys.exit("Python3 is required in order to install %s" % NAME)

setup(
    name=NAME,
    version=get_version(),
    packages=[NAME],
    scripts=['ml-kiwi'],
    install_requires=get_requirements(),
    author='Fridolin Pokorny',
    author_email='fridolin.pokorny@gmail.com',
    maintainer='Fridolin Pokorny',
    maintainer_email='fridolin.pokorny@gmail.com',
    description='A lightweight implementation for kiwi.com machine learning weekend.',
    url='https://github.com/fridex/ml_kiwi',
    license='MIT',
    keywords='homework machine-learning fun',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy"
    ]
)
