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

import unittest2
import sys

from alignak_app.widgets.banner import Banner

from PyQt5.QtWidgets import QApplication


class TestBanner(unittest2.TestCase):
    """
        This file test methods of Banner class.
    """

    @classmethod
    def setUpClass(cls):
        """Create QApplication"""

        try:
            cls.app = QApplication(sys.argv)
        except:
            pass

    def test_banner_creation(self):
        """Create Banner"""

        under_test = Banner()

        self.assertIsNotNone(under_test.banner_closed)

        self.assertIsNotNone(under_test.animation)
        self.assertIsNotNone(under_test.banner_type)
        self.assertIsNone(under_test.layout())

        under_test.create_banner('OK', 'test message')
        assert '#27ae60' in under_test.styleSheet()

        self.assertIsNotNone(under_test.animation)
        self.assertIsNotNone(under_test.banner_type)

        self.assertIsNotNone(under_test.layout())

    def test_all_banner_title(self):
        """All Banner Titles"""

        under_test_ok = Banner()
        under_test_ok.create_banner('OK', 'test message')
        assert '#27ae60' in under_test_ok.styleSheet()

        under_test_info = Banner()
        under_test_info.create_banner('INFO', 'test message')
        assert '#3884c3' in under_test_info.styleSheet()

        under_test_warn = Banner()
        under_test_warn.create_banner('WARN', 'test message')
        assert '#e67e22' in under_test_warn.styleSheet()

        under_test_alert = Banner()
        under_test_alert.create_banner('ALERT', 'test message')
        assert '#e74c3c' in under_test_alert.styleSheet()

    def test_wrong_title_banner(self):
        """Banner with Wrong Title"""

        under_test = Banner()
        self.assertIsNone(under_test.layout())

        under_test.create_banner('NONE', 'test message')
        assert '#383838' in under_test.styleSheet()

        self.assertIsNotNone(under_test.layout())