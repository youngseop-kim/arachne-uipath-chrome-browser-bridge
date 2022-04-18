from setuptools import setup
from setuptools import find_packages

with open('readme.md', mode='r', encoding='utf-8') as fd:
    long_description = fd.read()

setup(
    name = 'cbnmplib',
    version = '1.0.11',
    license = 'MIT',
    description = 'chrome browser native messaging pipeline library',
    long_description = long_description,
    packages = find_packages(),
    classifiers = [
        'Programming Language :: Python :: 3', 
        'License :: OSI Approved :: MIT License', 
        'Operating System :: OS Independent'
        ],
    )