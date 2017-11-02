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
from PyQt5.QtWidgets import QApplication, QLabel

from alignak_app.core.utils.config import init_config
from alignak_app.locales.locales import init_localization
from alignak_app.pyqt.systray.dialogs.about import AboutQDialog

init_config()
init_localization()


class TestAboutQDialog(unittest2.TestCase):
    """
        This file test the AboutQDialog classes.
    """

    @classmethod
    def setUpClass(cls):
        """Create QApplication"""
        try:
            cls.app = QApplication(sys.argv)
        except:
            pass

    def test_about_dialog(self):
        """Initialize About QDialog"""

        under_test = AboutQDialog()

        self.assertIsNotNone(under_test.app_frame_model)

        under_test.initialize()

        self.assertIsNotNone(under_test.app_frame_model)
        self.assertIsNotNone(under_test.layout())

    def test_get_external_link_label(self):
        """Get External Link"""

        about_test = AboutQDialog()

        link = 'http://demo.alignak.net'

        under_test = about_test.get_external_link_label(link)

        self.assertIsInstance(under_test, QLabel)
