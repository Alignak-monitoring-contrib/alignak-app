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

from alignak_app.synthesis.host_synthesis import HostSynthesis
from alignak_app.core.action_manager import ActionManager

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QStackedWidget, QListWidget
from PyQt5.Qt import QPixmap


class TestHostSynthesis(unittest2.TestCase):
    """
        This file test the HostSynthesis class.
    """

    service = {
        'name': 'my_service',
        'display_name': 'My Service',
        '_id': '11111',
        'ls_state': 'OK',
        '_overall_state_id': 2,
        'ls_last_check': 0.0,
        'ls_output': 'Output of the service',
        'ls_acknowledged': False,
        'ls_downtimed': False,
        'business_impact': '2',
        'customs': {},
        'aggregation': 'IO',
        'ls_last_state_changed': 0
    }

    backend_data = {
        'host': {
            'display_name': 'My Service',
            'alias': 'my service',
            'name': 'my_service',
            '_id': '00000',
            'ls_state': 'OK',
            'ls_last_check': 0.0,
            'ls_output': 'Output of the service',
            'ls_acknowledged': False,
            'ls_downtimed': False,
            'address': '127.0.0.1',
            'business_impact': '2',
            'parents': [],
            'ls_last_state_changed': 0
        },
        'services': [
            service,
            service
        ]
    }

    action_manager = ActionManager(None)

    @classmethod
    def setUpClass(cls):
        """Create QApplication"""
        try:
            cls.app = QApplication(sys.argv)
        except:
            pass

    def test_initialize(self):
        """Initialize Host Synthesis"""

        under_test = HostSynthesis(self.action_manager)

        self.assertIsNone(under_test.app_backend)
        self.assertIsNotNone(under_test.action_manager)
        self.assertFalse(under_test.host)
        self.assertIsNone(under_test.stack)
        self.assertIsNone(under_test.services_list)

        under_test.initialize(None)

        self.assertIsNone(under_test.app_backend)
        self.assertIsNotNone(under_test.action_manager)
        self.assertFalse(under_test.host)
        self.assertIsNone(under_test.stack)
        self.assertIsNone(under_test.services_list)

        under_test.initialize(self.backend_data)

        self.assertIsNone(under_test.app_backend)
        self.assertIsNotNone(under_test.action_manager)
        self.assertTrue(under_test.host)
        self.assertIsNotNone(under_test.stack)
        self.assertIsInstance(under_test.stack, QStackedWidget)
        self.assertIsNotNone(under_test.services_list)
        self.assertIsInstance(under_test.services_list, QListWidget)

    def test_get_host_widget(self):
        """Get Host QWidget"""

        under_test = HostSynthesis(self.action_manager)
        widget_test = under_test.get_host_widget(self.backend_data)

        self.assertIsNotNone(widget_test)
        self.assertIsInstance(widget_test, QWidget)

    def test_get_services_widget(self):
        """Get Services QWidget"""

        under_test = HostSynthesis(self.action_manager)

        self.assertIsNone(under_test.stack)
        self.assertIsNone(under_test.services_list)

        widget_test = under_test.get_services_widget(self.backend_data)

        self.assertIsNotNone(under_test.stack)
        self.assertEqual(2, under_test.stack.count())
        self.assertIsNotNone(under_test.services_list)
        self.assertEqual(2, under_test.services_list.count())

        self.assertIsNotNone(widget_test)
        self.assertIsInstance(widget_test, QWidget)

    def test_display_current_service(self):
        """Display Current Service"""

        under_test = HostSynthesis(self.action_manager)
        under_test.initialize(self.backend_data)

        under_test.display_current_service(1)

        self.assertEqual(1, under_test.stack.currentIndex())

        under_test.display_current_service(0)

        self.assertEqual(0, under_test.stack.currentIndex())

    def test_get_icons(self):
        """Get Host Icon and Host Real State Icon"""

        under_test = HostSynthesis(self.action_manager)

        host_icon_test = under_test.get_host_icon(self.backend_data['host'])

        self.assertIsInstance(host_icon_test, QPixmap)

        icon_real_state_test = under_test.get_real_state_icon(self.backend_data['services'])

        self.assertIsInstance(icon_real_state_test, QPixmap)
