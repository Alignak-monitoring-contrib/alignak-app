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

import time
import datetime

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

        # Keep labels that will be updated in dict
        self.labels = {
            'name': QLabel('<h3>Host Name</h3>'),
            'state_icon': QLabel(),
            'real_state_icon': QLabel(),
            'last_check': QLabel('N/A'),
            'output': QLabel('N/A')
        }

        # Create QWidgets
        states_widget = self.get_states_widget()
        check_widget = self.get_check_widget()
        buttons = self.get_buttons_widget()

        self.layout.addWidget(states_widget, 0, 0)
        self.layout.addWidget(check_widget, 0, 1, 1, 2)
        self.layout.addWidget(buttons, 0, 3)

    def get_states_widget(self):
        """
        Add QWidget states icons

        :return: states QWidget
        :rtype: QWidget
        """

        states_widget = QWidget(self)
        states_widget.setObjectName('states')
        states_widget.setStyleSheet(
            'QWidget#states{border: 1px solid #03a9f4;border-radius: 16px;}'
        )
        states_layout = QGridLayout()
        states_widget.setLayout(states_layout)

        self.labels['state_icon'].setFixedSize(64, 64)
        self.labels['state_icon'].setPixmap(self.get_host_icon(''))
        states_layout.addWidget(self.labels['state_icon'], 0, 0, 2, 2)

        self.labels['name'].setWordWrap(True)
        states_layout.addWidget(self.labels['name'], 2, 0, 1, 2)

        self.labels['real_state_icon'].setFixedSize(32, 32)
        self.labels['real_state_icon'].setScaledContents(True)
        self.labels['real_state_icon'].setPixmap(self.get_host_icon(''))
        states_layout.addWidget(self.labels['real_state_icon'], 2, 2, 1, 1)

        real_state_text = QLabel('Host real state, excluding services')
        real_state_text.setWordWrap(True)
        real_state_text.setStyleSheet('font-size: 10px;')
        states_layout.addWidget(real_state_text, 0, 2, 1, 1)

        return states_widget

    def get_check_widget(self):
        """
        Create and return check QWidget

        :return: Checks qwidget
        :rtype: QWidget
        """

        check_widget = QWidget(self)
        check_layout = QGridLayout()
        # check_widget.setStyleSheet('QLabel#title{}')
        check_widget.setLayout(check_layout)

        check_label = QLabel('<b>My last Check</b>')
        check_label.setObjectName('title')
        check_label.setStyleSheet(
            'border-style: solid;border-width:0px 0px 1px 0px;border-color: #03a9f4;'
        )
        check_layout.addWidget(check_label, 0, 0, 1, 2)
        check_layout.setAlignment(check_label, Qt.AlignCenter)

        last_check = QLabel('<b>Last check:</b>')
        check_layout.addWidget(last_check, 1, 0, 1, 1)
        check_layout.setAlignment(last_check, Qt.AlignLeft)

        check_layout.addWidget(self.labels['last_check'], 1, 1, 1, 2)

        output = QLabel('<b>Output:</b>')
        check_layout.addWidget(output, 2, 0, 1, 1)
        check_layout.setAlignment(output, Qt.AlignLeft)

        self.labels['output'].setWordWrap(True)
        check_layout.addWidget(self.labels['output'], 2, 1, 1, 2)

        return check_widget

    def get_buttons_widget(self):
        """
        Create and return QWidget for ack and downtime buttons

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

            if 'actiondowntime' in sender.objectName():
                comment = 'Schedule downtime by ' + user['name'] + ', from Alignak-app'
            else:
                comment = 'Acknowledge by ' + user['name'] + ', from Alignak-app'
            data = {
                'action': 'add',
                'host': self.host['_id'],
                'service': None,
                'user': user['_id'],
                'comment': comment
            }

            if 'actiondowntime' in sender.objectName():
                start_time = datetime.datetime.now()
                end_time = start_time + datetime.timedelta(days=1)
                data['start_time'] = start_time.timestamp()
                data['end_time'] = end_time.timestamp()
                data['fixed'] = True

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
                    ack_timer.singleShot(17000, self.downtime_message)
                else:
                    self.ack_button.setEnabled(False)
                    self.ack_button.setText('Waiting from backend...')
                    ack_timer.singleShot(17000, self.ack_message)
            else:
                logger.error('Action ' + sender.objectName() + 'failed')

    def ack_message(self):
        """
        Display QMessageBox if acknowledge processed return True

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

    def downtime_message(self):
        """
        Display QMessageBox if downtime processed return True

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

    def update_view(self, data):
        """
        Update Host view with desired host.

        :param data: host data with associated services from app_backend
        :type data: dict
        """

        self.host = data['host']

        logger.info('Update Host View...')
        logger.debug('Host: ' + self.host['name'] + ' is ' + self.host['ls_state'])

        if isinstance(self.host['ls_last_check'], int):
            time_delta = get_diff_since_last_check(self.host['ls_last_check'])
        else:
            time_delta = 'NOT FOUND'

        self.labels['name'].setText('<h3>' + self.host['alias'].title() + '</h3>')
        self.labels['state_icon'].setPixmap(self.get_real_state_icon(data['services']))
        self.labels['real_state_icon'].setPixmap(self.get_host_icon(self.host['ls_state']))
        self.labels['last_check'].setText(str(time_delta))
        self.labels['output'].setText(self.host['ls_output'])

        self.update_action_button()

    def update_action_button(self):
        """
        Check if there is action and update button

        """

        logger.debug('ACK: is ' + str(self.host['ls_acknowledged']))
        logger.debug('DOWNTIME: is ' + str(self.host['ls_downtimed']))

        if self.host['ls_acknowledged'] or 'UP' in self.host['ls_state']:
            self.ack_button.setEnabled(False)
            self.ack_button.setText('Acknowledged !')
            self.ack_button.setIcon(QIcon(get_image_path('valid')))
        else:
            self.ack_button.setEnabled(True)
            self.ack_button.setText('Acknowledge this problem')
            self.ack_button.setIcon(QIcon(get_image_path('acknowledged')))

        if self.host['ls_downtimed'] or 'UP' in self.host['ls_state']:
            self.down_button.setEnabled(False)
            self.down_button.setText('Downtimed !')
            self.down_button.setIcon(QIcon(get_image_path('downtime')))
        else:
            self.down_button.setEnabled(True)
            self.down_button.setText('Schedule a downtime')
            self.down_button.setIcon(QIcon(get_image_path('downtime')))

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

        icon = QPixmap(get_image_path(icon_name))

        return icon

    @staticmethod
    def get_real_state_icon(services):
        """
        Calculate real state and return QPixmap

        :param services: dict of services. None if search is not found
        :type services: dict
        """

        if services:
            icon_names = ['hosts_up', 'hosts_none', 'hosts_unreach', 'hosts_down']
            state_lvl = []
            for service in services:
                if 'UNREACHABLE' in service['ls_state'] or 'CRITICAL' in service['ls_state']:
                    state_lvl.append(3)
                elif 'WARNING' in service['ls_state'] or 'UNKNOWN' in service['ls_state']:
                    state_lvl.append(2)
                elif service['ls_downtimed']:
                    state_lvl.append(1)
                else:
                    state_lvl.append(0)

            result = max(state_lvl)

            icon = QPixmap(get_image_path(icon_names[result]))
        else:
            icon = QPixmap(get_image_path('hosts_none'))

        return icon
