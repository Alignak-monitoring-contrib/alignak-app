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
    Host manage QWidgets for hosts.
"""

import datetime

from logging import getLogger

from alignak_app.core.utils import get_image_path
from alignak_app.core.utils import get_diff_since_last_check
from alignak_app.core.action_manager import ACK, DOWNTIME, PROCESS

try:
    __import__('PyQt5')
    from PyQt5.QtWidgets import QPushButton  # pylint: disable=no-name-in-module
    from PyQt5.QtWidgets import QWidget, QVBoxLayout  # pylint: disable=no-name-in-module
    from PyQt5.QtWidgets import QGridLayout, QLabel  # pylint: disable=no-name-in-module
    from PyQt5.Qt import QPixmap, Qt, QIcon  # pylint: disable=no-name-in-module
except ImportError:  # pragma: no cover
    from PyQt4.Qt import QPushButton  # pylint: disable=import-error
    from PyQt4.Qt import QWidget, QVBoxLayout  # pylint: disable=import-error
    from PyQt4.Qt import QGridLayout, QLabel  # pylint: disable=import-error
    from PyQt4.Qt import QPixmap, Qt, QIcon  # pylint: disable=import-error


logger = getLogger(__name__)


class Host(QWidget):
    """
        Class who create the Host QWidget for SynthesisView.
    """

    def __init__(self, parent=None):
        super(Host, self).__init__(parent)
        self.setFixedHeight(150)
        self.setMinimumWidth(parent.width())
        self.setToolTip('Host View')
        # Fields
        self.acknowledge_btn = None
        self.downtime_btn = None
        self.layout = None
        self.labels = {}
        self.host = None
        self.app_backend = None
        self.action_manager = None
        self.endpoints = {
            ACK: {},
            DOWNTIME: {}
        }

    def init_view(self, app_backend, action_manager):
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

        self.action_manager = action_manager

    def get_states_widget(self):
        """
        Add QWidget states icons

        :return: states QWidget
        :rtype: QWidget
        """

        states_widget = QWidget(self)
        states_widget.setObjectName("states")
        states_layout = QGridLayout()
        states_widget.setLayout(states_layout)

        self.labels['state_icon'].setFixedSize(64, 64)
        self.labels['state_icon'].setPixmap(self.get_host_icon(''))
        states_layout.addWidget(self.labels['state_icon'], 0, 0, 2, 2)
        states_layout.setAlignment(self.labels['state_icon'], Qt.AlignCenter)

        self.labels['name'].setWordWrap(True)
        states_layout.addWidget(self.labels['name'], 2, 0, 1, 2)

        self.labels['real_state_icon'].setFixedSize(32, 32)
        self.labels['real_state_icon'].setScaledContents(True)
        self.labels['real_state_icon'].setPixmap(self.get_host_icon(''))
        states_layout.addWidget(self.labels['real_state_icon'], 2, 2, 1, 1)
        states_layout.setAlignment(self.labels['real_state_icon'], Qt.AlignCenter)

        real_state_text = QLabel('Host real state, excluding services')
        real_state_text.setWordWrap(True)
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
        check_widget.setLayout(check_layout)

        check_label = QLabel('<b>My last Check</b>')
        check_label.setObjectName('title')
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

        self.acknowledge_btn = QPushButton('Acknowledge this problem')
        self.acknowledge_btn.setToolTip('Acknowledge this problem')
        self.acknowledge_btn.setIcon(QIcon(get_image_path('acknowledged')))
        self.acknowledge_btn.setObjectName(ACK)
        self.acknowledge_btn.clicked.connect(self.add_acknowledge)

        self.downtime_btn = QPushButton('Schedule a downtime')
        self.downtime_btn.setToolTip('Schedule a downtime')
        self.downtime_btn.setIcon(QIcon(get_image_path('downtime')))
        self.downtime_btn.setObjectName(DOWNTIME)
        self.downtime_btn.clicked.connect(self.add_downtime)

        layout.addWidget(self.acknowledge_btn, 0)
        layout.addWidget(self.downtime_btn, 1)

        return button_widget

    def add_acknowledge(self):  # pragma: no cover
        """
        Handle action for "ack_button"

        """

        if self.host:
            user = self.app_backend.get_user()

            comment = 'Acknowledge by %s, from Alignak-app' % user['name']

            data = {
                'action': 'add',
                'host': self.host['_id'],
                'service': None,
                'user': user['_id'],
                'comment': comment
            }

            post = self.app_backend.post(ACK, data)
            item_process = {
                'action': PROCESS,
                'name': self.host['name'],
                'href': post
            }
            self.action_manager.add_item(item_process)

            item_action = {
                'action': ACK,
                'host': self.host,
                'service': None
            }
            self.action_manager.add_item(item_action)

            self.acknowledge_btn.setEnabled(False)
            self.acknowledge_btn.setText('Waiting from backend...')

    def add_downtime(self):
        """
        Handle action for "down_button"

        """

        if self.host:
            user = self.app_backend.get_user()

            comment = 'Schedule downtime by %s, from Alignak-app' % user['name']

            start_time = datetime.datetime.now()
            end_time = start_time + datetime.timedelta(days=1)

            data = {
                'action': 'add',
                'host': self.host['_id'],
                'service': None,
                'user': user['_id'],
                'comment': comment,
                'start_time': start_time.timestamp(),
                'end_time': end_time.timestamp(),
                'fixed': True
            }

            post = self.app_backend.post(DOWNTIME, data)
            item_process = {
                'action': PROCESS,
                'name': self.host['name'],
                'href': post
            }
            self.action_manager.add_item(item_process)

            item_action = {
                'action': DOWNTIME,
                'host': self.host,
                'service': None
            }
            self.action_manager.add_item(item_action)

            self.downtime_btn.setEnabled(False)
            self.downtime_btn.setText('Waiting from backend...')

    def update_view(self, data=False):
        """
        Update Host view with desired host.

        :param data: host data with associated services from app_backend
        :type data: dict
        """

        if data:
            self.host = data['host']

        logger.info('Update Host View...')
        logger.debug('Host: ' + self.host['name'] + ' is ' + self.host['ls_state'])

        if isinstance(self.host['ls_last_check'], int):
            time_delta = get_diff_since_last_check(self.host['ls_last_check'])
        else:
            time_delta = 'N/A'

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

        if self.host['ls_acknowledged'] \
                or 'UP' in self.host['ls_state'] \
                or self.host['name'] in self.action_manager.acks_to_check:
            self.acknowledge_btn.setEnabled(False)
            self.acknowledge_btn.setText('Acknowledged !')
        else:
            self.acknowledge_btn.setEnabled(True)
            self.acknowledge_btn.setText('Acknowledge this problem')

        if self.host['ls_downtimed'] \
                or 'UP' in self.host['ls_state'] \
                or self.host['name'] in self.action_manager.downtimes_to_check:
            self.downtime_btn.setEnabled(False)
            self.downtime_btn.setText('Downtimed !')
        else:
            self.downtime_btn.setEnabled(True)
            self.downtime_btn.setText('Schedule a downtime')

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
