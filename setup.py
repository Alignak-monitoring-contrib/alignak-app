#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from importlib import import_module

try:
    from setuptools import setup, find_packages
except:
    sys.exit("Error: missing python-setuptools library")

try:
    python_version = sys.version_info
except:
    python_version = (1, 5)
if python_version < (2, 7):
    sys.exit("This application requires a minimum Python 2.7.x, sorry!")

package = import_module('alignak_app')

# Requirements
install_requires = [
    'future',
    'configparser'
]

paths = {}
# Define paths
if 'linux' in sys.platform or 'sunos5' in sys.platform:
    paths = {
        'bin':     "/usr/bin",
        'var':     "/var/lib/alignak_app/",
        'share':   "/var/lib/alignak_app/share",
        'etc':     "/etc/alignak_app",
        'run':     "/var/run/alignak_app",
        'log':     "/var/log/alignak_app",
        'libexec': "/var/lib/alignak_app/libexec",
    }
else:
    print("Unsupported platform, sorry!")
    exit(1)

from alignak_app import __application__, __version__, __copyright__
from alignak_app import __releasenotes__, __license__, __doc_url__
from alignak_app import __name__ as __pkg_name__



setup(
name=__pkg_name__,
    version=__version__,

    license=__license__,

    # metadata for upload to PyPI
    author="Estrada Matthieu",
    author_email="ttamalfor@gmail.com",
    keywords="alignak app indicator",
    url="https://github.com/Alignak-monitoring-contrib/alignak-app",
    description=package.__doc__.strip(),
    long_description=open('README.md').read(),

    zip_safe=False,

    packages=find_packages(),
    include_package_data=True,

    data_files = [
        (paths['etc'], ['etc/settings.cfg']),
        (paths['etc'] + '/images', ['etc/images/alignak.svg'])
    ],

    install_requires=install_requires,

    entry_points={
        'console_scripts': [
            'alignak_app = alignak_app.launch:launch',
        ],
    },

    classifiers = [
        'Development Status :: 2 - Beta',
        'Environment :: Desktop Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: Customer Service',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Topic :: System :: Monitoring',
        'Topic :: System :: Systems Administration'
    ]

)

