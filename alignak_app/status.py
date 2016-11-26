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

        if self.ws_request:
            alignak_map = self.ws_request.json()

            self.daemons_label['poller'] = {}
            self.daemons_label['receiver'] = {}
            self.daemons_label['reactionner'] = {}
            self.daemons_label['arbiter'] = {}
            self.daemons_label['scheduler'] = {}
            self.daemons_label['broker'] = {}

            for poller in alignak_map['poller']:
                self.daemons_label['poller'][poller] = {
                    'label': QLabel(poller),
                    'icon': QLabel()
                }
                self.daemons_label['poller'][poller]['label'].setObjectName(poller)
                if alignak_map['poller'][poller]['alive']:
                    self.daemons_label['poller'][poller]['icon'].setPixmap(
                        QPixmap(get_image_path('host_up'))
                    )
                else:
                    self.daemons_label['poller'][poller]['icon'].setPixmap(
                        QPixmap(get_image_path('host_down'))
                    )

            for receiver in alignak_map['receiver']:
                self.daemons_label['receiver'][receiver] = {
                    'label': QLabel(receiver),
                    'icon': QLabel()
                }
                self.daemons_label['receiver'][receiver]['label'].setObjectName(receiver)
                if alignak_map['receiver'][receiver]['alive']:
                    self.daemons_label['receiver'][receiver]['icon'].setPixmap(
                        QPixmap(get_image_path('host_up'))
                    )
                else:
                    self.daemons_label['receiver'][receiver]['icon'].setPixmap(
                        QPixmap(get_image_path('host_down'))
                    )

            for reactionner in alignak_map['reactionner']:
                self.daemons_label['reactionner'][reactionner] = {
                    'label': QLabel(reactionner),
                    'icon': QLabel()
                }
                self.daemons_label['reactionner'][reactionner]['label'].setObjectName(reactionner)
                if alignak_map['reactionner'][reactionner]['alive']:
                    self.daemons_label['reactionner'][reactionner]['icon'].setPixmap(
                        QPixmap(get_image_path('host_up'))
                    )
                else:
                    self.daemons_label['reactionner'][reactionner]['icon'].setPixmap(
                        QPixmap(get_image_path('host_down'))
                    )

            for arbiter in alignak_map['arbiter']:
                self.daemons_label['arbiter'][arbiter] = {
                    'label': QLabel(arbiter),
                    'icon': QLabel()
                }
                self.daemons_label['arbiter'][arbiter]['label'].setObjectName(arbiter)
                if alignak_map['arbiter'][arbiter]['alive']:
                    self.daemons_label['arbiter'][arbiter]['icon'].setPixmap(
                        QPixmap(get_image_path('host_up'))
                    )
                else:
                    self.daemons_label['arbiter'][arbiter]['icon'].setPixmap(
                        QPixmap(get_image_path('host_down'))
                    )

            for scheduler in alignak_map['scheduler']:
                self.daemons_label['scheduler'][scheduler] = {
                    'label': QLabel(scheduler),
                    'icon': QLabel()
                }
                self.daemons_label['scheduler'][scheduler]['label'].setObjectName(scheduler)
                if alignak_map['scheduler'][scheduler]['alive']:
                    self.daemons_label['scheduler'][scheduler]['icon'].setPixmap(
                        QPixmap(get_image_path('host_up'))
                    )
                else:
                    self.daemons_label['scheduler'][scheduler]['icon'].setPixmap(
                        QPixmap(get_image_path('host_down'))
                    )

            for broker in alignak_map['broker']:
                self.daemons_label['broker'][broker] = {
                    'label': QLabel(broker),
                    'icon': QLabel()
                }
                self.daemons_label['broker'][broker]['label'].setObjectName(broker)
                if alignak_map['broker'][broker]['alive']:
                    self.daemons_label['broker'][broker]['icon'].setPixmap(
                        QPixmap(get_image_path('host_up'))
                    )
                else:
                    self.daemons_label['broker'][broker]['icon'].setPixmap(
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
            for poller in alignak_map['poller']:
                self.grid.addWidget(
                    self.daemons_label['poller'][poller]['label'], line, 0
                )
                self.grid.addWidget(
                    self.daemons_label['poller'][poller]['icon'], line, 1
                )
                line += 1

            for receiver in alignak_map['receiver']:
                self.grid.addWidget(
                    self.daemons_label['receiver'][receiver]['label'], line, 0
                )
                self.grid.addWidget(
                    self.daemons_label['receiver'][receiver]['icon'], line, 1
                )
                line += 1

            for reactionner in alignak_map['reactionner']:
                self.grid.addWidget(
                    self.daemons_label['reactionner'][reactionner]['label'], line, 0
                )
                self.grid.addWidget(
                    self.daemons_label['reactionner'][reactionner]['icon'], line, 1
                )
                line += 1

            for arbiter in alignak_map['arbiter']:
                self.grid.addWidget(
                    self.daemons_label['arbiter'][arbiter]['label'], line, 0
                )
                self.grid.addWidget(
                    self.daemons_label['arbiter'][arbiter]['icon'], line, 1
                )
                line += 1

            for scheduler in alignak_map['scheduler']:
                self.grid.addWidget(
                    self.daemons_label['scheduler'][scheduler]['label'], line, 0
                )
                self.grid.addWidget(
                    self.daemons_label['scheduler'][scheduler]['icon'], line, 1
                )
                line += 1

            for broker in alignak_map['broker']:
                self.grid.addWidget(
                    self.daemons_label['broker'][broker]['label'], line, 0
                )
                self.grid.addWidget(
                    self.daemons_label['broker'][broker]['icon'], line, 1
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
