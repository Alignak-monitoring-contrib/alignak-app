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

import sys

import unittest2

from alignak_app.core.utils import init_config
from alignak_app.synthesis.host_view import HostView
from alignak_app.core.backend import AppBackend

try:
    __import__('PyQt5')
    from PyQt5.QtWidgets import QApplication, QPushButton
    from PyQt5.QtWidgets import QWidget, QLabel
except ImportError:
    from PyQt4.Qt import QApplication, QPushButton
    from PyQt4.QtWidgets import QWidget, QLabel


class TestServicesView(unittest2.TestCase):
    """
        This file test the ServicesView class.
    """

    init_config()

    app_backend = AppBackend()
    app_backend.login()

    @classmethod
    def setUpClass(cls):
        """Create QApplication"""
        try:
            cls.app = QApplication(sys.argv)
            cls.widget = QWidget()
        except:
            pass

    def test_init_view(self):
        """Init Host View"""

        under_test = HostView(parent=self.widget)

        self.assertIsNone(under_test.app_backend)
        self.assertFalse(under_test.labels)
        self.assertIsNone(under_test.layout)
        self.assertIsNone(under_test.host)
        self.assertIsNone(under_test.ack_button)
        self.assertIsNone(under_test.down_button)
        self.assertIsNotNone(under_test.endpoints)

        under_test.init_view(self.app_backend)

        self.assertIsNotNone(under_test.app_backend)

        self.assertTrue(under_test.labels)
        for label in under_test.labels:
            self.assertIsInstance(under_test.labels[label], QLabel)

        self.assertIsNotNone(under_test.layout)
        self.assertIsNone(under_test.host)
        self.assertIsNotNone(under_test.ack_button)
        self.assertIsNotNone(under_test.down_button)
        self.assertIsNotNone(under_test.endpoints)

    def test_update_view(self):
        """Update Host View"""

        under_test = HostView(parent=self.widget)

        under_test.init_view(self.app_backend)

        data = self.app_backend.get_all_host_data('always_down')

        self.assertFalse(under_test.host)

        under_test.update_view(data)

        self.assertTrue(under_test.host)
        self.assertEqual(
            '<h3>Always Down</h3>',
            under_test.labels['name'].text()
        )
        self.assertEqual(
            data['host']['ls_output'],
            under_test.labels['output'].text()
        )
