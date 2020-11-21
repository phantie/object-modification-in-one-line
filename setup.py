"""Build with
   > py setup.py sdist"""

from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name = 'take',
    version = '1.0',
    packages = find_packages(),
    long_description = open(join(dirname(__file__), 'README.md')).read(),
)