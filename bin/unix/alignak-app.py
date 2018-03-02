#!/usr/bin/env python3
# -*- codinf: utf-8 -*-

# Copyright (c) 2015-2018:
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

"""
    Alignak App
    +++++++++++
    Alignak App launch or install Alignak-app
"""

import sys
import os

import argparse

from alignak_app.utils.installer import Installer

from alignak_app import __application__


def main():  # pragma: no cover
    """
        Launch or install Alignak-app
    """

    usage = u"./alignak-app.py [--start | --install]"
    if 'win32' not in sys.platform:
        description = u'Launch %s in shell or install as daemon.' % __application__
    else:
        description = u'Launch %s in shell.' % __application__

    # Init parser
    parser = argparse.ArgumentParser(
        usage=usage,
        description=description
    )

    parser.add_argument(
        '-s', '--start',
        help='Start %s in your shell.' % __application__,
        dest='start', action="store_true", default=False
    )

    args = parser.parse_args()

    installer = Installer()
    installer.check_installation()
    installer.install()

    if args.start:
        from alignak_app.app import AlignakApp

        if 'SSH_CONNECTION' in os.environ:
            fail = '\033[91m'
            endc = '\033[0m'

            sys.exit(
                '%sAlignak-app can not be launched during an SSH connection '
                'and requires an X server to be displayed.%s' % (fail, endc)
            )

        alignak_app = AlignakApp()
        alignak_app.start()
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
