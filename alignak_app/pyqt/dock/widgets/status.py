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
    Status QWidget display alignak daemons and backend status
"""

from logging import getLogger

from PyQt5.Qt import QLabel, QPushButton, QIcon, QStyleOption, QPainter, QStyle
from PyQt5.Qt import QWidget, QHBoxLayout, QTimer, QPixmap, Qt

from alignak_app.core.backend.client import app_backend
from alignak_app.core.models.daemon import Daemon
from alignak_app.core.utils.config import get_image, app_css, get_app_config

from alignak_app.pyqt.dock.dialogs.status import StatusQDialog

logger = getLogger(__name__)


class StatusQWidget(QWidget):
    """
        Class who display daemons and backend status
    """

    def __init__(self):
        super(StatusQWidget, self).__init__()
        self.setObjectName('bordered')
        self.setStyleSheet(app_css)
        # Fields
        self.daemons_status = QLabel('pending...')
        self.backend_connected = QLabel('pending...')
        self.status_dialog = StatusQDialog()
        self.refresh_timer = QTimer()

    def initialize(self):
        """
        Initialize QWidget

        """

        self.update_status()

        layout = QHBoxLayout()
        self.setLayout(layout)

        # Daemons
        daemons_title = QLabel(_('Status:'))
        daemons_title.setObjectName('borderedtitle')
        layout.addWidget(daemons_title)
        layout.setAlignment(daemons_title, Qt.AlignCenter)

        self.daemons_status.setFixedSize(16, 16)
        self.daemons_status.setScaledContents(True)
        self.daemons_status.setObjectName('borderedtitle')
        layout.addWidget(self.daemons_status)
        layout.setAlignment(self.daemons_status, Qt.AlignCenter)

        # Status button
        self.status_dialog.initialize()
        status_btn = QPushButton()
        status_btn.setIcon(QIcon(get_image('icon')))
        status_btn.setFixedSize(32, 32)
        status_btn.clicked.connect(self.show_status_dialog)
        layout.addWidget(status_btn)
        layout.setAlignment(status_btn, Qt.AlignCenter)

        # Backend state
        connected_title = QLabel(_('Backend:'))
        connected_title.setObjectName('borderedtitle')
        layout.addWidget(connected_title)
        layout.setAlignment(connected_title, Qt.AlignCenter)

        self.backend_connected.setFixedSize(16, 16)
        self.backend_connected.setScaledContents(True)
        self.backend_connected.setObjectName('borderedtitle')
        layout.addWidget(self.backend_connected)
        layout.setAlignment(self.backend_connected, Qt.AlignCenter)

        update_status = int(get_app_config('Alignak-app', 'update_status')) * 1000
        self.refresh_timer.setInterval(update_status)
        self.refresh_timer.start()
        self.refresh_timer.timeout.connect(self.update_status)

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

        logger.info("Update Status QWidget...")
        self.backend_connected.setPixmap(
            QPixmap(get_image(app_backend.get_backend_status_icon()))
        )
        self.daemons_status.setPixmap(
            QPixmap(get_image(Daemon.get_daemons_status_icon()))
        )

    def paintEvent(self, _):
        """Override to paint background"""

        opt = QStyleOption()
        opt.initFrom(self)
        painter = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, painter, self)
