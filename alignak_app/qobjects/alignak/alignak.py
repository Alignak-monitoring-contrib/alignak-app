#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015-2018:
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
    Alignak
    +++++++
    Alignak manage creation of QWidgets for general Alignak data, like:

    * **Daemons status:** status of each daemons (
      see :class:`StatusQDialog <alignak_app.qobjects.alignak.status.StatusQDialog>` class)
    * **Backend connection:** status of backend connection (
      see :class:`TrayIcon <alignak_app.qobjects.systray.tray_icon.AppTrayIcon>` class)
    * **User:** data of current user (see :class:`User <alignak_app.qobjects.user>` package)

"""

from logging import getLogger

from PyQt5.Qt import QLabel, QPushButton, QIcon, QWidget, QTimer, QPixmap, Qt, QGridLayout

from alignak_app.backend.backend import app_backend
from alignak_app.backend.datamanager import data_manager
from alignak_app.qobjects.alignak.status import StatusQDialog
from alignak_app.utils.config import settings

from alignak_app.qobjects.user.profile import ProfileQWidget

logger = getLogger(__name__)


class AlignakQWidget(QWidget):
    """
        Class who display daemons status, backend connection and user informations
    """

    def __init__(self):
        super(AlignakQWidget, self).__init__()
        # Fields
        self.backend_connected = QLabel('pending...')
        self.status_dialog = StatusQDialog()
        self.status_btn = QPushButton()
        self.profile_widget = ProfileQWidget()
        self.profile_btn = QPushButton()
        self.refresh_timer = QTimer()

    def initialize(self):
        """
        Initialize QWidget

        """

        self.update_status()

        layout = QGridLayout()
        self.setLayout(layout)

        # Backend state
        connected_title = QLabel(_('Backend'))
        connected_title.setObjectName('subtitle')
        layout.addWidget(connected_title, 0, 0, 1, 1)
        layout.setAlignment(connected_title, Qt.AlignCenter)

        self.backend_connected.setFixedSize(16, 16)
        self.backend_connected.setScaledContents(True)
        layout.addWidget(self.backend_connected, 0, 1, 1, 1)
        layout.setAlignment(self.backend_connected, Qt.AlignCenter)

        # Daemons Status
        daemons_title = QLabel(_('Status'))
        daemons_title.setObjectName('subtitle')
        layout.addWidget(daemons_title, 1, 0, 1, 1)
        layout.setAlignment(daemons_title, Qt.AlignCenter)

        # Status button
        self.status_dialog.initialize()
        self.status_btn.setIcon(QIcon(settings.get_image('icon')))
        self.status_btn.setFixedSize(32, 32)
        self.status_btn.clicked.connect(self.show_status_dialog)
        layout.addWidget(self.status_btn, 1, 1, 1, 1)
        layout.setAlignment(self.status_btn, Qt.AlignCenter)

        # User
        user_lbl = QLabel(_('User'))
        user_lbl.setObjectName('subtitle')
        layout.addWidget(user_lbl, 0, 2, 2, 1)
        self.profile_widget.initialize()
        self.profile_btn.setIcon(QIcon(settings.get_image('user')))
        self.profile_btn.setFixedSize(40, 40)
        self.profile_btn.clicked.connect(self.open_user_widget)
        self.profile_btn.setToolTip(_('User'))
        layout.addWidget(self.profile_btn, 0, 3, 2, 1)

        update_status = int(settings.get_config('Alignak-app', 'update_status')) * 1000
        self.refresh_timer.setInterval(update_status)
        self.refresh_timer.start()
        self.refresh_timer.timeout.connect(self.update_status)

    def show_status_dialog(self):
        """
        Update and show StatusQDialog

        """

        self.status_dialog.update_dialog()
        self.status_dialog.app_widget.show_widget()

    def open_user_widget(self):
        """
        Show ProfileQWidget

        """

        self.profile_widget.update_widget()
        self.profile_widget.app_widget.show_widget()

    def update_status(self):
        """
        Update daemons and backend status

        """

        self.backend_connected.setPixmap(
            QPixmap(settings.get_image(app_backend.get_backend_status_icon()))
        )
        self.status_btn.setEnabled(bool(data_manager.database['alignakdaemon']))

        if self.status_dialog.labels:
            self.status_dialog.update_dialog()
