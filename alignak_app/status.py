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
    Status manage QWidget who display Alignak status.
"""

from logging import getLogger

import requests

from alignak_app import __application__
from alignak_app.utils import get_image_path, get_app_config

try:
    __import__('PyQt5')
    from PyQt5.QtWidgets import QApplication, QWidget  # pylint: disable=no-name-in-module
    from PyQt5.QtWidgets import QGridLayout  # pylint: disable=no-name-in-module
    from PyQt5.QtWidgets import QLabel  # pylint: disable=no-name-in-module
    from PyQt5.QtGui import QIcon, QPixmap  # pylint: disable=no-name-in-module
except ImportError:  # pragma: no cover
    from PyQt4.Qt import QApplication, QWidget  # pylint: disable=import-error
    from PyQt4.Qt import QGridLayout  # pylint: disable=import-error
    from PyQt4.Qt import QLabel  # pylint: disable=import-error
    from PyQt4.QtGui import QIcon, QPixmap  # pylint: disable=import-error

logger = getLogger(__name__)


class AlignakStatus(QWidget):
    """
        Class who create QWidget for Alignak status.
    """

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        # General settings
        self.setWindowTitle(__application__ + ': Alignak-States')
        self.setContentsMargins(0, 0, 0, 0)
        self.setMinimumSize(425, 270)
        self.setMaximumSize(425, 270)
        self.setWindowIcon(QIcon(get_image_path('icon')))
        self.move(QApplication.desktop().screen().rect().center() - self.rect().center())
        # Fields
        self.grid = None
        self.start = True
        self.daemons = [
            'poller',
            'receiver',
            'reactionner',
            'arbiter',
            'scheduler',
            'broker'
        ]
        self.ws_request = None
        self.daemons_label = {}

    def show_at_start(self):
        """
        Show AlignakStatus on start

        """
        if self.start:
            self.show()
        else:
            self.start = False

    def create_status(self):
        """
        Create grid layout for status QWidget

        """

        self.grid = QGridLayout()

        self.setLayout(self.grid)

        self.alignak_ws_request()
        self.create_daemons_labels()

        self.web_service_data()
        self.show_at_start()

    def alignak_ws_request(self):
        """

        :return:
        """

        try:
            self.ws_request = requests.get(
                get_app_config('Backend', 'web_service') + '/alignak_map'
            )
        except TypeError as e:
            logger.error('Bad value in "web_service" option : ' + str(e))

    def create_daemons_labels(self):
        """
        Create QLabels and Pixmaps for each daemons

        """

        for daemon in self.daemons:
            # Initialize daemon category dict
            self.daemons_label[daemon] = {}

            # Get json data from Web_service
            alignak_map = self.ws_request.json()

            # Create QLabel and Pixmap for each sub_daemon
            for sub_daemon in alignak_map[daemon]:
                self.daemons_label[daemon][sub_daemon] = {
                    'label': QLabel(sub_daemon),
                    'icon': QLabel()
                }
                self.daemons_label[daemon][sub_daemon]['label'].setObjectName(sub_daemon)
                if alignak_map[daemon][sub_daemon]['alive']:
                    self.daemons_label[daemon][sub_daemon]['icon'].setPixmap(
                        QPixmap(get_image_path('host_up'))
                    )
                else:
                    self.daemons_label[daemon][sub_daemon]['icon'].setPixmap(
                        QPixmap(get_image_path('host_down'))
                    )

    def web_service_data(self):
        """
        Get web service data and add to layout

        """

        self.grid.addWidget(QLabel('Daemon Name '), 1, 0)
        self.grid.addWidget(QLabel('Status'), 1, 1)

        if self.ws_request:
            alignak_map = self.ws_request.json()

            for d in self.daemons_label:
                logger.debug(self.daemons_label[d])

            line = 2
            for daemon in self.daemons:
                for sub_daemon in alignak_map[daemon]:
                    self.grid.addWidget(
                        self.daemons_label[daemon][sub_daemon]['label'], line, 0
                    )
                    self.grid.addWidget(
                        self.daemons_label[daemon][sub_daemon]['icon'], line, 1
                    )
                    line += 1
        else:
            self.grid.addWidget(QLabel('Alignak Web Service not available !'), 2, 0)
            self.grid.addWidget(QLabel('N/A'), 2, 1)

    def show_states(self):
        """
        Show AlignakStatus

        """

        self.web_service_data()

        self.show()
