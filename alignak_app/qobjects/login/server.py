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
    Server
    ++++++
    Server manage creation of QDialog for Alignak backend server settings
"""

import sys
from logging import getLogger

from PyQt5.Qt import QGridLayout
from PyQt5.Qt import QLineEdit, Qt, QIcon, QLabel, QVBoxLayout, QWidget, QDialog, QPushButton

from alignak_app.utils.config import settings

from alignak_app.qobjects.common.widgets import get_logo_widget, center_widget

logger = getLogger(__name__)


class ServerQDialog(QDialog):
    """
        Class who create Server QDialog.
    """

    def __init__(self, parent=None):
        super(ServerQDialog, self).__init__(parent)
        self.setWindowTitle(_('Server Configuration'))
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet(settings.css_style)
        self.setWindowIcon(QIcon(settings.get_image('icon')))
        self.setObjectName('dialog')
        self.setFixedSize(300, 360)
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
        server_layout = QVBoxLayout(server_widget)

        # Title
        title_lbl = QLabel(_('Alignak Backend'))
        title_lbl.setObjectName('itemtitle')
        server_layout.addWidget(title_lbl)
        server_layout.setAlignment(title_lbl, Qt.AlignTop)

        # Description
        desc_label = QLabel(
            _(
                '<p>Here you can define alignak settings.</p>'
                '<b>Be sure to enter a valid address</b>'
            )
        )
        desc_label.setWordWrap(True)
        server_layout.addWidget(desc_label)

        # Server URL
        server_lbl = QLabel(_('Server'))
        server_layout.addWidget(server_lbl)

        self.server_url.setText(settings.get_config('Alignak', 'url'))
        self.server_url.setPlaceholderText(_('alignak backend url'))
        self.server_url.setFixedHeight(25)
        server_layout.addWidget(self.server_url)

        # Server Port
        port_lbl = QLabel(_('Port'))
        server_layout.addWidget(port_lbl)

        cur_port = settings.get_config('Alignak', 'backend').split(':')[2]
        self.server_port.setText(cur_port)
        self.server_port.setPlaceholderText(_('alignak backend port'))
        self.server_port.setFixedHeight(25)
        server_layout.addWidget(self.server_port)

        # Server Processes
        process_lbl = QLabel(_('Processes'))
        server_layout.addWidget(process_lbl)

        if 'win32' in sys.platform:
            self.server_proc.setEnabled(False)
        cur_proc = settings.get_config('Alignak', 'processes')
        self.server_proc.setText(cur_proc)
        self.server_proc.setPlaceholderText(_('alignak backend processes'))
        self.server_proc.setFixedHeight(25)
        server_layout.addWidget(self.server_proc)

        # Valid Button
        valid_btn = QPushButton(_('Valid'))
        valid_btn.setObjectName('valid')
        valid_btn.setMinimumHeight(30)
        valid_btn.clicked.connect(self.accept)
        server_layout.addWidget(valid_btn)

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
