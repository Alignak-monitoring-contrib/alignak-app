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
from alignak_app.dialogs.status_dialog import StatusQDialog

from PyQt5.Qt import QWidget, QHBoxLayout, QTimer, QPixmap, Qt  # pylint: disable=no-name-in-module
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
        self.status_dialog = StatusQDialog()
        self.timer = QTimer()

    def initialize(self):
        """
        Initialize QWidget

        """

        self.update_status()

        layout = QHBoxLayout()
        self.setLayout(layout)

        # Daemons
        daemons_title = QLabel(_('Status:'))
        daemons_title.setObjectName('title')
        layout.addWidget(daemons_title)
        layout.setAlignment(daemons_title, Qt.AlignCenter)
        self.daemons_status.setFixedSize(16, 16)
        self.daemons_status.setScaledContents(True)
        layout.addWidget(self.daemons_status)
        layout.setAlignment(self.daemons_status, Qt.AlignCenter)

        # Status button
        self.status_dialog.initialize()
        status_btn = QPushButton()
        status_btn.setIcon(QIcon(get_image_path('icon')))
        status_btn.setFixedSize(32, 32)
        status_btn.clicked.connect(self.show_status_dialog)
        layout.addWidget(status_btn)
        layout.setAlignment(status_btn, Qt.AlignCenter)

        # Backend state
        connected_title = QLabel(_('Backend:'))
        connected_title.setObjectName('title')
        layout.addWidget(connected_title)
        layout.setAlignment(connected_title, Qt.AlignCenter)

        self.backend_connected.setFixedSize(16, 16)
        self.backend_connected.setScaledContents(True)
        layout.addWidget(self.backend_connected)
        layout.setAlignment(self.backend_connected, Qt.AlignCenter)

        self.timer.setInterval(15000)
        self.timer.start()
        self.timer.timeout.connect(self.update_status)

    def show_status_dialog(self):
        """
        Update and show StatusQDialog

        """

        self.status_dialog.update_dialog()
        self.status_dialog.app_widget.show()

    def update_status(self):
        """
        Update dameons and backend status

        """

        self.backend_connected.setPixmap(
            QPixmap(get_image_path(self.update_backend_status()))
        )
        self.daemons_status.setPixmap(
            QPixmap(get_image_path(self.update_daemons_status()))
        )

    @staticmethod
    def get_states(status):
        """
        Return states of daemons or backend

        :param status: status of item
        :type status: str
        :return: the status string
        :rtype: str
        """

        states = {
            'ok': 'connected',
            'ko': 'disconnected'
        }

        return states[status]

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

        return self.get_states(status)

    def update_backend_status(self):
        """
        Update and return backend status

        :return: daemon status
        :rtype: str
        """

        if app_backend.connected:
            return self.get_states('ok')

        return self.get_states('ko')
