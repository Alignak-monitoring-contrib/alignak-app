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

from alignak_app.app import AlignakApp
from alignak_app.core.data_manager import data_manager
from alignak_app.items.item_user import User

from PyQt5.QtWidgets import QApplication


class TestApp(unittest2.TestCase):
    """
        TODO This file test methods of AlignakApp class.
    """

    # data_manager.database['user'] = User()

    @classmethod
    def setUpClass(cls):
        """Create QApplication"""

        try:
            cls.app = QApplication(sys.argv)
        except:
            pass

    def test_app_main(self):
        """Build Alignak-App"""

        under_test = AlignakApp()

        self.assertIsNone(under_test.tray_icon)
        self.assertFalse(under_test.reconnect_mode)

        # Build alignak_app
        under_test.reconnect_to_backend('ERROR')

        self.assertIsNone(under_test.tray_icon)
        self.assertTrue(under_test.reconnect_mode)
