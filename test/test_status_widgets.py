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
from PyQt5.Qt import QApplication, QWidget

from alignak_app.backend.backend import app_backend
from alignak_app.utils.config import settings
from alignak_app.locales.locales import init_localization

from alignak_app.qobjects.dock.status import StatusQDialog, StatusQWidget


class TestStatus(unittest2.TestCase):
    """
        This file test methods of StatusQDialog class object
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

    def test_initialize_status_qdialog(self):
        """Initialize StatusQDialog"""

        under_test = StatusQDialog()

        self.assertIsNotNone(under_test.app_widget)
        self.assertIsNotNone(under_test.layout)
        self.assertFalse(under_test.labels)

        under_test.initialize()

    def test_get_buttons_widget(self):
        """Get Buttons Status from StatusQDialog"""

        status_dialog_test = StatusQDialog()

        under_test = status_dialog_test.get_buttons_widget()

        self.assertIsInstance(under_test, QWidget)

    def test_initialize_status_qwidget(self):
        """Initialize StatusQWidget"""

        under_test = StatusQWidget()

        self.assertIsNotNone(under_test.backend_connected)

        self.assertIsNotNone(under_test.daemons_status)

        self.assertIsNotNone(under_test.refresh_timer)
        self.assertFalse(under_test.refresh_timer.isActive())
        self.assertIsNotNone(under_test.status_dialog)

        self.assertIsInstance(under_test.status_dialog, StatusQDialog)

        under_test.initialize()

        self.assertTrue(under_test.refresh_timer.isActive())
