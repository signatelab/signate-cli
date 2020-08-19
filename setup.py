#!/usr/bin/python
#
# Copyright 2018 - 2020 SIGNATE Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from signate import info
import codecs
import sys

if sys.version_info[:2] < (3, 6):
    raise RuntimeError("Python version >= 3.6 required.")

CLI_REQUIRES = ['click', 'tabulate', 'wget']
SWAGGER_REQUIRES = ['urllib3 >= 1.25.3', 'six >= 1.10', 'certifi', 'python-dateutil']

setup(
    name='signate',
    version=info.VERSION,
    description=info.NAME,
    url='https://signate.jp',
    long_description=codecs.open('README.md', 'r', 'utf-8').read(),
    long_description_content_type='text/markdown',
    author='SIGNATE Inc.',
    keywords=['signate', 'signate-cli'],
    entry_points={'console_scripts': ['signate = signate.cli:main']},
    install_requires=CLI_REQUIRES + SWAGGER_REQUIRES,
    python_requires='>=3.6',
    packages=find_packages(exclude=['tests']),
    license='Apache 2.0')
