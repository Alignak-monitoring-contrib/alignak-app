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
    Token
    +++++
    Token manage creation of QDialog for user token
"""

from logging import getLogger

from PyQt5.Qt import QPushButton, QLabel, QVBoxLayout, QWidget, QDialog, QIcon, Qt

from alignak_app.backend.datamanager import data_manager
from alignak_app.utils.config import settings

from alignak_app.qobjects.common.widgets import get_logo_widget, center_widget

logger = getLogger(__name__)


class TokenQDialog(QDialog):
    """
        Class who create Token QDialog
    """

    def __init__(self, parent=None):
        super(TokenQDialog, self).__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet(settings.css_style)
        self.setWindowIcon(QIcon(settings.get_image('icon')))
        self.setFixedSize(500, 200)
        self.setObjectName('dialog')

    def initialize(self):
        """
        Initialize QDialog for PasswordDialog

        """

        center_widget(self)

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)

        main_layout.addWidget(get_logo_widget(self, _('See Token')))
        main_layout.addWidget(self.get_token_widget())

    def get_token_widget(self):
        """
        Return token QWidget

        :return: token QWidget
        :rtype: QWidget
        """

        # Token QWidget
        token_widget = QWidget()
        token_widget.setObjectName('dialog')
        token_layout = QVBoxLayout()
        token_widget.setLayout(token_layout)

        token_title = QLabel(
            _("<b>Token:</b> %s") % data_manager.database['user'].name.capitalize()
        )
        token_title.setObjectName('itemtitle')
        token_layout.addWidget(token_title)
        token_layout.setAlignment(token_title, Qt.AlignCenter)

        token_label = QLabel(data_manager.database['user'].data['token'])
        token_label.setObjectName('notes')
        token_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        token_label.setWordWrap(True)
        token_layout.addWidget(token_label)

        # Login button
        accept_btn = QPushButton('OK', self)
        accept_btn.clicked.connect(self.accept)
        accept_btn.setObjectName('ok')
        accept_btn.setMinimumHeight(30)
        token_layout.addWidget(accept_btn)

        return token_widget
