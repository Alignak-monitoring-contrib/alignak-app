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
from alignak_app.core.locales import init_localization
from alignak_app.synthesis.synthesis import Synthesis

from PyQt5.QtWidgets import QApplication


class TestSynthesis(unittest2.TestCase):
    """
        This file test the Synthesis class.
    """

    init_config()
    init_localization()

    app_backend = AppBackend()
    app_backend.login()

    @classmethod
    def setUpClass(cls):
        """Create QApplication"""
        try:
            cls.app = QApplication(sys.argv)
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

    def test_display_host_synthesis(self):
        """Display Host Synthesis"""

        under_test = Synthesis()

        under_test.initialize(self.app_backend)

        self.assertIsNone(under_test.host_synthesis)
        self.assertTrue(under_test.update_line_edit)

        under_test.display_host_synthesis()

        # Assert "update_line_edit" is False
        self.assertIsNone(under_test.host_synthesis)
        self.assertFalse(under_test.update_line_edit)

        # Update Synthesis view to create HostSynthesis and make "update_line_edit" True
        under_test.update_synthesis_view('denice')

        self.assertIsNotNone(under_test.host_synthesis)
        self.assertFalse(under_test.update_line_edit)

        # Assert new HostSynthesis is create each time "update_synthesis_view" is called
        old_synthesis = under_test.host_synthesis

        under_test.update_synthesis_view('denice')

        new_synthesis = under_test.host_synthesis

        self.assertNotEqual(new_synthesis, old_synthesis)
