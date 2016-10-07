#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015-2016:
#   Matthieu Estrada, ttamalfor@gmail.com
#
# This file is part of (AlignakApp).
#
# (AlignakApp) is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# (AlignakApp) is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with (AlignakApp).  If not, see <http://www.gnu.org/licenses/>.

import sys
import os
import subprocess

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
    'configparser',
    'alignak_backend_client'
]

# Get HOME and USER
home = os.environ['HOME']
if 'root' in home or not home:
    sys.exit('Application can\'t find the user HOME or maybe you are connected as ROOT.')
if home.endswith('/'):
    home = home[:-1]
home += '/bin'

print('HOME = ' + home)

user = home.split('/')[2]

print('USER = ' + user)

# Define paths
paths = {}
if 'linux' in sys.platform or 'sunos5' in sys.platform:
    paths = {
        'etc': "/etc/alignak_app",
        'log': home + "alignak_app/logs",
        'bin': home,
    }
else:
    print("Unsupported platform, sorry!")
    exit(1)

from alignak_app import __description__, __version__, __license__
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
    description=__description__,
    long_description=open('README.rst').read(),

    zip_safe=False,

    packages=find_packages(),
    include_package_data=True,

    data_files = [
        (paths['etc'], ['etc/settings.cfg']),
        (paths['etc'] + '/images', ['etc/images/alignak.svg']),
        (paths['etc'] + '/images', ['etc/images/ok.svg']),
        (paths['etc'] + '/images', ['etc/images/warning.svg']),
        (paths['etc'] + '/images', ['etc/images/alert.svg']),
        (paths['etc'] + '/images', ['etc/images/error.svg']),
        (paths['etc'] + '/images', ['etc/images/host_up.svg']),
        (paths['etc'] + '/images', ['etc/images/host_down.svg']),
        (paths['etc'] + '/images', ['etc/images/host_unreach.svg']),
        (paths['etc'] + '/images', ['etc/images/service_ok.svg']),
        (paths['etc'] + '/images', ['etc/images/service_critical.svg']),
        (paths['etc'] + '/images', ['etc/images/service_warning.svg']),
        (paths['etc'] + '/images', ['etc/images/service_unknown.svg']),
        (paths['bin'], ['etc/bin/alignak-app']),
        (paths['bin'] + '/alignak_app', ['etc/bin/launch.py']),
    ],

    install_requires=install_requires,

    # entry_points={
    #     'gui_scripts': [
    #         'alignak_app = alignak_app.launch:launch',
    #     ],
    # },

    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: X11 Applications :: GTK',
        'Intended Audience :: Developers',
        'Intended Audience :: Customer Service',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: System :: Monitoring',
        'Topic :: System :: Systems Administration',
        'Topic :: Desktop Environment'
    ]

)

cmd = 'sudo chown -R ' + user + ':' + user + ' ~/bin'
try:
    subprocess.Popen(cmd,
        shell=True, stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
except Exception:
    print('ERROR : Alignak-app failed to give the necessary rights !')

