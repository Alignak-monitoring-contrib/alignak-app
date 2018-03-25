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

import sys

import unittest2
from PyQt5.Qt import QApplication, QTimer, QLineEdit

from alignak_app.utils.config import settings

from alignak_app.qobjects.login.login import LoginQDialog


class TestLoginQDialog(unittest2.TestCase):
    """
        This file test the LoginQDialog class.
    """

    settings.init_config()

    @classmethod
    def setUpClass(cls):
        """Create QApplication"""
        try:
            cls.app = QApplication(sys.argv)
        except:
            pass

    def test_initialize_login_dialog(self):
        """Initialize LoginQDialog"""

        under_test = LoginQDialog()

        self.assertIsInstance(under_test.username_line, QLineEdit)
        self.assertIsInstance(under_test.password_line, QLineEdit)
        self.assertFalse(under_test.proxies)
        self.assertIsNone(under_test.offset)

        under_test.create_widget()

        self.assertFalse(under_test.proxies)
        self.assertIsNone(under_test.offset)

    def test_accept_login(self):
        """QDialog Accept Login"""

        under_test = LoginQDialog()
        under_test.create_widget()

        timer = QTimer()
        timer.timeout.connect(under_test.accept_login)
        timer.start(0.5)

        # If login failed, Rejected
        self.assertEqual(LoginQDialog.Rejected, under_test.exec())

        # Set username and password for login
        under_test.username_line.setText('admin')
        under_test.password_line.setText('admin')

        timer.start(0.5)
        self.assertEqual(LoginQDialog.Accepted, under_test.exec())

    def test_set_proxy_settings(self):
        """LoginQDialog Set Proxy Settings"""

        under_test = LoginQDialog()
        under_test.create_widget()

        # Set Proxy address
        self.assertFalse(under_test.proxies)
        settings.set_config('Alignak', 'proxy', 'http://127.0.0.1:5000')

        under_test.set_proxy_settings()

        # Proxy is set in "proxies" QDialog
        self.assertEqual({'http': 'http://127.0.0.1:5000'}, under_test.proxies)

        # Set user Proxy
        settings.set_config('Alignak', 'proxy_user', 'user')

        # Give password in parameter
        under_test.set_proxy_settings('password')

        # Proxy user and password are set in "proxies" QDialog
        self.assertEqual({'http': 'http://user:password@127.0.0.1:5000'}, under_test.proxies)

        # Back settings for other tests
        settings.set_config('Alignak', 'proxy', '')
        settings.set_config('Alignak', 'proxy_user', '')
        settings.set_config('Alignak', 'proxy_password', '')

        under_test.set_proxy_settings()

        # QDialog "proxies" is empty (False)
        self.assertFalse(under_test.proxies)





