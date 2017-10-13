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
    Token Dialog manage display of user token
"""

from logging import getLogger

from alignak_app.core.utils import get_css, get_image_path
from alignak_app.core.data_manager import data_manager
from alignak_app.widgets.utils_widgets import get_logo_widget, center_widget

from PyQt5.Qt import QWidget, QDialog, QIcon, Qt  # pylint: disable=no-name-in-module
from PyQt5.Qt import QPushButton, QLabel, QVBoxLayout  # pylint: disable=no-name-in-module

logger = getLogger(__name__)


class TokenQDialog(QDialog):
    """
        Class who create Token QDialog
    """

    def __init__(self, parent=None):
        super(TokenQDialog, self).__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet(get_css())
        self.setWindowIcon(QIcon(get_image_path('icon')))
        self.setFixedSize(500, 200)

    def initialize(self):
        """
        Initialize QDialog for PasswordDialog

        """

        center_widget(self)

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)

        main_layout.addWidget(get_logo_widget(self))

        # Token QWidget
        token_widget = QWidget()
        token_layout = QVBoxLayout()
        token_widget.setLayout(token_layout)

        token_title = QLabel("Token: %s" % data_manager.database['user'].name.capitalize())
        token_layout.addWidget(token_title)
        token_layout.setAlignment(token_title, Qt.AlignCenter)

        token_label = QLabel(data_manager.database['user'].data['token'])
        token_label.setObjectName('output')
        token_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        token_label.setWordWrap(True)
        token_layout.addWidget(token_label)

        # Login button
        accept_btn = QPushButton('OK', self)
        accept_btn.clicked.connect(self.accept)
        accept_btn.setObjectName('valid')
        accept_btn.setMinimumHeight(30)
        token_layout.addWidget(accept_btn)

        main_layout.addWidget(token_widget)
