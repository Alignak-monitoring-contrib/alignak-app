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

import sys

from logging import getLogger

from alignak_app import __short_version__
from alignak_app.core.backend import AppBackend, Backend
from alignak_app.core.utils import get_app_config, set_app_config, init_config
from alignak_app.core.utils import get_css, get_image_path
from alignak_app.widgets.banner import send_banner


from PyQt5.QtWidgets import QWidget, QDialog, QApplication  # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QPushButton, QGridLayout  # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout  # pylint: disable=no-name-in-module
from PyQt5.Qt import QLineEdit, Qt, QIcon, QLabel, QPixmap  # pylint: disable=no-name-in-module


logger = getLogger(__name__)


class AppLogin(QDialog):
    """
        Class who create login QDialog.
    """

    def __init__(self, parent=None):
        super(AppLogin, self).__init__(parent)
        self.setWindowTitle('Login to Alignak')
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet(get_css())
        self.setWindowIcon(QIcon(get_image_path('icon')))
        self.setFixedSize(300, 330)
        # Fields
        self.app_backend = AppBackend()
        self.backend_url = None
        self.username_line = None
        self.password_line = None
        self.offset = None

    def showEvent(self, _):
        """ QDialog.showEvent(QShowEvent) """

        self.username_line.setFocus()

    def create_widget(self):
        """
        Create widget login

        """

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        main_layout.addWidget(self.get_logo_widget(self))

        title = QLabel(
            '<h2>Welcome to Alignak-app</h2><span style="text-align:center;">Version %s</span>'
            % __short_version__
        )
        title.setObjectName('title_login')
        main_layout.addWidget(title)
        main_layout.setAlignment(title, Qt.AlignCenter)

        # Login QWidget
        login_widget = QWidget(self)
        login_widget.setObjectName('login')
        login_layout = QGridLayout(login_widget)

        # Configuration button
        refresh_conf_btn = QPushButton()
        refresh_conf_btn.clicked.connect(init_config)
        refresh_conf_btn.setFixedSize(25, 25)
        refresh_conf_btn.setIcon(QIcon(get_image_path('refresh')))
        refresh_conf_btn.setToolTip('Reload configuration')
        login_layout.addWidget(refresh_conf_btn, 2, 1, 1, 1)

        # Server button
        server_btn = QPushButton()
        server_btn.clicked.connect(self.handle_server)
        server_btn.setFixedSize(25, 25)
        server_btn.setIcon(QIcon(get_image_path('host')))
        server_btn.setToolTip('Modify Alignak Server')
        login_layout.addWidget(server_btn, 2, 2, 1, 1)

        # Welcome text
        login_label = QLabel('<b>Log-in</b> to use the application')
        login_layout.addWidget(login_label, 2, 0, 1, 1)
        login_layout.setAlignment(login_label, Qt.AlignCenter)

        # Username field
        self.username_line = QLineEdit(self)
        self.username_line.setPlaceholderText('Username')
        login_layout.addWidget(self.username_line, 3, 0, 1, 3)

        # Password field
        self.password_line = QLineEdit(self)
        self.password_line.setPlaceholderText('Password')
        self.password_line.setEchoMode(QLineEdit.Password)
        login_layout.addWidget(self.password_line, 4, 0, 1, 3)

        # Login button
        login_button = QPushButton('LOGIN', self)
        login_button.clicked.connect(self.handle_login)
        login_button.setObjectName('valid')
        login_button.setMinimumHeight(30)
        login_button.setDefault(True)
        login_layout.addWidget(login_button, 5, 0, 1, 3)

        main_layout.addWidget(login_widget)
        self.setLayout(main_layout)

        self.center(self)

    @staticmethod
    def center(widget):
        """
        Center QWidget

        """

        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        center = QApplication.desktop().screenGeometry(screen).center()
        widget.move(center.x() - (widget.width() / 2), center.y() - (widget.height() / 2))

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
        logo_widget.setObjectName('title')
        logo_layout = QHBoxLayout()
        logo_widget.setLayout(logo_layout)

        logo_label = QLabel()
        logo_label.setPixmap(QPixmap(get_image_path('alignak')))
        logo_label.setFixedSize(121, 35)
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

    def handle_login(self):
        """
        Handle for login button

        """

        username = self.username_line.text()
        password = self.password_line.text()

        self.app_backend.backend = Backend(get_app_config('Alignak', 'backend'))

        resp = self.app_backend.login(str(username), str(password))

        if resp:
            send_banner('OK', 'Welcome %s, you are connected to Alignak Backend' % username)
            self.app_backend.user['username'] = str(username)
            self.app_backend.user['token'] = str(self.app_backend.backend.token)
            self.accept()
        else:
            send_banner('WARN', 'Backend connection refused...', duration=10000)
            logger.warning('Connection informations are not accepted !')

    def handle_server(self):
        """
        Handle for server button

        """

        server_dialog = QDialog()
        server_dialog.setWindowTitle('Server Configuration')
        server_dialog.setWindowFlags(Qt.FramelessWindowHint)
        server_dialog.setStyleSheet(get_css())
        server_dialog.setFixedSize(300, 300)

        main_layout = QVBoxLayout(server_dialog)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.get_logo_widget(server_dialog))

        server_widget = QWidget(self)
        server_widget.setObjectName('login')
        server_layout = QGridLayout(server_widget)

        # Description
        desc_label = QLabel(
            '<h3>Alignak Backend</h3><p>Here you can define alignak settings.</p>'
            '<b>Be sure to enter a valid address</b>'
        )
        desc_label.setWordWrap(True)
        server_layout.addWidget(desc_label, 0, 0, 1, 3)

        # Server URL
        server_layout.addWidget(QLabel('Server'), 1, 0, 1, 1)

        server_url = QLineEdit()
        server_url.setPlaceholderText('alignak backend url')
        server_url.setText(get_app_config('Alignak', 'url'))
        server_layout.addWidget(server_url, 1, 1, 1, 2)

        # Server Port
        server_layout.addWidget(QLabel('Port'), 2, 0, 1, 1)

        server_port = QLineEdit()
        server_port.setPlaceholderText('alignak backend port')
        cur_port = get_app_config('Alignak', 'backend').split(':')[2]
        server_port.setText(cur_port)
        server_layout.addWidget(server_port, 2, 1, 1, 2)

        # Server Processes
        server_layout.addWidget(QLabel('Processes'), 3, 0, 1, 1)

        server_proc = QLineEdit()
        if 'win32' in sys.platform:
            server_proc.setEnabled(False)
        server_proc.setPlaceholderText('alignak backend processes')
        cur_proc = get_app_config('Alignak', 'processes')
        server_proc.setText(cur_proc)
        server_layout.addWidget(server_proc, 3, 1, 1, 2)

        # Valid Button
        valid_btn = QPushButton('Valid')
        valid_btn.clicked.connect(server_dialog.accept)
        server_layout.addWidget(valid_btn, 4, 0, 1, 3)

        main_layout.addWidget(server_widget)

        self.center(server_widget)

        if server_dialog.exec_() == QDialog.Accepted:
            backend_url = '%(url)s:' + str(server_port.text()).rstrip()
            set_app_config('Alignak', 'backend', backend_url)
            set_app_config('Alignak', 'url', str(server_url.text()).rstrip())
            set_app_config('Alignak', 'processes', str(server_proc.text()).rstrip())

    def mousePressEvent(self, event):
        """ QWidget.mousePressEvent(QMouseEvent) """

        self.offset = event.pos()

    def mouseMoveEvent(self, event):
        """ QWidget.mousePressEvent(QMouseEvent) """

        try:
            x = event.globalX()
            y = event.globalY()
            x_w = self.offset.x()
            y_w = self.offset.y()
            self.move(x - x_w, y - y_w)
        except AttributeError as e:
            logger.warning('Move Event %s: %s', self.objectName(), str(e))
