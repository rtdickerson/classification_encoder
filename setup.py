#!/usr/bin/env python
"""
Setup script for classification_encoder package.
"""

from setuptools import setup, find_packages
import os

# Read the README file for long description
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return ''

setup(
    name='classification-encoder',
    version='0.1.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='A Python library to encode/decode classification strings to/from unsigned 32-bit integers',
    long_description=read_readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/classification_encoder',
    packages=find_packages(where='lib'),
    package_dir={'': 'lib'},
    package_data={
        'classification_encoder': ['world.json'],
    },
    include_package_data=True,
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Security',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    keywords='classification security encoding bitmask',
    project_urls={
        'Bug Reports': 'https://github.com/yourusername/classification_encoder/issues',
        'Source': 'https://github.com/yourusername/classification_encoder',
    },
)
