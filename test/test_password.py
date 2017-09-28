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

from alignak_app.core.utils import init_config
from alignak_app.core.backend import AppBackend
from alignak_app.user.password import PasswordDialog
from alignak_app.core.locales import init_localization

from PyQt5.QtWidgets import QApplication, QWidget


class TestUserManager(unittest2.TestCase):
    """
       TODO This file test the PasswordDialog class.
    """

    init_config()
    init_localization()

    @classmethod
    def setUpClass(cls):
        """Create QApplication"""
        try:
            cls.app = QApplication(sys.argv)
            cls.app_backend = AppBackend()
            cls.app_backend.login()
        except:
            pass

    def test_initialize(self):
        """Initialize PasswordDialog"""

        under_test = PasswordDialog()

        self.assertIsNone(under_test.pass_edit)
        self.assertIsNone(under_test.confirm_edit)
        self.assertIsNone(under_test.help_label)

        under_test.initialize()

        self.assertIsNotNone(under_test.pass_edit)
        self.assertIsNotNone(under_test.confirm_edit)
        self.assertIsNotNone(under_test.help_label)

    def test_center(self):
        """Center PasswordDialog"""

        under_test = PasswordDialog()

        old_pos_test = under_test.pos()

        self.assertFalse(old_pos_test)

        under_test.center(under_test)

        new_pos_test = under_test.pos()

        self.assertTrue(new_pos_test)
