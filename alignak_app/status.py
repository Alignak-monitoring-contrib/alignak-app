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
    from PyQt5.QtGui import QIcon  # pylint: disable=no-name-in-module
except ImportError:  # pragma: no cover
    from PyQt4.Qt import QApplication, QWidget  # pylint: disable=import-error
    from PyQt4.Qt import QGridLayout  # pylint: disable=import-error
    from PyQt4.Qt import QLabel  # pylint: disable=import-error
    from PyQt4.QtGui import QIcon  # pylint: disable=import-error

logger = getLogger(__name__)


class AlignakStatus(QWidget):
    """
    Class who create QWidget for Alignak status..
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

    def create_status(self):
        """

        :return:
        """
        self.grid = QGridLayout()
        self.grid.addWidget(QLabel('Daemon Name '), 1, 0)
        self.grid.addWidget(QLabel('Status'), 1, 1)

        self.setLayout(self.grid)

    def web_service_data(self):
        """
        Get web service data and add to layout

        :param grid: QGridLayout
        :type grid: QGridLayout
        """

        req = requests.get(get_app_config().get('Backend', 'web_service') + '/alignak_map')
        alignak_map = req.json()

        line = 2
        for poller in alignak_map['poller']:
            self.grid.addWidget(QLabel(poller), line, 0)
            self.grid.addWidget(QLabel(str(alignak_map['poller'][poller]['alive'])), line, 1)
            line += 1

        for receiver in alignak_map['receiver']:
            self.grid.addWidget(QLabel(receiver), line, 0)
            self.grid.addWidget(QLabel(str(alignak_map['receiver'][receiver]['alive'])), line, 1)
            line += 1

        for reactionner in alignak_map['reactionner']:
            self.grid.addWidget(QLabel(reactionner), line, 0)
            self.grid.addWidget(QLabel(str(alignak_map['reactionner'][reactionner]['alive'])), line, 1)
            line += 1

        for arbiter in alignak_map['arbiter']:
            self.grid.addWidget(QLabel(arbiter), line, 0)
            self.grid.addWidget(QLabel(str(alignak_map['arbiter'][arbiter]['alive'])), line, 1)
            line += 1

        for scheduler in alignak_map['scheduler']:
            self.grid.addWidget(QLabel(scheduler), line, 0)
            self.grid.addWidget(QLabel(str(alignak_map['scheduler'][scheduler]['alive'])), line, 1)
            line += 1

        for broker in alignak_map['broker']:
            self.grid.addWidget(QLabel(broker), line, 0)
            self.grid.addWidget(QLabel(str(alignak_map['broker'][broker]['alive'])), line, 1)
            line += 1

    def show_states(self):
        """
        Show AlignakStatus

        """

        self.web_service_data()

        self.show()
