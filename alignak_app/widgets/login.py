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
from alignak_app.core.backend import AppBackend, Backend
from alignak_app.core.utils import get_app_config, set_app_config, get_css
from alignak_app.widgets.title import get_widget_title
from alignak_app.widgets.tick import send_tick


try:
    __import__('PyQt5')
    from PyQt5.QtWidgets import QApplication  # pylint: disable=no-name-in-module
    from PyQt5.QtWidgets import QDialog, QPushButton  # pylint: disable=no-name-in-module
    from PyQt5.QtWidgets import QGridLayout, QLabel  # pylint: disable=no-name-in-module
    from PyQt5.Qt import QLineEdit, Qt  # pylint: disable=no-name-in-module
except ImportError:  # pragma: no cover
    from PyQt4.Qt import QApplication  # pylint: disable=import-error
    from PyQt4.Qt import QDialog, QPushButton  # pylint: disable=import-error
    from PyQt4.Qt import QGridLayout, QLabel  # pylint: disable=import-error
    from PyQt4.Qt import QLineEdit, Qt  # pylint: disable=import-error


logger = getLogger(__name__)


class AppLogin(QDialog):
    """
        Class who create login QDialog.
    """

    def __init__(self, parent=None):
        super(AppLogin, self).__init__(parent)
        self.setWindowTitle('Connect to Alignak')
        self.resize(320, 150)
        self.app_backend = AppBackend()
        self.backend_url = None
        self.username_line = None
        self.password_line = None
        self.setStyleSheet(get_css())

    def create_widget(self):
        """
        Create widget login

        """

        layout = QGridLayout(self)

        # QDialog title
        popup_title = get_widget_title('', self)
        layout.addWidget(popup_title, 0, 0, 1, 2)

        # Login text
        login_line = QLabel('<b>Login</b>')
        login_line.setObjectName('login')
        layout.addWidget(login_line, 1, 0, 1, 1)

        # Configure button
        conf_button = QPushButton('Server')
        conf_button.clicked.connect(self.handle_server)
        layout.addWidget(conf_button, 1, 1, 1, 1)

        # Welcome text
        welcome = QLabel(
            '<b>Welcome to Alignak-app v' +
            __short_version__ +
            '</b><br>Please enter your credentials'
        )
        layout.addWidget(welcome, 2, 0, 1, 2)
        layout.setAlignment(welcome, Qt.AlignTrailing)

        # Username field
        self.username_line = QLineEdit(self)
        self.username_line.setPlaceholderText('Username')
        self.username_line.setFocus()
        layout.addWidget(self.username_line, 3, 0, 1, 2)

        # Password field
        self.password_line = QLineEdit(self)
        self.password_line.setPlaceholderText('Password')
        self.password_line.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_line, 4, 0, 1, 2)

        # Login button
        login_button = QPushButton('Login', self)
        login_button.clicked.connect(self.handle_login)
        login_button.setDefault(True)
        self.password_line.returnPressed.connect(login_button.click)
        layout.addWidget(login_button, 5, 0, 1, 2)

        self.setLayout(layout)

    def handle_login(self):
        """
        Handle for login button

        """

        username = self.username_line.text()
        password = self.password_line.text()

        self.app_backend.backend = Backend(get_app_config('Backend', 'alignak_backend'))

        resp = self.app_backend.login(str(username), str(password))

        if resp:
            send_tick('OK', 'Connected to Alignak Backend')
            self.app_backend.user['username'] = str(username)
            self.app_backend.user['token'] = str(self.app_backend.backend.token)
            self.accept()
        else:
            send_tick('WARN', 'Your connection information are not accepted !')
            logger.warning('Connection informations are not accepted !')

    def handle_server(self):
        """
        TODO
        :return:
        """

        server_dialog = QDialog(self)
        server_dialog.setWindowTitle('Server Configuration')
        server_dialog.setMinimumSize(250, 100)

        layout = QGridLayout()
        server_dialog.setLayout(layout)

        server_desc = QLabel(
            '<b>Server:</b> Here you can define alignak server url. '
            '<b>Be sure to enter a valid address</b>'
        )
        server_desc.setWordWrap(True)
        layout.addWidget(server_desc)

        server_url = QLineEdit()
        server_url.setPlaceholderText('alignak server url')
        server_url.setText(get_app_config('Backend', 'alignak_url'))
        layout.addWidget(server_url)

        valid_btn = QPushButton('Valid')
        valid_btn.clicked.connect(server_dialog.accept)
        layout.addWidget(valid_btn)

        if server_dialog.exec_() == QDialog.Accepted:
            set_app_config('Backend', 'alignak_url', str(server_url.text()).rstrip())
