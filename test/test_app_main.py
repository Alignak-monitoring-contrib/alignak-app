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

from alignak_app.backend.datamanager import data_manager
from alignak_app.utils.config import settings

from alignak_app.qobjects.events.events import init_event_widget
from alignak_app.qobjects.app_main import AppQMainWindow


class TestAppQMainWindow(unittest2.TestCase):
    """
        This file test methods of AppQMainWindow class.
    """

    @classmethod
    def setUpClass(cls):
        """Create QApplication"""

        try:
            cls.app = QApplication(sys.argv)
        except:
            pass

    def test_initialize_app_main_window(self):
        """Initialize AppQMainWindow"""

        under_test = AppQMainWindow()

        self.assertTrue(under_test.panel_widget)
        self.assertTrue(under_test.dock)
        self.assertIsNone(under_test.offset)

        data_manager.update_database('host', [])
        data_manager.update_database('service', [])
        init_event_widget()
        under_test.initialize()

        self.assertTrue(under_test.panel_widget)
        self.assertTrue(under_test.dock)
        self.assertIsNone(under_test.offset)

    def test_app_main_window_display_settings(self):
        """Display AppQMainWindow at Start"""

        under_test = AppQMainWindow()
        data_manager.update_database('host', [])
        data_manager.update_database('service', [])

        self.assertFalse(under_test.isVisible())
        settings.set_config('Alignak-app', 'display', 'min')

        under_test.initialize()

        # AppQMainWindow is visible but not maximized
        self.assertEqual('min', settings.get_config('Alignak-app', 'display'))
        self.assertTrue(under_test.isVisible())
        self.assertFalse(under_test.isMaximized())
        under_test.close()

        settings.set_config('Alignak-app', 'display', 'max')

        under_test = AppQMainWindow()
        init_event_widget()
        under_test.initialize()

        # AppQMainWindow is visible and Maximized
        self.assertEqual('max', settings.get_config('Alignak-app', 'display'))
        self.assertTrue(under_test.isVisible())
        self.assertTrue(under_test.isMaximized())
        under_test.close()

        settings.set_config('Alignak-app', 'display', 'no')

        under_test = AppQMainWindow()
        init_event_widget()
        under_test.initialize()

        # AppQMainWindow is not visible and not maximized
        self.assertEqual('no', settings.get_config('Alignak-app', 'display'))
        self.assertFalse(under_test.isVisible())
        self.assertFalse(under_test.isMaximized())
        under_test.close()

        # Restore default setting
        settings.set_config('Alignak-app', 'display', 'min')

    def test_default_view_is_problems(self):
        """Display Problems View by Default"""

        settings.set_config('Alignak-app', 'problems', 'no')

        under_test = AppQMainWindow()
        data_manager.update_database('host', [])
        data_manager.update_database('service', [])
        init_event_widget()

        self.assertEqual(-1, under_test.panel_widget.tab_widget.currentIndex())

        under_test.initialize()
        problems_index = under_test.panel_widget.get_tab_order().index('p')

        self.assertFalse(settings.get_config('Alignak-app', 'problems', boolean=True))
        self.assertEqual(
            problems_index,
            under_test.panel_widget.tab_widget.indexOf(under_test.panel_widget.problems_widget)
        )

        # Make "Problems" as default view
        settings.set_config('Alignak-app', 'problems', 'yes')

        under_test = AppQMainWindow()
        init_event_widget()
        under_test.initialize()

        self.assertTrue(settings.get_config('Alignak-app', 'problems', boolean=True))
        self.assertEqual(
            problems_index,
            under_test.panel_widget.tab_widget.indexOf(under_test.panel_widget.problems_widget)
        )

        # Reset settings
        settings.set_config('Alignak-app', 'problems', 'no')
