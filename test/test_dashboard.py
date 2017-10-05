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

from alignak_app.core.utils import init_config, set_app_config
from alignak_app.core.locales import init_localization
from alignak_app.dashboard.app_dashboard import Dashboard

from PyQt5.QtWidgets import QApplication


class TestDashboard(unittest2.TestCase):
    """
        This file test the Dashboard class and by same time the DashboardFactory
    """

    init_config()
    init_localization()

    @classmethod
    def setUpClass(cls):
        """Create QApplication"""
        try:
            cls.app = QApplication(sys.argv)
        except:
            pass

    def test_initialize_dashboard(self):
        """Initialize Dashboard"""

        under_test = Dashboard()

        self.assertIsNone(under_test.dashboard_type)
        self.assertIsNotNone(under_test.dashboard_factory)

        # Create all the label
        under_test.initialize()

        self.assertEqual('state', under_test.dashboard_type.objectName())
        self.assertIsNotNone(under_test.dashboard_factory)

    def test_get_style_sheet(self):
        """Get Style Sheet according to States"""

        ok_css = "Background-color: #27ae60;"
        warning_css = "Background-color: #e67e22;"
        critical_css = "Background-color: #e74c3c;"
        none_css = "Background-color: #EEE;"

        under_test = Dashboard()

        css = {
            'OK': ok_css,
            'WARNING': warning_css,
            'CRITICAL': critical_css,
            'NONE': none_css,
        }
        states = ('OK', 'WARNING', 'CRITICAL', 'NONE')

        for state in states:
            expected_css = css[state]
            under_test.set_style_sheet(state)
            current_css = under_test.styleSheet()
            assert expected_css in current_css

    def test_set_position(self):
        """Dashboard Position change"""

        under_test = Dashboard()

        initial_position = under_test.app_widget.pos()

        # Test set_position affect Dashboard
        set_app_config('Dashboard', 'position', 'top:right')
        under_test.set_position()
        self.assertNotEqual(under_test.app_widget.pos(), initial_position)

        # Test new configuration not affect Dashbard position
        new_position = under_test.app_widget.pos()
        set_app_config('Dashboard', 'position', 'top:left')
        self.assertEqual(under_test.app_widget.pos(), new_position)
