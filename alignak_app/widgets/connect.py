#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015-2016:
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
    Login manage login form
"""

from logging import getLogger

from alignak_app import __short_version__
from alignak_app.core.backend import AppBackend, Backend, BackendException
from alignak_app.core.utils import get_app_config
from alignak_app.widgets.title import get_widget_title


try:
    __import__('PyQt5')
    from PyQt5.QtWidgets import QApplication, QWidget  # pylint: disable=no-name-in-module
    from PyQt5.QtWidgets import QDialog, QPushButton  # pylint: disable=no-name-in-module
    from PyQt5.QtWidgets import QVBoxLayout, QLabel  # pylint: disable=no-name-in-module
    from PyQt5.Qt import QLineEdit, QMessageBox, Qt  # pylint: disable=no-name-in-module
except ImportError:  # pragma: no cover
    from PyQt4.Qt import QApplication, QWidget  # pylint: disable=import-error
    from PyQt4.Qt import QDialog, QPushButton  # pylint: disable=import-error
    from PyQt4.Qt import QVBoxLayout, QLabel  # pylint: disable=import-error
    from PyQt4.Qt import QLineEdit, QMessageBox, Qt  # pylint: disable=import-error


logger = getLogger(__name__)


class AppLogin(QDialog):
    """
        Class who create login QDialog.
    """

    def __init__(self, parent=None):
        super(AppLogin, self).__init__(parent)
        self.setWindowTitle('Connect to Alignak')
        self.resize(300, 150)
        self.app_backend = AppBackend()
        self.username_line = None
        self.password_line = None
        self.message = None
        self.login_line = None

    def create_widget(self):
        """
        Create widget login

        """

        layout = QVBoxLayout(self)

        # QDialog title
        popup_title = get_widget_title('', self)
        layout.addWidget(popup_title, 0)

        # Login text
        login_line = QLabel('<b>LOGIN</b>')
        login_line.setStyleSheet('color: #1fb4e4; font-size: 18px;')
        layout.addWidget(login_line, 1)

        # Welcome text
        welcome = QLabel(
            '<b>Welcome to Alignak-app v' +
            __short_version__ +
            '</b><br>Please enter your credentials'
        )
        welcome.setStyleSheet('font-size: 14px; text-align: center;')
        layout.addWidget(welcome, 2)
        layout.setAlignment(welcome, Qt.AlignTrailing)

        # Username field
        self.username_line = QLineEdit(self)
        self.username_line.setPlaceholderText('Username')
        layout.addWidget(self.username_line, 3)

        # Password field
        self.password_line = QLineEdit(self)
        self.password_line.setPlaceholderText('Password')
        layout.addWidget(self.password_line, 4)

        # Login button
        login_button = QPushButton('Login', self)
        login_button.clicked.connect(self.handle_login)
        layout.addWidget(login_button, 5)

        # Message output
        self.message = QLabel('...')
        layout.addWidget(self.message, 6)
        layout.setAlignment(self.message, Qt.AlignCenter)

        self.setLayout(layout)

    def handle_login(self):
        """
        Handle for login button

        """

        username = self.username_line.text()
        password = self.password_line.text()

        self.app_backend.backend = Backend(get_app_config('Backend', 'backend_url'))

        try:
            resp = self.app_backend.backend.login(username, password)

            if resp:
                self.accept()
            else:
                self.message.setText('Bad crendentials :(')
                self.message.setStyleSheet('color: red;')
                logger.error('Bad credentials in login form.')
        except BackendException as e:
            self.message.setText('Bad crendentials :(')
            self.message.setStyleSheet('color: red;')
            logger.error('Bad credentials in login form ! Missing password !')
            logger.error(str(e))
