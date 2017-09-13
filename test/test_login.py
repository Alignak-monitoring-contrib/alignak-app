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

import sys

import unittest2

from alignak_app.core.utils import init_config
from alignak_app.widgets.login import AppLogin

from PyQt5.QtWidgets import QApplication


class TestAppLogin(unittest2.TestCase):
    """
        This file test the AppLogin class.
    """

    init_config()

    @classmethod
    def setUpClass(cls):
        """Create QApplication"""
        try:
            cls.app = QApplication(sys.argv)
        except:
            pass

    def test_create_widget(self):
        """Inititalize AppLogin"""

        under_test = AppLogin()

        self.assertIsNotNone(under_test.app_backend)
        self.assertIsNone(under_test.username_line)
        self.assertIsNone(under_test.password_line)

        under_test.create_widget()

        self.assertIsNotNone(under_test.app_backend)
        self.assertIsNotNone(under_test.username_line)
        self.assertIsNotNone(under_test.password_line)

    def test_handle_login_good_connection(self):
        """Handle Login: good credentials"""

        under_test = AppLogin()
        under_test.create_widget()

        under_test.username_line.setText('admin')
        under_test.password_line.setText('admin')

        self.assertFalse(under_test.app_backend.user)

        under_test.handle_login()

        self.assertTrue(under_test.app_backend.user)
        self.assertIsNotNone(under_test.app_backend.user['username'])
        self.assertIsNotNone(under_test.app_backend.user['token'])

    def test_handle_login_bad_connection(self):
        """Handle Login: bad credentials"""

        under_test = AppLogin()
        under_test.create_widget()

        under_test.username_line.setText('bad')
        under_test.password_line.setText('bad')

        under_test.handle_login()

        self.assertFalse(under_test.app_backend.user)
