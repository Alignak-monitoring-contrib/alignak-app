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

from alignak_app.synthesis.serviceframe import ServiceFrame
from alignak_app.models.item_service import Service

from PyQt5.QtWidgets import QApplication, QLabel


class TestService(unittest2.TestCase):
    """
        This file test the Service class.
    """

    service = Service()
    service_data = {
        'display_name': 'My Service',
        'ls_state': 'OK',
        'ls_last_check': 0.0,
        'ls_output': 'Output of the service',
        '_id': '000',
        'business_impact': '2',
        'customs': {},
        'ls_last_state_changed': 0,
        'ls_acknowledged': True,
        'ls_downtimed': False,
        'name': 'my_service'
    }
    service.create(service_data['_id'], service_data, service_data['name'])

    @classmethod
    def setUpClass(cls):
        """Create QApplication"""
        try:
            cls.app = QApplication(sys.argv)
        except:
            pass

    def test_init_view(self):
        """Initialize Service"""

        under_test = ServiceFrame()

        self.assertIsNone(under_test.acknowledge_btn)
        self.assertIsNone(under_test.downtime_btn)

        under_test.initialize(self.service)

        self.assertIsNotNone(under_test.acknowledge_btn)
        self.assertIsNotNone(under_test.downtime_btn)

    def test_get_service_icon(self):
        """Get Service Icon"""

        under_test = ServiceFrame()

        icon_ok = under_test.get_service_icon('OK')

        self.assertIsInstance(icon_ok, QLabel)
        self.assertEqual(icon_ok.toolTip(), 'Service is OK')

        icon_warning = under_test.get_service_icon('WARNING')
        self.assertEqual(icon_warning.toolTip(), 'Service is WARNING')

        icon_critical = under_test.get_service_icon('CRITICAL')
        self.assertEqual(icon_critical.toolTip(), 'Service is CRITICAL')

        icon_unknown = under_test.get_service_icon('UNKNOWN')
        self.assertEqual(icon_unknown.toolTip(), 'Service is UNKNOWN')

        icon_unreachable = under_test.get_service_icon('UNREACHABLE')
        self.assertEqual(icon_unreachable.toolTip(), 'Service is UNREACHABLE')

        icon_bad = under_test.get_service_icon('BAD')
        self.assertEqual(icon_bad.toolTip(), 'Service is ERROR')
