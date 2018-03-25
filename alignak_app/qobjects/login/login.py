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
from alignak_app.qobjects.login.proxy import ProxyQDialog

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
        self.username_line = QLineEdit()
        self.password_line = QLineEdit()
        self.proxies = {}
        self.offset = None

    def create_widget(self):
        """
        Create widget login

        """

        # Main status_layout
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

        # Alignak server
        login_label = QLabel(_('Configure Alignak server'))
        login_layout.addWidget(login_label, 2, 0, 1, 1)
        login_layout.setAlignment(login_label, Qt.AlignRight)

        server_btn = QPushButton()
        server_btn.clicked.connect(self.handle_server)
        server_btn.setFixedSize(35, 35)
        server_btn.setIcon(QIcon(settings.get_image('server_settings')))
        server_btn.setToolTip(_('Configure Alignak Server'))
        login_layout.addWidget(server_btn, 2, 1, 1, 1)

        # Proxy settings
        proxy_lbl = QLabel(_('Configure Proxy'))
        login_layout.addWidget(proxy_lbl, 3, 0, 1, 1)
        login_layout.setAlignment(proxy_lbl, Qt.AlignRight)

        proxy_btn = QPushButton()
        proxy_btn.setIcon(QIcon(settings.get_image('password')))
        proxy_btn.setToolTip(_('Configure your Proxy'))
        proxy_btn.setFixedSize(35, 35)
        proxy_btn.clicked.connect(self.handle_proxy)
        login_layout.addWidget(proxy_btn, 3, 1, 1, 1)

        # Connection label
        connection_lbl = QLabel()
        connection_lbl.setText(_('<b>Log-in</b> to use the application'))
        connection_lbl.setWordWrap(True)
        login_layout.addWidget(connection_lbl, 4, 0, 1, 2)

        # Username field
        self.username_line.setFixedHeight(25)
        self.username_line.setPlaceholderText(_('username...'))
        login_layout.addWidget(self.username_line, 5, 0, 1, 2)

        # Password field
        self.password_line.setFixedHeight(25)
        self.password_line.setPlaceholderText(_('password...'))
        self.password_line.setEchoMode(QLineEdit.Password)
        login_layout.addWidget(self.password_line, 6, 0, 1, 2)

        # Login button
        login_button = QPushButton(_('LOGIN'), self)
        login_button.clicked.connect(self.accept_login)
        login_button.setObjectName('valid')
        login_button.setMinimumHeight(30)
        login_button.setDefault(True)
        login_layout.addWidget(login_button, 7, 0, 1, 2)

        main_layout.addWidget(login_widget)
        self.setLayout(main_layout)

        center_widget(self)

        if settings.get_config('Alignak', 'proxy_user'):
            self.handle_proxy()

    def accept_login(self):
        """
        Accept Login or not if backend is connected

        """

        username = str(self.username_line.text())
        password = str(self.password_line.text())

        # Set proxy only if in config
        if not self.proxies and settings.get_config('Alignak', 'proxy'):
            self.set_proxy_settings()

        if app_backend.login(username, password, proxies=self.proxies):
            self.accept()
        else:
            self.reject()

    def set_proxy_settings(self, proxy_password=None):
        """
        Set the proxy settings, with password if given

        :param proxy_password: the pasword of proxy
        :type proxy_password: str
        """

        if settings.get_config('Alignak', 'proxy_user'):
            # Model is: {'http': 'http://user:pass@proxy:port'}
            protocol, address, port = settings.get_config('Alignak', 'proxy').split(':')
            proxy_user = settings.get_config('Alignak', 'proxy_user')
            address = address.replace('//', '')
            proxy = {
                protocol: '%s://%s:%s@%s:%s' %
                          (protocol, proxy_user, proxy_password, address, port)
            }
            self.proxies = proxy
        elif settings.get_config('Alignak', 'proxy'):
            protocol = settings.get_config('Alignak', 'proxy').split(':')[0]
            self.proxies = {protocol: settings.get_config('Alignak', 'proxy')}
        else:
            self.proxies = {}

    def handle_proxy(self):  # pragma: no cover - not testable
        """
        Handle Proxy QDialog display and set proxies for login

        """

        proxy_dialog = ProxyQDialog()
        proxy_dialog.initialize_dialog()

        self.proxies = None

        if proxy_dialog.exec_() == ProxyQDialog.Accepted:
            proxy_address = proxy_dialog.proxy_address.text().rstrip()
            proxy_user = proxy_dialog.proxy_user.text().rstrip()
            proxy_password = proxy_dialog.proxy_password.text().rstrip()

            # Save proxy and user proxy for next login
            settings.set_config('Alignak', 'proxy', proxy_address)
            settings.set_config('Alignak', 'proxy_user', proxy_user)

            self.set_proxy_settings(proxy_password)

    @staticmethod
    def handle_server():  # pragma: no cover - not testable
        """
        Handle for Server QDialog and set alignak backend server settings

        """

        server_dialog = ServerQDialog()
        server_dialog.initialize_dialog()

        if server_dialog.exec_() == QDialog.Accepted:
            backend_url = '%(url)s:' + str(server_dialog.server_port.text()).rstrip()
            settings.set_config('Alignak', 'backend', backend_url)
            settings.set_config(
                'Alignak', 'url', str(server_dialog.server_url.text()).rstrip())
            settings.set_config(
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
