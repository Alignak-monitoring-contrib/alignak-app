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
    Server QDialog manage creation of QDialogs and QWidgets for LoginQDialog
"""

import sys
from logging import getLogger

from PyQt5.Qt import QGridLayout
from PyQt5.Qt import QLineEdit, Qt, QIcon, QLabel, QVBoxLayout, QWidget, QDialog, QPushButton

from alignak_app.core.utils.config import app_css, get_image
from alignak_app.core.utils.config import get_app_config
from alignak_app.pyqt.common.widgets import get_logo_widget, center_widget

logger = getLogger(__name__)


class ServerQDialog(QDialog):
    """
        Class who create Server QDialog.
    """

    def __init__(self, parent=None):
        super(ServerQDialog, self).__init__(parent)
        self.setWindowTitle(_('Server Configuration'))
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet(app_css)
        self.setWindowIcon(QIcon(get_image('icon')))
        self.setObjectName('dialog')
        self.setFixedSize(300, 330)
        # Fields
        self.server_proc = QLineEdit()
        self.server_url = QLineEdit()
        self.server_port = QLineEdit()
        self.offset = None

    def initialize_dialog(self):
        """
        Initialize Server QDialog

        """

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(get_logo_widget(self, _('Alignak server')))

        server_widget = QWidget(self)
        server_widget.setObjectName('dialog')
        server_layout = QGridLayout(server_widget)

        # Description
        desc_label = QLabel(
            _(
                '<h3>Alignak Backend</h3><p>Here you can define alignak settings.</p>'
                '<b>Be sure to enter a valid address</b>'
            )
        )
        desc_label.setWordWrap(True)
        server_layout.addWidget(desc_label, 0, 0, 1, 3)

        # Server URL
        server_layout.addWidget(QLabel(_('Server')), 1, 0, 1, 1)

        self.server_url.setPlaceholderText(_('alignak backend url'))
        self.server_url.setText(get_app_config('Alignak', 'url'))
        server_layout.addWidget(self.server_url, 1, 1, 1, 2)

        # Server Port
        server_layout.addWidget(QLabel(_('Port')), 2, 0, 1, 1)

        self.server_port.setPlaceholderText(_('alignak backend port'))
        cur_port = get_app_config('Alignak', 'backend').split(':')[2]
        self.server_port.setText(cur_port)
        server_layout.addWidget(self.server_port, 2, 1, 1, 2)

        # Server Processes
        server_layout.addWidget(QLabel(_('Processes')), 3, 0, 1, 1)

        if 'win32' in sys.platform:
            self.server_proc.setEnabled(False)
        self.server_proc.setPlaceholderText(_('alignak backend processes'))
        cur_proc = get_app_config('Alignak', 'processes')
        self.server_proc.setText(cur_proc)
        server_layout.addWidget(self.server_proc, 3, 1, 1, 2)

        # Valid Button
        valid_btn = QPushButton(_('Valid'))
        valid_btn.setObjectName('valid')
        valid_btn.setMinimumHeight(30)
        valid_btn.clicked.connect(self.accept)
        server_layout.addWidget(valid_btn, 4, 0, 1, 3)

        main_layout.addWidget(server_widget)

        center_widget(server_widget)

    def mousePressEvent(self, event):  # pragma: no cover - not testable
        """ QWidget.mousePressEvent(QMouseEvent) """

        self.offset = event.pos()

    def mouseMoveEvent(self, event):  # pragma: no cover - not testable
        """ QWidget.mousePressEvent(QMouseEvent) """

        try:
            x = event.globalX()
            y = event.globalY()
            x_w = self.offset.x()
            y_w = self.offset.y()
            self.move(x - x_w, y - y_w)
        except AttributeError as e:
            logger.warning('Move Event %s: %s', self.objectName(), str(e))
