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
from PyQt5.Qt import QApplication, QLineEdit, QTimer, QWidget

from alignak_app.backend.backend import app_backend
from alignak_app.utils.config import settings
from alignak_app.locales.locales import init_localization

from alignak_app.qobjects.login.proxy import ProxyQDialog


class TestProxyQDialog(unittest2.TestCase):
    """
        This file test methods of ProxyQDialog class object
    """

    settings.init_config()
    init_localization()
    app_backend.login()

    @classmethod
    def setUpClass(cls):
        """Create QApplication"""
        try:
            cls.app = QApplication(sys.argv)
        except:
            pass

    def test_initialize_proxy_dialog(self):
        """Initialize ProxyQDialog"""

        under_test = ProxyQDialog()

        self.assertEqual('dialog', under_test.objectName())

        self.assertIsNotNone(under_test.proxy_address)
        self.assertIsInstance(under_test.proxy_address, QLineEdit)
        self.assertIsNotNone(under_test.proxy_user)
        self.assertIsInstance(under_test.proxy_user, QLineEdit)
        self.assertIsNotNone(under_test.proxy_password)
        self.assertIsInstance(under_test.proxy_password, QLineEdit)

        self.assertIsNone(under_test.offset)

        under_test.initialize_dialog()

        self.assertEqual('dialog', under_test.objectName())

        self.assertIsNotNone(under_test.proxy_address)
        self.assertIsInstance(under_test.proxy_address, QLineEdit)
        self.assertIsNotNone(under_test.proxy_user)
        self.assertIsInstance(under_test.proxy_user, QLineEdit)
        self.assertIsNotNone(under_test.proxy_password)
        self.assertIsInstance(under_test.proxy_password, QLineEdit)
        self.assertEqual(QLineEdit.Password, under_test.proxy_password.echoMode())

        self.assertIsNone(under_test.offset)

    def test_get_proxy_widget(self):
        """Get Proxy QWidget"""

        under_test = ProxyQDialog()

        self.assertIsInstance(under_test.get_proxy_widget(), QWidget)

    def test_accept_proxy(self):
        """Accept Proxy QDialog"""

        under_test = ProxyQDialog()

        under_test.initialize_dialog()

        timer = QTimer()
        timer.timeout.connect(under_test.accept_proxy)
        timer.start(0.5)

        # When all proxy settings are empties, dialog Accepted
        self.assertTrue(ProxyQDialog.Accepted == under_test.exec())

        # Proxy address is set, dialog Accepted
        under_test.proxy_address.setText('http://127.0.0.1:8000')
        timer.start(0.5)

        self.assertTrue(ProxyQDialog.Accepted == under_test.exec())
