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

"""
    App manage Alignak-App
"""

import os
import sys
from logging import getLogger

from alignak_app.core.notifier import AppNotifier

from alignak_app.core.utils import create_logger
from alignak_app.core.utils import get_image_path
from alignak_app.systray.tray_icon import TrayIcon

try:
    __import__('PyQt5')
    from PyQt5.QtWidgets import QApplication  # pylint: disable=no-name-in-module
    from PyQt5.QtGui import QIcon  # pylint: disable=no-name-in-module
except ImportError:
    from PyQt4.QtGui import QIcon  # pylint: disable=import-error
    from PyQt4.Qt import QApplication  # pylint: disable=import-error


logger = getLogger()

# noinspection PyTypeChecker
create_logger(logger)


class AlignakApp(object):
    """
        Class who build application and configuration.
    """

    def __init__(self):
        self.tray_icon = None
        self.notifier = None

    def build_alignak_app(self):
        """
        The main function of Alignak-App

        """

        # Create notifier
        self.notifier = AppNotifier(self.get_icon())

        # Create QSystemTrayIcon
        self.tray_icon = TrayIcon(self.get_icon())
        self.tray_icon.build_menu(self.notifier.backend)

    def run(self):  # pragma: no cover
        """
        Start the application.

        """

        if 'linux' in sys.platform or 'sunos5' in sys.platform:
            try:
                os.environ['DESKTOP_SESSION']
            except KeyError as e:
                logger.critical('You must be in desktop session to launch Alignak-App : ' + str(e))
                sys.exit()

        # Build app
        self.build_alignak_app()

        # Start process notifier
        self.notifier.start_process(self.tray_icon)

    @staticmethod
    def get_icon():
        """
        Set icon of application.

        """

        img = get_image_path('icon')
        icon = QIcon(img)

        return icon

if __name__ == "__main__":  # pragma: no cover
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    alignak_app = AlignakApp()
    alignak_app.run()
    alignak_app.tray_icon.show()

    sys.exit(app.exec_())
