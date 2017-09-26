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
from alignak_app.user.user_manager import UserManager
from alignak_app.core.locales import init_localization

from PyQt5.QtWidgets import QApplication


class TestUserManager(unittest2.TestCase):
    """
        This file test the UserManager class.
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

    def test_create_user_profile(self):
        """Create UserProfile QWidget"""

        under_test = UserManager(self.app_backend)

        self.assertFalse(under_test.user_widget)
        self.assertTrue(under_test.app_backend)

        under_test.create_user_profile()

        self.assertTrue(under_test.user_widget)
        self.assertTrue(under_test.app_backend)

    def test_show_user_widget(self):
        """Show User QWidget"""

        under_test = UserManager(self.app_backend)

        self.assertFalse(under_test.user_widget)
        self.assertTrue(under_test.app_backend)

        under_test.show_user_widget()

        self.assertTrue(under_test.user_widget)
        self.assertTrue(under_test.app_backend)