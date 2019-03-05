#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Setup for activate-aiida."""

import io
from importlib import import_module
from setuptools import setup, find_packages

with io.open('README.md') as readme:
    readme_content = readme.read()

setup(
    name='activate-aiida',
    version=import_module("activate_aiida").__version__,
    description=(
        'a package to activate an aiida environment, from a yaml config file'
    ),
    long_description=readme_content,
    long_description_content_type='text/markdown',
    install_requires=[
        "ruamel.yaml",
        "jsonschema"
    ],
    license='MIT',
    author='Chris Sewell',
    author_email='chrisj_sewell@hotmail.com',
    url='https://github.com/chrisjsewell/activate_aiida',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OSX',
        'Operating System :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Scientific/Engineering :: Chemistry',
        'Topic :: Scientific/Engineering :: Physics',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
    keywords='aiida, yaml, configuration',
    zip_safe=True,
    packages=find_packages(),
    package_data={},
    scripts=[
        "bin/activate-aiida",
        "bin/deactivate-aiida"
    ],
    entry_points={
        'console_scripts': [
            'read-aiida-args = activate_aiida.parse_args:run',
            'read-aiida-config = activate_aiida.read_config:run'
        ]
    }
)
