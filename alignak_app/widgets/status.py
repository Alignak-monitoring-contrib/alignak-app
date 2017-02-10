#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015-2017:
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
from alignak_app.widgets.banner import send_banner
from alignak_app.widgets.app_widget import AppQWidget

try:
    __import__('PyQt5')
    from PyQt5.QtWidgets import QApplication, QWidget  # pylint: disable=no-name-in-module
    from PyQt5.QtWidgets import QGridLayout, QAction  # pylint: disable=no-name-in-module
    from PyQt5.QtWidgets import QLabel, QPushButton  # pylint: disable=no-name-in-module
    from PyQt5.QtGui import QIcon, QPixmap  # pylint: disable=no-name-in-module
    from PyQt5.QtCore import Qt, QTimer  # pylint: disable=no-name-in-module
except ImportError:  # pragma: no cover
    from PyQt4.Qt import QApplication, QWidget  # pylint: disable=import-error
    from PyQt4.Qt import QGridLayout, QAction  # pylint: disable=import-error
    from PyQt4.Qt import QLabel, QPushButton  # pylint: disable=import-error
    from PyQt4.QtGui import QIcon, QPixmap  # pylint: disable=import-error
    from PyQt4.QtCore import Qt, QTimer  # pylint: disable=import-error

logger = getLogger(__name__)


class AlignakStatus(QWidget):
    """
        Class who create QWidget for Daemons status.
    """

    daemons = [
        'poller',
        'receiver',
        'reactionner',
        'arbiter',
        'scheduler',
        'broker'
    ]

    def __init__(self, parent=None):
        super(AlignakStatus, self).__init__(parent)
        # General settings
        self.setWindowTitle(__application__)
        self.setToolTip('Alignak Status')
        self.setStyleSheet(get_css())
        # Fields
        self.app_backend = None
        self.daemons_labels = {}
        self.info = None
        self.old_bad_daemons = 0
        self.app_widget = AppQWidget()

    def create_status(self, app_backend):
        """
        Create grid layout for status QWidget

        """

        self.app_backend = app_backend

        # Add Layout
        layout = QGridLayout()
        self.setLayout(layout)

        self.create_daemons_labels(layout)

        # Default text and color
        self.info.setText('All daemons are alive.')
        self.info.setStyleSheet('color: #27ae60;')

        # Update status for first start
        self.check_status()

        # Start checks
        timer = QTimer(self)
        timer.start(60000)
        timer.timeout.connect(self.check_status)

        # Use AppQWidget
        self.app_widget.initialize('Alignak Status')
        self.app_widget.add_widget(self)

        self.show_states()

    def create_daemons_labels(self, layout):
        """
        Create QLabels and Pixmaps for each daemons

        """

        help_txt = QLabel('(Hover your mouse over each daemon to learn more)')
        help_txt.setObjectName('help')
        layout.addWidget(help_txt, 0, 0, 1, 2)
        layout.setAlignment(help_txt, Qt.AlignCenter)

        layout.addWidget(QLabel('<b>Daemon Name</b> '), 1, 0, 1, 1)
        status_title = QLabel('<b>Status</b>')
        status_title.setAlignment(Qt.AlignCenter)
        layout.addWidget(status_title, 1, 1, 1, 1)

        line = 2

        for daemon in self.daemons:
            # Initialize dict for each daemon category
            self.daemons_labels[daemon] = {
                'label': QLabel(daemon.capitalize() + 's'),
                'icon': QLabel(),
            }

            self.daemons_labels[daemon]['icon'].setAlignment(Qt.AlignCenter)
            self.daemons_labels[daemon]['icon'].setFixedSize(24, 24)
            self.daemons_labels[daemon]['icon'].setScaledContents(True)

            layout.addWidget(
                self.daemons_labels[daemon]['label'], line, 0
            )
            layout.addWidget(
                self.daemons_labels[daemon]['icon'], line, 1
            )
            line += 1

        self.info = QLabel()
        layout.addWidget(self.info, line, 0, 1, 2)
        layout.setAlignment(self.info, Qt.AlignCenter)
        line += 1

    def check_status(self):
        """
        Check daemons states, update icons and display banner if changes.

        """

        bad_daemons = 0
        total_daemons = 0
        arbiter_down = False

        daemon_msg = dict((element, '') for element in self.daemons)

        alignak_daemon = self.app_backend.get('alignakdaemon')
        for daemon in alignak_daemon['_items']:
            if not daemon['alive']:
                bad_daemons += 1
                daemon_msg[daemon['type']] += '<p>%s is not alive</p>' % daemon['name'].capitalize()
                if daemon == self.daemons[3]:
                    arbiter_down = True

            if not bad_daemons:
                self.daemons_labels[daemon['type']]['icon'].setPixmap(
                    QPixmap(get_image_path('valid'))
                )
                self.daemons_labels[daemon['type']]['icon'].setToolTip(
                    'All %ss are alive ' % daemon['type']
                )
                self.daemons_labels[daemon['type']]['label'].setToolTip(
                    'All %ss are alive ' % daemon['type']
                )
            else:
                self.daemons_labels[daemon['type']]['icon'].setPixmap(
                    QPixmap(get_image_path('unvalid'))
                )
                self.daemons_labels[daemon['type']]['icon'].setToolTip(
                    daemon_msg[daemon['type']]
                )
                self.daemons_labels[daemon['type']]['label'].setToolTip(
                    daemon_msg[daemon['type']]
                )

            total_daemons += 1

        if bad_daemons:
            self.info.setText('%d on %d daemons are down !' % (bad_daemons, total_daemons))
            self.info.setStyleSheet('color: #e74c3c;')

        if self.sender() and not isinstance(self.sender(), QAction):
            if not bad_daemons and (self.old_bad_daemons != 0):
                self.info.setText('All daemons are alive.')
                self.info.setStyleSheet('color: #27ae60;')
                send_banner('OK', 'All daemons are alive.')
                # Reset old bad daemons count
                self.old_bad_daemons = 0
            if bad_daemons:
                self.info.setText('%d on %d daemons are down !' % (bad_daemons, total_daemons))
                self.info.setStyleSheet('color: #e74c3c;')
                send_banner('WARN', '%d on %d daemons are down !' % (bad_daemons, total_daemons))

                if arbiter_down:
                    self.info.setText('Arbiter daemons are down !')
                    self.info.setStyleSheet('color: #e74c3c;')
                    send_banner('ALERT', 'Arbiter daemons are down !')

        self.old_bad_daemons = bad_daemons

    def show_states(self):
        """
        Show AlignakStatus

        """

        self.check_status()
        self.app_widget.show_widget()
