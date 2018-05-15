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
    Proxy
    +++++
    Proxy manage creation of QDialog for Alignak backend proxy
"""

from logging import getLogger

from PyQt5.Qt import QLineEdit, Qt, QIcon, QLabel, QVBoxLayout, QWidget, QDialog, QPushButton

from alignak_app.utils.config import settings

from alignak_app.qobjects.common.widgets import get_logo_widget, center_widget
from alignak_app.qobjects.common.dialogs import MessageQDialog

logger = getLogger(__name__)


class ProxyQDialog(QDialog):
    """
        Class who create a Proxy QDialog
    """

    def __init__(self, parent=None):
        super(ProxyQDialog, self).__init__(parent)
        self.setWindowTitle(_('Proxy Configuration'))
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet(settings.css_style)
        self.setWindowIcon(QIcon(settings.get_image('icon')))
        self.setObjectName('dialog')
        self.setFixedSize(320, 380)
        # Fields
        self.proxy_address = QLineEdit()
        self.proxy_user = QLineEdit()
        self.proxy_password = QLineEdit()
        self.offset = None

    def initialize_dialog(self):
        """
        Initialize Proxy QDialog

        """

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)

        main_layout.addWidget(get_logo_widget(self, _('Proxy Settings')))

        main_layout.addWidget(self.get_proxy_widget())

        center_widget(self)

    def get_proxy_widget(self):
        """
        Return the proxy QWidget

        :return: proxy QWidget
        :rtype: QWidget
        """

        proxy_widget = QWidget()
        proxy_widget.setObjectName('dialog')
        proxy_layout = QVBoxLayout(proxy_widget)

        # Title
        title_lbl = QLabel(_('Proxy Settings'))
        title_lbl.setObjectName('itemtitle')
        proxy_layout.addWidget(title_lbl)
        proxy_layout.setAlignment(title_lbl, Qt.AlignTop)

        # Description
        desc_label = QLabel(
            _('Here you can define your proxy. Be sure to enter a valid address.')
        )
        desc_label.setWordWrap(True)
        proxy_layout.addWidget(desc_label)

        # Proxy Settings
        proxy_lbl = QLabel(_('Proxy Address with Port'))
        proxy_layout.addWidget(proxy_lbl)

        proxy = settings.get_config('Alignak', 'proxy')
        self.proxy_address.setText(proxy)
        self.proxy_address.setPlaceholderText(_('proxy adress:port...'))
        self.proxy_address.setFixedHeight(25)
        proxy_layout.addWidget(self.proxy_address)

        # Proxy User
        proxy_user_lbl = QLabel(_('Proxy User (Optional)'))
        proxy_layout.addWidget(proxy_user_lbl)

        proxy_user = settings.get_config('Alignak', 'proxy_user')
        self.proxy_user.setText(proxy_user)
        self.proxy_user.setPlaceholderText(_('proxy user...'))
        self.proxy_user.setFixedHeight(25)
        proxy_layout.addWidget(self.proxy_user)

        # Proxy Password
        proxy_password_lbl = QLabel(_('Proxy Password (Optional)'))
        proxy_layout.addWidget(proxy_password_lbl)

        if settings.get_config('Alignak', 'proxy_password'):
            self.proxy_password.setText(settings.get_config('Alignak', 'proxy_password'))
        self.proxy_password.setPlaceholderText(_('proxy password...'))
        self.proxy_password.setFixedHeight(25)
        self.proxy_password.setEchoMode(QLineEdit.Password)
        proxy_layout.addWidget(self.proxy_password)

        # Valid Button
        valid_btn = QPushButton(_('Valid'))
        valid_btn.setObjectName('valid')
        valid_btn.setMinimumHeight(30)
        valid_btn.clicked.connect(self.accept_proxy)

        proxy_layout.addWidget(valid_btn)

        return proxy_widget

    def accept_proxy(self):
        """
        Accept QDialog if proxy is valid

        """

        if self.proxy_address.text() or self.proxy_user.text() or self.proxy_password.text():
            try:
                _, _, _ = self.proxy_address.text().split(':')
                self.accept()
            except ValueError:
                self.proxy_error()
        else:
            self.accept()

    @staticmethod
    def proxy_error():  # pragma: no cover - not testable
        """
        Display a Message QDialog error

        """

        error_dialog = MessageQDialog()
        error_dialog.initialize(
            'Proxy Error', 'error', 'Wrong proxy setting !',
            'You must enter a valid address: "http://proxy:port"'
        )
        error_dialog.exec_()

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
