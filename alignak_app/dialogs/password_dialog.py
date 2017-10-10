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
    Password manage password form
"""

from logging import getLogger

from alignak_app.core.utils import get_css, get_image_path


from PyQt5.QtWidgets import QWidget, QDialog, QApplication  # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QPushButton  # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout  # pylint: disable=no-name-in-module
from PyQt5.Qt import QLineEdit, Qt, QIcon, QLabel, QPixmap  # pylint: disable=no-name-in-module


logger = getLogger(__name__)


class PasswordQDialog(QDialog):
    """
        Class who create PasswordDialog QDialog
    """

    def __init__(self, parent=None):
        super(PasswordQDialog, self).__init__(parent)
        self.setWindowTitle('User Password')
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet(get_css())
        self.setWindowIcon(QIcon(get_image_path('icon')))
        self.setFixedSize(300, 300)
        # Fields
        self.pass_edit = None
        self.confirm_edit = None
        self.help_label = None

    def initialize(self):
        """
        Initialize QDialog for PasswordDialog

        """

        self.center(self)

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)

        main_layout.addWidget(self.get_logo_widget(self))

        pass_title = QLabel("Please type a new PASSWORD:")
        main_layout.addWidget(pass_title)
        main_layout.setAlignment(pass_title, Qt.AlignCenter)

        pass_widget = QWidget()
        pass_widget.setObjectName('login')
        pass_layout = QVBoxLayout()
        pass_widget.setLayout(pass_layout)

        self.pass_edit = QLineEdit()
        self.pass_edit.setPlaceholderText('type password')
        self.pass_edit.setEchoMode(QLineEdit.Password)
        pass_layout.addWidget(self.pass_edit)

        self.confirm_edit = QLineEdit()
        self.confirm_edit.setPlaceholderText('confirm password')
        self.confirm_edit.setEchoMode(QLineEdit.Password)
        pass_layout.addWidget(self.confirm_edit)

        self.help_label = QLabel("Your password must contain at least 5 characters.")
        self.help_label.setWordWrap(True)
        pass_layout.addWidget(self.help_label)

        # Login button
        accept_btn = QPushButton('Confirm', self)
        accept_btn.clicked.connect(self.handle_confirm)
        accept_btn.setObjectName('valid')
        accept_btn.setMinimumHeight(30)
        pass_layout.addWidget(accept_btn)

        main_layout.addWidget(pass_widget)

    @staticmethod
    def get_logo_widget(widget):
        """
        Return the logo QWidget

        :param widget: widget parent, needed for action button
        :type widget: QWidget
        :return: logo QWidget
        :rtype: QWidget
        """

        logo_widget = QWidget()
        logo_widget.setFixedHeight(45)
        logo_widget.setObjectName('app_widget')
        logo_layout = QHBoxLayout()
        logo_widget.setLayout(logo_layout)

        logo_label = QLabel()
        logo_label.setPixmap(QPixmap(get_image_path('password')))
        logo_label.setObjectName('widget_title')
        logo_label.setScaledContents(True)

        logo_layout.addWidget(logo_label, 0)

        minimize_btn = QPushButton()
        minimize_btn.setIcon(QIcon(get_image_path('minimize')))
        minimize_btn.setFixedSize(24, 24)
        minimize_btn.setObjectName('app_widget')
        minimize_btn.clicked.connect(widget.showMinimized)
        logo_layout.addStretch(widget.width())
        logo_layout.addWidget(minimize_btn, 1)

        maximize_btn = QPushButton()
        maximize_btn.setIcon(QIcon(get_image_path('maximize')))
        maximize_btn.setFixedSize(24, 24)
        maximize_btn.setObjectName('app_widget')
        maximize_btn.clicked.connect(widget.showMaximized)
        logo_layout.addWidget(maximize_btn, 2)

        close_btn = QPushButton()
        close_btn.setIcon(QIcon(get_image_path('exit')))
        close_btn.setObjectName('app_widget')
        close_btn.setFixedSize(24, 24)
        close_btn.clicked.connect(widget.close)
        logo_layout.addWidget(close_btn, 3)

        return logo_widget

    def handle_confirm(self):
        """
        Handle accept_btn for password

        """

        if bool(self.pass_edit.text() == self.confirm_edit.text()) and \
                len(self.pass_edit.text()) > 4 and len(self.confirm_edit.text()) > 4:
            self.accept()
        else:
            if bool(self.pass_edit.text() != self.confirm_edit.text()):
                self.help_label.setText("Passwords do not match !")
                self.help_label.setStyleSheet("color: red;")
            if len(self.pass_edit.text()) < 5 or len(self.confirm_edit.text()) < 5:
                self.help_label.setText("Your password must contain at least 5 characters.")
                self.help_label.setStyleSheet("color: orange;")

    @staticmethod
    def center(widget):
        """
        Center QWidget

        """

        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        center = QApplication.desktop().screenGeometry(screen).center()
        widget.move(center.x() - (widget.width() / 2), center.y() - (widget.height() / 2))
