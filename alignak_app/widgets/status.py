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
    Status manage QWidget who display Alignak Daemons status.
"""

from logging import getLogger

import requests

from alignak_app import __application__
from alignak_app.core.utils import get_image_path, get_app_config, get_css
from alignak_app.widgets.title import get_widget_title

try:
    __import__('PyQt5')
    from PyQt5.QtWidgets import QApplication, QWidget  # pylint: disable=no-name-in-module
    from PyQt5.QtWidgets import QGridLayout  # pylint: disable=no-name-in-module
    from PyQt5.QtWidgets import QLabel, QPushButton  # pylint: disable=no-name-in-module
    from PyQt5.QtGui import QIcon, QPixmap  # pylint: disable=no-name-in-module
    from PyQt5.QtCore import Qt  # pylint: disable=no-name-in-module
except ImportError:  # pragma: no cover
    from PyQt4.Qt import QApplication, QWidget  # pylint: disable=import-error
    from PyQt4.Qt import QGridLayout  # pylint: disable=import-error
    from PyQt4.Qt import QLabel, QPushButton  # pylint: disable=import-error
    from PyQt4.QtGui import QIcon, QPixmap  # pylint: disable=import-error
    from PyQt4.QtCore import Qt  # pylint: disable=import-error

logger = getLogger(__name__)


class AlignakStatus(QWidget):
    """
        Class who create QWidget for Daemons status.
    """

    def __init__(self, parent=None):
        super(AlignakStatus, self).__init__(parent)
        # General settings
        self.setWindowTitle(__application__)
        self.setWindowIcon(QIcon(get_image_path('icon')))
        self.setToolTip('Daemons Status')
        # Fields
        self.daemons = [
            'poller',
            'receiver',
            'reactionner',
            'arbiter',
            'scheduler',
            'broker'
        ]
        self.ws_request = None
        self.daemons_labels = {}
        self.setStyleSheet(get_css())

    def center(self):
        """
        Center QWidget

        """

        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        center = QApplication.desktop().screenGeometry(screen).center()
        self.move(center.x() - (self.width() / 2), center.y() - (self.height() / 2))

    def show_at_start(self):
        """
        Show AlignakStatus on start

        """

        self.alignak_ws_request()

        if get_app_config('Backend', 'web_service', boolean=True) and self.ws_request:
            self.center()
            self.show()

    def create_status(self):
        """
        Create grid layout for status QWidget

        """

        # Add Layout
        layout = QGridLayout()
        self.setLayout(layout)

        # Display daemons status or info windows
        if get_app_config('Backend', 'web_service', boolean=True):
            self.alignak_ws_request()
            if self.ws_request:

                self.create_daemons_labels()
                self.daemons_to_layout(layout)
            else:
                self.web_service_info(layout)

        self.show_at_start()

    def alignak_ws_request(self):
        """
        Request to get json data from alignak web service

        """

        try:
            self.ws_request = requests.get(
                get_app_config('Backend', 'alignak_ws') + '/alignak_map'
            )
        except requests.ConnectionError as e:
            logger.error('Bad value in "web_service_url" option : ' + str(e))

    def create_daemons_labels(self):
        """
        Create QLabels and Pixmaps for each daemons

        """

        for daemon in self.daemons:
            # Initialize daemon category dict
            self.daemons_labels[daemon] = {}

            # Get json data from Web_service
            alignak_map = self.ws_request.json()

            # Create QLabel and Pixmap for each sub_daemon
            for sub_daemon in alignak_map[daemon]:
                self.daemons_labels[daemon][sub_daemon] = {
                    'label': QLabel(sub_daemon),
                    'icon': QLabel()
                }

                logger.debug(
                    'Daemon ' +
                    str(sub_daemon) +
                    ' is alive: ' +
                    str(alignak_map[daemon][sub_daemon]['alive'])
                )

                self.daemons_labels[daemon][sub_daemon]['label'].setObjectName(sub_daemon)
                self.daemons_labels[daemon][sub_daemon]['icon'].setAlignment(Qt.AlignCenter)
                self.daemons_labels[daemon][sub_daemon]['icon'].setFixedSize(24, 24)
                self.daemons_labels[daemon][sub_daemon]['icon'].setScaledContents(True)

                if alignak_map[daemon][sub_daemon]['alive']:
                    self.daemons_labels[daemon][sub_daemon]['icon'].setPixmap(
                        QPixmap(get_image_path('valid'))
                    )
                else:
                    self.daemons_labels[daemon][sub_daemon]['icon'].setPixmap(
                        QPixmap(get_image_path('unvalid'))
                    )

    def add_button(self, pos, layout):
        """
        Add a button

        """

        button = QPushButton(self)
        button.setIcon(QIcon(get_image_path('checked')))
        button.setObjectName('valid')
        button.setFixedSize(30, 30)

        button.clicked.connect(self.close)
        layout.addWidget(button, pos, 0, 1, 2)
        layout.setAlignment(button, Qt.AlignCenter)

    def web_service_info(self, layout):
        """
        Display information text if "web_service" is not configured

        """

        title = get_widget_title(
            'alignak status',
            self
        )
        layout.addWidget(title, 0, 0)

        info_title_label = QLabel(
            '<br><span style="color: blue;">Alignak <b>Web Service</b> is not available !</span>'
        )
        layout.addWidget(info_title_label, 1, 0)

        info_label = QLabel(
            'Install it on your <b>Alignak server</b>. '
            'And configure the <b>settings.cfg</b> accordingly in <b>Alignak-app</b>.'
        )
        info_label.setWordWrap(True)
        info_label.setAlignment(Qt.AlignTop)

        layout.addWidget(info_label, 2, 0)
        self.add_button(3, layout)

    def daemons_to_layout(self, layout):
        """
        Add all daemons label to layout

        """

        title = get_widget_title(
            'alignak status',
            self
        )
        layout.addWidget(title, 0, 0, 1, 2)
        layout.setAlignment(Qt.AlignCenter)

        if self.ws_request:
            layout.addWidget(QLabel('<b>Daemon Name</b> '), 1, 0, 1, 1)

            status_title = QLabel('<b>Status</b>')
            status_title.setAlignment(Qt.AlignCenter)
            layout.addWidget(status_title, 1, 1, 1, 1)

            alignak_map = self.ws_request.json()

            line = 2
            for daemon in self.daemons:
                for sub_daemon in alignak_map[daemon]:
                    layout.addWidget(
                        self.daemons_labels[daemon][sub_daemon]['label'], line, 0
                    )
                    layout.addWidget(
                        self.daemons_labels[daemon][sub_daemon]['icon'], line, 1
                    )
                    line += 1
        self.add_button(line, layout)

    def update_status(self):
        """
        Check daemons states and update icons

        """

        # New request
        self.alignak_ws_request()

        for daemon in self.daemons:
            alignak_map = self.ws_request.json()

            # Update daemons QPixmap for each sub_daemon
            for sub_daemon in alignak_map[daemon]:
                if alignak_map[daemon][sub_daemon]['alive']:
                    self.daemons_labels[daemon][sub_daemon]['icon'].setPixmap(
                        QPixmap(get_image_path('valid'))
                    )
                else:
                    self.daemons_labels[daemon][sub_daemon]['icon'].setPixmap(
                        QPixmap(get_image_path('unvalid'))
                    )

    def show_states(self):
        """
        Show AlignakStatus

        """

        if get_app_config('Backend', 'web_service', boolean=True) and self.ws_request:
            self.update_status()
        else:
            self.web_service_info(self.layout())

        self.center()
        self.show()
