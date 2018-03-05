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

from alignak_app.utils.config import settings
from alignak_app.locales.locales import init_localization

from alignak_app.qobjects.common.widgets import get_logo_widget, center_widget, LogoQWidget

settings.init_config()
init_localization()


class TestCommonQWidget(unittest2.TestCase):
    """
        This file test the Utils Widget classes and funtions
    """

    @classmethod
    def setUpClass(cls):
        """Create QApplication"""
        try:
            cls.app = QApplication(sys.argv)
        except:
            pass

    def test_initialize_acknowledge(self):
        """Initialize LogoQWidget"""

        under_test = LogoQWidget()

        test_widget = QWidget()

        self.assertIsNone(under_test.layout())
        self.assertEqual('app_widget', under_test.objectName())
        self.assertIsNone(under_test.child_widget)

        under_test.initialize(test_widget, '', False)

        self.assertIsNotNone(under_test.layout())
        self.assertEqual('app_widget', under_test.objectName())
        self.assertIsNotNone(under_test.child_widget)

    def test_get_logo_widget(self):
        """Get LogoQWidget"""

        test_widget = QWidget()

        under_test = get_logo_widget(test_widget, '')

        self.assertIsInstance(under_test, LogoQWidget)
        self.assertIsNotNone(under_test.layout())
        self.assertEqual('app_widget', under_test.objectName())

    def test_center_widget(self):
        """Center QWidget"""

        under_test = LogoQWidget()
        old_pos = under_test.pos()

        center_widget(under_test)

        new_pos = under_test.pos()

        self.assertNotEqual(old_pos, new_pos)
