#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
alignak-app-launcher command line interface::

    Usage:
        alignak-app-launcher [-h]
        alignak-app-launcher [-s][--start]
        alignak-app-launcher [-i][--install]

    Options:
        -h, --help          Show this screen.
        -s, --start         Start Alignak-app in your current shell. (All platforms)
        -i, --install       Check installation folders and files. (All platforms)
                            Install a daemon file and autocompletion. (Linux only)

    Daemon [alignak-app]:
        Option "--install" will create a bin folder in your "$HOME", with a daemon file based on
        the environment variables of your current session.

        Then simply run "alignak-app start" to launch application.

    Exit codes:
        0  if required operation succeeded

        22 if application detect an SSH session.
        64 if command line parameters are not used correctly

"""

import os

from docopt import docopt, DocoptExit

from alignak_app import __version__
from alignak_app.alignakapp import AlignakApp
from alignak_app.utils.installer import Installer


def main():  # pragma: no cover
    """
        Launch / install Alignak-app
    """

    # Get command line parameters
    args = None
    try:
        args = docopt(__doc__, version=__version__)
    except DocoptExit as exp:
        print("Command line parsing error:\n%s." % exp)
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("Exiting with error code: 64")
        exit(64)

    # Prepare installer
    installer = Installer()

    if args['--start']:
        if 'SSH_CONNECTION' in os.environ:
            print(
                'Alignak-app can\'t be launched during an SSH connection.'
            )
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print("Exiting with error code: 22")
            exit(22)

        # In case of, check installation
        installer.check_installation()

        # Start Alignak-app
        alignak_app = AlignakApp()
        alignak_app.start()
    if args['--install']:
        # Check installation and install folders and files
        installer.check_installation(mode='install')
        installer.install()


if __name__ == '__main__':  # pragma: no cover
    main()
