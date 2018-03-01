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
from PyQt5.QtWidgets import QApplication

from alignak_app.app import AppProgressBar, AppProgressQWidget


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

    def test_app_progressbar(self):
        """App Progress Bar"""

        under_test = AppProgressBar()

        self.assertEqual(under_test.minimum(), 0)
        self.assertEqual(under_test.maximum(), 0)

        under_test.set_text('test')

        self.assertEqual('test', under_test.text())

    def test_app_progress_Widget(self):
        """App Progress QWidget"""

        under_test = AppProgressQWidget()

        self.assertTrue(under_test.progress_bar)
        self.assertIsInstance(under_test.progress_bar, AppProgressBar)

        under_test.initialize()

        self.assertTrue(under_test.progress_bar)
        self.assertIsInstance(under_test.progress_bar, AppProgressBar)
