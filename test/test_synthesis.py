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
from alignak_app.synthesis.synthesis import Synthesis

from PyQt5.QtWidgets import QApplication, QWidget


class TestServicesView(unittest2.TestCase):
    """
        This file test the Synthesis class.
    """

    init_config()

    app_backend = AppBackend()
    app_backend.login()

    @classmethod
    def setUpClass(cls):
        """Create QApplication"""
        try:
            cls.app = QApplication(sys.argv)
            cls.widget = QWidget()
        except:
            pass

    def test_initialize(self):
        """Initialize Synthesis"""

        under_test = Synthesis()

        self.assertFalse(under_test.app_backend)
        self.assertFalse(under_test.action_manager)
        self.assertIsNone(under_test.host_synthesis)
        self.assertTrue(under_test.line_search)

        under_test.initialize(self.app_backend)

        self.assertTrue(under_test.app_backend)
        self.assertTrue(under_test.action_manager)
        self.assertIsNone(under_test.host_synthesis)
        self.assertTrue(under_test.line_search)