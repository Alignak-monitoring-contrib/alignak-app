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
from PyQt5.Qt import QApplication

from alignak_app.utils.config import settings

from alignak_app.qobjects.login.login import LoginQDialog


class TestLoginQDialog(unittest2.TestCase):
    """
        This file test the LoginQDialog class.
    """

    settings.init_config()

    @classmethod
    def setUpClass(cls):
        """Create QApplication"""
        try:
            cls.app = QApplication(sys.argv)
        except:
            pass

    def test_create_widget(self):
        """Inititalize AppLogin"""

        under_test = LoginQDialog()

        self.assertIsNone(under_test.username_line)
        self.assertIsNone(under_test.password_line)

        under_test.create_widget()

        self.assertIsNotNone(under_test.username_line)
        self.assertIsNotNone(under_test.password_line)
