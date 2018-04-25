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
from PyQt5.Qt import QApplication, QLineEdit

from alignak_app.backend.backend import app_backend
from alignak_app.utils.config import settings
from alignak_app.locales.locales import init_localization

from alignak_app.qobjects.login.server import ServerQDialog


class TestServerQDialog(unittest2.TestCase):
    """
        This file test methods of ServerQDialog class object
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

    def test_initialize_server_dialog(self):
        """Initialize ServerQDialog"""

        under_test = ServerQDialog()

        self.assertIsInstance(under_test.server_proc, QLineEdit)
        self.assertEqual('', under_test.server_proc.text())

        self.assertIsInstance(under_test.server_port, QLineEdit)
        self.assertEqual('', under_test.server_port.text())

        self.assertIsInstance(under_test.server_url, QLineEdit)
        self.assertEqual('', under_test.server_url.text())

        self.assertIsInstance(under_test.webservice_url, QLineEdit)
        self.assertEqual('', under_test.webservice_url.text())

        self.assertIsNone(under_test.offset)
        self.assertEqual('dialog', under_test.objectName())

        under_test.initialize_dialog()

        # After initialization,
        # QLineEdit texts must be equal to what is defined in the configuration file
        self.assertIsInstance(under_test.server_proc, QLineEdit)
        self.assertEqual(
            settings.get_config('Alignak', 'processes'),
            under_test.server_proc.text()
        )

        self.assertIsInstance(under_test.server_port, QLineEdit)
        self.assertEqual(
            settings.get_config('Alignak', 'backend').split(':')[2],
            under_test.server_port.text()
        )

        self.assertIsInstance(under_test.server_url, QLineEdit)
        self.assertEqual(
            settings.get_config('Alignak', 'url'),
            under_test.server_url.text()
        )

        self.assertIsInstance(under_test.webservice_url, QLineEdit)
        self.assertEqual(
            settings.get_config('Alignak', 'webservice'),
            under_test.webservice_url.text()
        )
