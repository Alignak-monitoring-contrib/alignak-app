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

import unittest2
import sys

from alignak_app.app import AlignakApp, QIcon

try:
    __import__('PyQt5')
    from PyQt5.QtWidgets import QApplication
except ImportError:
    from PyQt4.Qt import QApplication


class TestApp(unittest2.TestCase):
    """
        This file test methods of AlignakApp class.
    """

    @classmethod
    def setUpClass(cls):
        """Create QApplication"""

        try:
            cls.app = QApplication(sys.argv)
        except:
            pass

    def test_app_main(self):
        """Build Alignak-App"""

        under_test = AlignakApp()

        self.assertIsNone(under_test.tray_icon)
        self.assertIsNone(under_test.notifier)

        # Build alignak_app
        under_test.start()

        self.assertIsNotNone(under_test.tray_icon)
        self.assertIsNotNone(under_test.notifier)

    def test_get_icon(self):
        """Get Icon"""

        under_test = AlignakApp()

        icon = under_test.get_icon()

        self.assertIsInstance(icon, QIcon, 'This is a test for QIcon')
