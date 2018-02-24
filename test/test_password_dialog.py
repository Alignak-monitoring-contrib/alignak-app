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

from alignak_app.utils.config import settings
from alignak_app.locales.locales import init_localization

from alignak_app.qobjects.dock.password import PasswordQDialog

settings.init_config()
init_localization()


class TestPasswordQDialog(unittest2.TestCase):
    """
        This file test the PasswordQDialog classes.
    """

    @classmethod
    def setUpClass(cls):
        """Create QApplication"""
        try:
            cls.app = QApplication(sys.argv)
        except:
            pass

    def test_about_dialog(self):
        """Initialize Password QDialog"""

        under_test = PasswordQDialog()

        self.assertIsNotNone(under_test.pass_edit)
        self.assertIsNotNone(under_test.confirm_edit)
        self.assertIsNotNone(under_test.help_label)

        under_test.initialize()

        self.assertIsNotNone(under_test.pass_edit)
        self.assertIsNotNone(under_test.confirm_edit)
        self.assertIsNotNone(under_test.help_label)
        self.assertEqual(
            'Your password must contain at least 5 characters.',
            under_test.help_label.text()
        )

    def test_handle_confirm(self):
        """Confirm Password"""

        under_test = PasswordQDialog()

        # Passwords do not match
        under_test.pass_edit.setText('password1')
        under_test.confirm_edit.setText('password2')

        under_test.handle_confirm()

        self.assertEqual('Passwords do not match !', under_test.help_label.text())

        # Password is too short
        under_test.pass_edit.setText('pass')
        under_test.confirm_edit.setText('pass')

        under_test.handle_confirm()

        self.assertEqual(
            'Your password must contain at least 5 characters.',
            under_test.help_label.text()
        )
