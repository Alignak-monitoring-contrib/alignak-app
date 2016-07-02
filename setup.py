#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

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

# Requirements
install_requires = [
    'future',
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

import alignak_app

setup(
    # Library Name
    name='alignak_app',

    # Version
    version=alignak_app.__version__,

    # Packages :
    # Found recursively all in 'alignak_app' folder
    packages=find_packages(),
    install_requires=install_requires,

    data_files=[
        (paths['etc'], ['etc/settings.cfg'])
    ],

    # Author
    author="Estrada Matthieu",
    author_email="ttamalfor@gmail.com",

    # Description
    description="AppIndicator for Alignak",
    long_description=open('README.md').read(),

    include_package_data=True,

    url='https://github.com/Alignak-monitoring-contrib/alignak-app',

    classifiers=[
        'Development Status :: 2 - Beta',
        'Environment :: Desktop',
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

