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
    App Synthesis manage widget for Synthesis QWidget.
"""

from logging import getLogger

from alignak_app.core.utils import get_image_path
from alignak_app.core.utils import get_diff_since_last_check

try:
    __import__('PyQt5')
    from PyQt5.QtWidgets import QPushButton, QMessageBox  # pylint: disable=no-name-in-module
    from PyQt5.QtWidgets import QWidget, QVBoxLayout  # pylint: disable=no-name-in-module
    from PyQt5.QtWidgets import QGridLayout, QLabel  # pylint: disable=no-name-in-module
    from PyQt5.Qt import QPixmap, Qt, QIcon  # pylint: disable=no-name-in-module
    from PyQt5.QtCore import QTimer  # pylint: disable=no-name-in-module
except ImportError:  # pragma: no cover
    from PyQt4.Qt import QPushButton, QMessageBox  # pylint: disable=import-error
    from PyQt4.Qt import QWidget, QVBoxLayout  # pylint: disable=import-error
    from PyQt4.Qt import QGridLayout, QLabel  # pylint: disable=import-error
    from PyQt4.Qt import QPixmap, Qt, QIcon  # pylint: disable=import-error
    from PyQt4.QtCore import QTimer  # pylint: disable=import-error


logger = getLogger(__name__)


class HostView(QWidget):
    """
        Class who create the Host View QWidget.
    """

    def __init__(self, parent=None):
        super(HostView, self).__init__(parent)
        self.setFixedHeight(150)
        self.setMinimumWidth(parent.width())
        self.setToolTip('Host View')
        # Fields
        self.ack_button = None
        self.down_button = None
        self.layout = None
        self.labels = {}
        self.host = None
        self.app_backend = None
        self.endpoints = {
            'actionacknowledge': {},
            'actiondowntime': {}
        }

    def init_view(self, app_backend):
        """
        Init Host View with default values.

        """

        logger.info('Initialize Host View...')

        self.app_backend = app_backend

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        # Creates the labels that will be updated
        self.labels = {
            'name': QLabel('<h3>Host Name</h3>'),
            'state_icon': QLabel(),
            'real_state_icon': QLabel(),
            'last_check': QLabel('N/A'),
            'output': QLabel('N/A')
        }

        # Adjust icons and set default icons
        self.labels['state_icon'].setFixedSize(64, 64)
        self.labels['state_icon'].setPixmap(self.get_host_icon(''))
        self.labels['real_state_icon'].setFixedSize(32, 32)
        self.labels['real_state_icon'].setScaledContents(True)
        self.labels['real_state_icon'].setPixmap(self.get_host_icon(''))

        # row, column, rowSpan, colSPan
        self.layout.addWidget(self.labels['state_icon'], 0, 0, 2, 1)
        self.layout.addWidget(self.labels['name'], 2, 0, 1, 1)

        real_state_text = QLabel('Host real state, excluding services')
        real_state_text.setWordWrap(True)
        self.layout.addWidget(real_state_text, 0, 1, 1, 1)
        self.layout.addWidget(self.labels['real_state_icon'], 1, 1, 2, 1)

        check_label = QLabel('<b>My last Check</b>')
        self.layout.addWidget(check_label, 0, 2, 1, 2)
        self.layout.setAlignment(check_label, Qt.AlignTrailing)
        last_check = QLabel('<b>Last check:</b>')
        self.layout.addWidget(last_check, 1, 2, 1, 1)
        self.layout.setAlignment(last_check, Qt.AlignTrailing)
        self.layout.addWidget(self.labels['last_check'], 1, 3, 1, 1)
        output = QLabel('<b>Output:</b>')
        self.layout.addWidget(output, 2, 2, 1, 1)
        self.layout.setAlignment(output, Qt.AlignTrailing)
        self.layout.addWidget(self.labels['output'], 2, 3, 1, 1)

        buttons = self.action_buttons()
        self.layout.addWidget(buttons, 1, 4, 1, 2)

    def action_buttons(self):
        """
        Create ack and downtime buttons

        :return: QWidget with buttons
        :rtype: QWidget
        """

        button_widget = QWidget()
        layout = QVBoxLayout()
        button_widget.setLayout(layout)

        self.ack_button = QPushButton('Acknowledge this problem')
        self.ack_button.setToolTip('Acknowledge this problem')
        self.ack_button.setIcon(QIcon(get_image_path('acknowledged')))
        self.ack_button.setObjectName('actionacknowledge')
        self.ack_button.clicked.connect(self.action)

        self.down_button = QPushButton('Schedule a downtime')
        self.down_button.setToolTip('Schedule a downtime')
        self.down_button.setIcon(QIcon(get_image_path('downtime')))
        self.down_button.setObjectName('actiondowntime')
        self.down_button.clicked.connect(self.action)

        layout.addWidget(self.ack_button, 0)
        layout.addWidget(self.down_button, 1)

        return button_widget

    def action(self):  # pragma: no cover
        """
        Handle action for "ack_button" and "down_button"

        """

        # Which button is caller
        # objectname can be 'actionacknowledge' or 'actiondowntime'
        sender = self.sender()

        user = self.app_backend.get_user()

        if self.host:

            data = {
                'action': 'add',
                'host': self.host['_id'],
                'service': None,
                'user': user['_id'],
                'comment': 'comment'
            }

            action = self.app_backend.post(sender.objectName(), data)

            if action['_status'] == 'OK':
                # Init timer
                ack_timer = QTimer(self)

                # If endpoints is not store, add it
                if self.host['_id'] not in self.endpoints[sender.objectName()]:
                    self.endpoints[sender.objectName()][self.host['_id']] = \
                        action['_links']['self']['href']

                # Update buttons
                if 'actiondowntime' in sender.objectName():
                    self.down_button.setEnabled(False)
                    self.down_button.setText('Waiting from backend...')
                    ack_timer.singleShot(17000, self.check_downtime_done)
                else:
                    self.ack_button.setEnabled(False)
                    self.ack_button.setText('Waiting from backend...')
                    ack_timer.singleShot(17000, self.check_ack_done)
            else:
                logger.error('Action failed...')

    def check_ack_done(self):
        """
        Check if acknowledge is done.

        """

        ack_response = self.app_backend.backend.get(
            self.endpoints['actionacknowledge'][self.host['_id']]
        )

        if ack_response['processed']:
            QMessageBox.information(
                self,
                'Acknowledge',
                "Acknowledged on " + self.host['name'] + " is done !",
                QMessageBox.Ok
            )
        else:
            logger.error('Acknowledge failed: ' + str(ack_response))

    def check_downtime_done(self):
        """
        Check if downtime scheduled is done

        """

        down_response = self.app_backend.backend.get(
            self.endpoints['actiondowntime'][self.host['_id']]
        )

        if down_response['processed']:
            QMessageBox.information(
                self,
                'Downtime' + self.host['name'],
                "Schedule a downtime on " + self.host['name'] + " is done !",
                QMessageBox.Ok
            )
        else:
            logger.error('Downtime failed: ' + str(down_response))

    def update_view(self, host):
        """
        Update Host view with desired host.

        :param host: host data from app_backend
        :type host: dict
        """

        self.host = host

        logger.info('Update Host View...')
        logger.debug('Host: ' + host['name'] + ' is ' + host['ls_state'])

        if isinstance(host['ls_last_check'], int):
            time_delta = get_diff_since_last_check(host['ls_last_check'])
        else:
            time_delta = 'NOT FOUND'

        self.labels['name'].setText('<h3>' + host['name'].title() + '</h3>')
        self.labels['state_icon'].setPixmap(self.get_host_icon(host['ls_state']))
        self.labels['real_state_icon'].setPixmap(self.get_host_icon(''))
        self.labels['last_check'].setText(str(time_delta))
        self.labels['output'].setText(host['ls_output'])

    @staticmethod
    def get_host_icon(state):
        """
        Return QPixmap with the icon corresponding to the status.

        :param state: state of the host.
        :type state: str
        :return: QPixmap with image
        :rtype: QPixmap
        """

        if 'UP' in state:
            icon_name = 'hosts_up'
        elif 'UNREACHABLE' in state:
            icon_name = 'hosts_unreach'
        elif 'DOWN' in state:
            icon_name = 'hosts_down'
        else:
            icon_name = 'hosts_none'

        logger.debug('Host icon: ' + icon_name)
        icon = QPixmap(get_image_path(icon_name))

        return icon
