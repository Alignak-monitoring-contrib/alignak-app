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

import sys
import os
import configparser as cfg

from logging import getLogger

from alignak_app.menu import AppIcon
from alignak_app.notifier import AppNotifier
from alignak_app.utils import get_alignak_home

from PyQt5.QtWidgets import QApplication  # pylint: disable=no-name-in-module
from PyQt5.QtGui import QIcon  # pylint: disable=no-name-in-module


logger = getLogger(__name__)


class AlignakApp(object):
    """
        Class who build application and configuration.
    """

    def __init__(self):
        self.app = None
        self.config = None
        self.app_icon = None
        self.alignak_data = None

    def main(self):
        """
        The main function of Alignak-App

        """

        # Create app
        self.app = QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(False)

        # Init. configuration
        self.read_configuration()

        # Create QSystemTrayIcon
        icon = self.set_icon()
        self.app_icon = AppIcon(icon, self.config)
        self.app_icon.build_menu()

        # Create process notifier
        notifier = AppNotifier(icon)
        notifier.start_process(self.config)

        # Show app and run exec
        self.app_icon.show()
        sys.exit(self.app.exec_())

    def read_configuration(self):  # pragma: no cover
        """
        Read the configuration file.

        """

        config_file = get_alignak_home() + '/alignak_app/settings.cfg'

        self.config = cfg.ConfigParser()
        logger.info('Read configuration file...')

        if os.path.isfile(config_file):
            self.config.read(config_file)
            logger.info('Configuration file is OK.')
        else:
            logger.error('Configuration file is missing in [' + config_file + '] !')
            sys.exit('Configuration file is missing in [' + config_file + '] !')

    def set_icon(self):
        """
        Set icon of application.

        """
        qicon_path = get_alignak_home() \
            + self.config.get('Config', 'path') \
            + self.config.get('Config', 'img') \
            + '/'
        img = os.path.abspath(qicon_path + self.config.get('Config', 'icon'))
        icon = QIcon(img)

        return icon

if __name__ == '__main__':
    AlignakApp().main()
