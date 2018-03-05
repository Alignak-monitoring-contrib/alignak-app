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
    Password
    ++++++++
    Password manage Qdialog for user password
"""

from logging import getLogger

from PyQt5.Qt import QLineEdit, Qt, QIcon, QLabel, QWidget, QDialog, QPushButton, QVBoxLayout

from alignak_app.utils.config import settings

from alignak_app.qobjects.common.widgets import center_widget, get_logo_widget

logger = getLogger(__name__)


class PasswordQDialog(QDialog):
    """
        Class who create PasswordDialog QDialog
    """

    def __init__(self, parent=None):
        super(PasswordQDialog, self).__init__(parent)
        self.setWindowTitle('User Password')
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet(settings.css_style)
        self.setWindowIcon(QIcon(settings.get_image('icon')))
        self.setObjectName('dialog')
        self.setFixedSize(300, 300)
        # Fields
        self.pass_edit = QLineEdit()
        self.confirm_edit = QLineEdit()
        self.help_label = QLabel()

    def initialize(self):
        """
        Initialize QDialog for PasswordDialog

        """

        center_widget(self)

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)

        main_layout.addWidget(get_logo_widget(self, _('Edit Password')))

        pass_title = QLabel(_("Please type a new PASSWORD:"))
        pass_title.setObjectName('itemtitle')
        main_layout.addWidget(pass_title)
        main_layout.setAlignment(pass_title, Qt.AlignCenter)

        pass_widget = QWidget()
        pass_widget.setObjectName('dialog')
        pass_layout = QVBoxLayout()
        pass_widget.setLayout(pass_layout)

        self.pass_edit.setPlaceholderText(_('type new password'))
        self.pass_edit.setEchoMode(QLineEdit.Password)
        self.pass_edit.setFixedHeight(25)
        pass_layout.addWidget(self.pass_edit)

        self.confirm_edit.setPlaceholderText(_('confirm new password'))
        self.confirm_edit.setEchoMode(QLineEdit.Password)
        self.confirm_edit.setFixedHeight(25)
        pass_layout.addWidget(self.confirm_edit)

        self.help_label.setText(_("Your password must contain at least 5 characters."))
        self.help_label.setWordWrap(True)
        pass_layout.addWidget(self.help_label)

        # Accept button
        accept_btn = QPushButton('Confirm', self)
        accept_btn.clicked.connect(self.handle_confirm)
        accept_btn.setObjectName('valid')
        accept_btn.setMinimumHeight(30)
        pass_layout.addWidget(accept_btn)

        main_layout.addWidget(pass_widget)

    def handle_confirm(self):
        """
        Handle accept_btn for password

        """

        if bool(self.pass_edit.text() == self.confirm_edit.text()) and \
                len(self.pass_edit.text()) > 4 and len(self.confirm_edit.text()) > 4:
            self.accept()
        else:
            if bool(self.pass_edit.text() != self.confirm_edit.text()):
                self.help_label.setText(_("Passwords do not match !"))
                self.help_label.setStyleSheet("color: red;")
            if len(self.pass_edit.text()) < 5 or len(self.confirm_edit.text()) < 5:
                self.help_label.setText(_("Your password must contain at least 5 characters."))
                self.help_label.setStyleSheet("color: orange;")
