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
    ResumeStatus QWidget display alignak daemons and backend status
"""

from alignak_app.core.utils import get_image_path, get_css
from alignak_app.core.data_manager import data_manager
from alignak_app.core.backend import app_backend

from PyQt5.Qt import QWidget, QHBoxLayout  # pylint: disable=no-name-in-module
from PyQt5.Qt import QLabel, QPushButton, QIcon  # pylint: disable=no-name-in-module


class DockStatusQWidget(QWidget):
    """
        Class who display daemons and backend status
    """

    def __init__(self):
        super(DockStatusQWidget, self).__init__()
        self.setStyleSheet(get_css())
        # Fields
        self.daemons_status = QLabel('pending...')
        self.backend_connected = QLabel('pending...')

    def initialize(self):
        """
        Initialize QWidget

        """

        self.update_status()

        layout = QHBoxLayout()
        self.setLayout(layout)

        # Daemons
        daemons_title = QLabel('Alignak status:')
        daemons_title.setObjectName('title')
        layout.addWidget(daemons_title)
        layout.addWidget(self.daemons_status)

        # Status button
        status_btn = QPushButton()
        status_btn.setIcon(QIcon(get_image_path('icon')))
        status_btn.setFixedSize(32, 32)
        layout.addWidget(status_btn)

        # Backend state
        connected_title = QLabel('Backend:')
        connected_title.setObjectName('title')
        layout.addWidget(connected_title)

        layout.addWidget(self.backend_connected)

    def update_status(self):
        """
        Update dameons and backend status
        TODO: add pyqtSignal to update
        """

        self.backend_connected.setText(self.update_backend_status())
        self.daemons_status.setText(self.update_daemons_status())

    @staticmethod
    def get_states(item_type, status):
        """
        Return states of daemons or backend

        :param item_type: backend or daemons
        :type item_type: str
        :param status: status of item
        :type status: str
        :return: the status string
        :rtype: str
        """

        states = {
            'daemons': {
                'ok': 'online',
                'warn': 'flapping',
                'ko': 'down'
            },
            'backend': {
                'ok': 'connected',
                'ko': 'offline'
            }
        }

        return states[item_type][status]

    def update_daemons_status(self):
        """
        Update and return daemons status

        :return: daemons status
        :rtype: str
        """

        alignak_daemons = data_manager.database['alignakdaemon']

        daemons_down = 0
        daemons_nb = len(alignak_daemons)
        for daemon in alignak_daemons:
            daemons_nb += 1
            if not daemon.data['alive']:
                daemons_down += 1

        if daemons_down == daemons_nb:
            status = 'ko'
        elif daemons_down > 0:
            status = 'warn'
        else:
            status = 'ok'

        self.daemons_status.setObjectName(status)

        return self.get_states('daemons', status)

    def update_backend_status(self):
        """
        Update and return backend status

        :return: daemon status
        :rtype: str
        """

        if app_backend.connected:
            self.backend_connected.setObjectName('ok')
            return self.get_states('backend', 'ok')
        else:
            self.backend_connected.setObjectName('ko')
            return self.get_states('backend', 'ko')
