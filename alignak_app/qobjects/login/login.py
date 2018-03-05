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
    Login
    +++++
    Login manage creation of QDialog for user login
"""

from logging import getLogger

from PyQt5.Qt import QLabel, QVBoxLayout, QGridLayout, QLineEdit
from PyQt5.Qt import QWidget, QDialog, QPushButton, Qt, QIcon

from alignak_app import __version__
from alignak_app.backend.backend import app_backend
from alignak_app.utils.config import settings

from alignak_app.qobjects.common.widgets import get_logo_widget, center_widget
from alignak_app.qobjects.login.server import ServerQDialog

logger = getLogger(__name__)


class LoginQDialog(QDialog):
    """
        Class who create login QDialog.
    """

    def __init__(self, parent=None):
        super(LoginQDialog, self).__init__(parent)
        self.setWindowTitle('Login to Alignak')
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet(settings.css_style)
        self.setWindowIcon(QIcon(settings.get_image('icon')))
        self.setObjectName('dialog')
        self.setFixedSize(310, 360)
        # Fields
        self.backend_url = None
        self.username_line = None
        self.password_line = None
        self.offset = None

    def create_widget(self):
        """
        Create widget login

        """

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        main_layout.addWidget(get_logo_widget(self, _('Login'), exitapp=True))

        # Login QWidget
        login_widget = QWidget(self)
        login_widget.setObjectName('dialog')
        login_layout = QGridLayout()
        login_widget.setLayout(login_layout)

        # _ = init_localization()
        title = QLabel(
            _('Welcome to Alignak-app')
        )
        title.setObjectName('itemtitle')
        title.setContentsMargins(1, 1, 1, 1)
        login_layout.addWidget(title, 0, 0, 1, 2)
        login_layout.setAlignment(title, Qt.AlignCenter)

        version = QLabel(_('Version %s') % __version__)
        version.setObjectName('subtitle')
        login_layout.addWidget(version, 1, 0, 1, 2)
        login_layout.setAlignment(version, Qt.AlignCenter | Qt.AlignTop)

        # Welcome text
        login_label = QLabel(_('Configure Alignak server'))
        login_layout.addWidget(login_label, 2, 0, 1, 1)
        login_layout.setAlignment(login_label, Qt.AlignRight)

        # Server button
        server_btn = QPushButton()
        server_btn.clicked.connect(self.handle_server)
        server_btn.setFixedSize(35, 35)
        server_btn.setIcon(QIcon(settings.get_image('server_settings')))
        server_btn.setToolTip(_('Configure Alignak Server'))
        login_layout.addWidget(server_btn, 2, 1, 1, 1)

        # Connection label
        connection_lbl = QLabel()
        connection_lbl.setText(_('<b>Log-in</b> to use the application'))
        connection_lbl.setWordWrap(True)
        login_layout.addWidget(connection_lbl, 3, 0, 1, 2)

        # Username field
        self.username_line = QLineEdit(self)
        self.username_line.setFixedHeight(25)
        self.username_line.setPlaceholderText(_('Username'))
        login_layout.addWidget(self.username_line, 4, 0, 1, 2)

        # Password field
        self.password_line = QLineEdit(self)
        self.password_line.setFixedHeight(25)
        self.password_line.setPlaceholderText(_('Password'))
        self.password_line.setEchoMode(QLineEdit.Password)
        login_layout.addWidget(self.password_line, 5, 0, 1, 2)

        # Login button
        login_button = QPushButton(_('LOGIN'), self)
        login_button.clicked.connect(self.accept_login)
        login_button.setObjectName('valid')
        login_button.setMinimumHeight(30)
        login_button.setDefault(True)
        login_layout.addWidget(login_button, 6, 0, 1, 2)

        main_layout.addWidget(login_widget)
        self.setLayout(main_layout)

        center_widget(self)

    def accept_login(self):
        """
        Accept Login or not if backend is connected

        """

        username = str(self.username_line.text())
        password = str(self.password_line.text())

        if app_backend.login(username, password):
            self.accept()
        else:
            self.reject()

    @staticmethod
    def handle_server():
        """
        Handle for server button

        """

        server_dialog = ServerQDialog()
        server_dialog.initialize_dialog()

        if server_dialog.exec_() == QDialog.Accepted:
            backend_url = '%(url)s:' + str(server_dialog.server_port.text()).rstrip()
            settings.edit_setting_value('Alignak', 'backend', backend_url)
            settings.edit_setting_value(
                'Alignak', 'url', str(server_dialog.server_url.text()).rstrip())
            settings.edit_setting_value(
                'Alignak', 'processes', str(server_dialog.server_proc.text()).rstrip()
            )

    def showEvent(self, _):
        """ QDialog.showEvent(QShowEvent) """

        self.username_line.setFocus()

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
