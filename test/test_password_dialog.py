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

from alignak_app.dialogs.password_dialog import PasswordQDialog
from alignak_app.core.utils import init_config
from alignak_app.core.locales import init_localization

from PyQt5.QtWidgets import QApplication, QWidget

init_config()
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

    def test_get_password_logo_widget(self):
        """Get Password Dialog logo Widget"""

        password_test = PasswordQDialog()

        under_test = password_test.get_logo_widget(password_test)

        self.assertIsInstance(under_test, QWidget)

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

    def test_center(self):
        """Center Password Dialog"""

        under_test = PasswordQDialog()

        old_pos_test = under_test.pos()

        self.assertFalse(old_pos_test)

        under_test.center(under_test)

        new_pos_test = under_test.pos()

        self.assertTrue(new_pos_test)
