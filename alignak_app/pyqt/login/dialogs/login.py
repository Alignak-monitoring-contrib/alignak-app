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
    Login manage login form
"""

from logging import getLogger

from PyQt5.Qt import QLabel, QVBoxLayout, QGridLayout, QLineEdit
from PyQt5.Qt import QWidget, QDialog, QPushButton, Qt, QIcon

from alignak_app import __version__
from alignak_app.core.utils.config import app_css, get_image
from alignak_app.core.utils.config import edit_setting_value
from alignak_app.pyqt.common.widgets import get_logo_widget, center_widget
from alignak_app.pyqt.login.dialogs.server import ServerQDialog

logger = getLogger(__name__)


class LoginQDialog(QDialog):
    """
        Class who create login QDialog.
    """

    def __init__(self, parent=None):
        super(LoginQDialog, self).__init__(parent)
        self.setWindowTitle('Login to Alignak')
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet(app_css)
        self.setWindowIcon(QIcon(get_image('icon')))
        self.setObjectName('dialog')
        self.setFixedSize(300, 330)
        # Fields
        self.backend_url = None
        self.username_line = None
        self.password_line = None
        self.offset = None
        self.connection_lbl = QLabel(_('Type your Alignak username and password.'))

    def create_widget(self):
        """
        Create widget login

        """

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        main_layout.addWidget(get_logo_widget(self, _('Login')))

        # Login QWidget
        login_widget = QWidget(self)
        login_widget.setObjectName('dialog')
        login_layout = QGridLayout()
        login_widget.setLayout(login_layout)

        # _ = init_localization()
        title = QLabel(
            _('Welcome to Alignak-app')
        )
        title.setObjectName('title')
        title.setContentsMargins(1, 1, 1, 1)
        login_layout.addWidget(title, 0, 0, 1, 2)
        login_layout.setAlignment(title, Qt.AlignCenter)

        version = QLabel(_('Version %s') % __version__)
        login_layout.addWidget(version, 1, 0, 1, 2)
        login_layout.setAlignment(version, Qt.AlignCenter | Qt.AlignTop)

        # Welcome text
        login_label = QLabel(_('<b>Log-in</b> to use the application'))
        login_layout.addWidget(login_label, 2, 0, 1, 1)
        login_layout.setAlignment(login_label, Qt.AlignCenter)

        # Server button
        server_btn = QPushButton()
        server_btn.clicked.connect(self.handle_server)
        server_btn.setFixedSize(25, 25)
        server_btn.setIcon(QIcon(get_image('server_settings')))
        server_btn.setToolTip(_('Modify Alignak Server'))
        login_layout.addWidget(server_btn, 2, 1, 1, 1)

        # Connection label
        self.connection_lbl.setWordWrap(True)
        login_layout.addWidget(self.connection_lbl, 3, 0, 1, 2)

        # Username field
        self.username_line = QLineEdit(self)
        self.username_line.setPlaceholderText(_('Username'))
        login_layout.addWidget(self.username_line, 4, 0, 1, 2)

        # Password field
        self.password_line = QLineEdit(self)
        self.password_line.setPlaceholderText(_('Password'))
        self.password_line.setEchoMode(QLineEdit.Password)
        login_layout.addWidget(self.password_line, 5, 0, 1, 2)

        # Login button
        login_button = QPushButton(_('LOGIN'), self)
        login_button.clicked.connect(self.accept)
        login_button.setObjectName('valid')
        login_button.setMinimumHeight(30)
        login_button.setDefault(True)
        login_layout.addWidget(login_button, 6, 0, 1, 2)

        main_layout.addWidget(login_widget)
        self.setLayout(main_layout)

        center_widget(self)

    @staticmethod
    def handle_server():
        """
        Handle for server button

        """

        server_dialog = ServerQDialog()
        server_dialog.initialize_dialog()

        if server_dialog.exec_() == QDialog.Accepted:
            backend_url = '%(url)s:' + str(server_dialog.server_port.text()).rstrip()
            edit_setting_value('Alignak', 'backend', backend_url)
            edit_setting_value('Alignak', 'url', str(server_dialog.server_url.text()).rstrip())
            edit_setting_value(
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
