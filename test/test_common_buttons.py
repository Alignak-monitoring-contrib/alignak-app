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
from PyQt5.Qt import QApplication, QWidget, QPushButton

from alignak_app.utils.config import settings

from alignak_app.qobjects.common.buttons import ToggleQWidgetButton

settings.init_config()


class TestCommonQPixmap(unittest2.TestCase):
    """
        This file test the Common QPixmap funtions
    """

    @classmethod
    def setUpClass(cls):
        """Create QApplication"""
        try:
            cls.app = QApplication(sys.argv)
        except:
            pass

    def test_toggle_button_init(self):
        """Initialize ToggleQWidgetButton"""

        under_test = ToggleQWidgetButton()

        self.assertIsInstance(under_test, QWidget)
        self.assertIsInstance(under_test.toggle_btn, QPushButton)
        self.assertFalse(under_test.toggle_btn.isChecked())
        self.assertEqual('', under_test.toggle_btn.text())

        under_test.initialize()

        self.assertIsInstance(under_test, QWidget)
        self.assertIsInstance(under_test.toggle_btn, QPushButton)
        self.assertTrue(under_test.toggle_btn.isChecked())
        self.assertEqual('ON', under_test.toggle_btn.text())

    def test_update_btn_state(self):
        """Update ToggleQWidgetButton state"""

        under_test = ToggleQWidgetButton()
        under_test.initialize()

        self.assertEqual('ON', under_test.toggle_btn.text())

        under_test.update_btn_state(False)

        self.assertEqual('OFF', under_test.toggle_btn.text())
        self.assertFalse(under_test.toggle_btn.isChecked())

        under_test.update_btn_state(True)

        self.assertEqual('ON', under_test.toggle_btn.text())
        self.assertTrue(under_test.toggle_btn.isChecked())

    def test_get_btn_state(self):
        """Get ToggleQWidgetButton button state"""

        under_test = ToggleQWidgetButton()
        under_test.initialize()

        self.assertTrue(under_test.get_btn_state())

        under_test.update_btn_state(True)

        self.assertTrue(under_test.get_btn_state())

        under_test.update_btn_state(False)

        self.assertFalse(under_test.get_btn_state())
