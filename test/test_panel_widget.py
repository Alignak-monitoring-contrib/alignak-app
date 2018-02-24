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

from alignak_app.utils.config import settings
from alignak_app.backend.datamanager import data_manager
from alignak_app.items.host import Host
from alignak_app.items.service import Service

from alignak_app.qobjects.panel.panel import PanelQWidget
from alignak_app.qobjects.dock.spy import SpyQWidget


class TestLoginQDialog(unittest2.TestCase):
    """
        This file test the PanelQWidget class.
    """

    settings.init_config()

    # Host data test
    host_list = []
    for i in range(0, 10):
        host = Host()
        host.create(
            '_id%d' % i,
            {
                'name': 'host%d' % i,
                'alias': 'Host %d' % i,
                '_id': '_id%d' % i,
                'ls_downtimed': True,
                'ls_acknowledged': True,
                'ls_state': 'UNKNOWN',
                'ls_output': 'output host %d' % i,
                'ls_last_check': '',
                '_realm': '59c4e38535d17b8dcb0bed42',
                'address': '127.0.0.1',
                'business_impact': '2',
                'notes': 'host notes',
                'passive_checks_enabled': False,
                'active_checks_enabled': True
            },
            'host%d' % i
        )
        host_list.append(host)

    # Service data test
    service_list = []
    for i in range(0, 10):
        service = Service()
        service.create(
            '_id%d' % i,
            {
                'name': 'service%d' % i,
                'alias': 'Service %d' % i,
                'host': '_id%d' % i,
                'ls_acknowledged': False,
                'ls_downtimed': False,
                'ls_state': 'CRITICAL',
                'ls_output': 'output host %d' % i,
                'aggregation': 'disk',
                '_overall_state_id': 4,
                'passive_checks_enabled': False,
                'active_checks_enabled': True
            },
            'service%d' % i
        )
        service_list.append(service)

    @classmethod
    def setUpClass(cls):
        """Create QApplication"""
        try:
            cls.app = QApplication(sys.argv)
        except:
            pass

    def test_create_widget(self):
        """Inititalize PanelQWidget"""

        data_manager.update_database('host', self.host_list)
        data_manager.update_database('service', self.service_list)
        under_test = PanelQWidget()

        self.assertIsNotNone(under_test.layout)
        self.assertIsNotNone(under_test.line_search)
        self.assertIsNotNone(under_test.completer)
        self.assertIsNotNone(under_test.dashboard_widget)
        self.assertIsNotNone(under_test.host_widget)
        self.assertIsNotNone(under_test.services_widget)
        self.assertIsNotNone(under_test.spy_button)

        self.assertIsNone(under_test.spy_widget)
        self.assertFalse(under_test.hostnames_list)

        spy_widget_test = SpyQWidget()
        under_test.initialize(spy_widget_test)

        self.assertIsNotNone(under_test.layout)
        self.assertIsNotNone(under_test.line_search)
        self.assertIsNotNone(under_test.completer)
        self.assertIsNotNone(under_test.dashboard_widget)
        self.assertIsNotNone(under_test.host_widget)
        self.assertIsNotNone(under_test.services_widget)
        self.assertIsNotNone(under_test.spy_button)

        self.assertIsNotNone(under_test.spy_widget)
        self.assertTrue(under_test.hostnames_list)
        self.assertEqual(
            ['host0', 'host1', 'host2', 'host3', 'host4', 'host5', 'host6', 'host7', 'host8', 'host9'],
            under_test.hostnames_list
        )

    def test_spy_host(self):
        """Panel Add Spy Host"""

        under_test = PanelQWidget()
        spy_widget_test = SpyQWidget()
        under_test.initialize(spy_widget_test)

        # Host is not in hostname_list
        under_test.line_search.setText('no_host')
        under_test.spy_host()
        self.assertTrue(under_test.spy_button.isEnabled())
        # Host Id is not added in spied_hosts of SpyQWidget.SpyQListWidget
        self.assertFalse('_id0' in under_test.spy_widget.spy_list_widget.spied_hosts)

        # Host is in hostname_list
        under_test.line_search.setText('host0')
        under_test.spy_host()
        self.assertFalse(under_test.spy_button.isEnabled())
        # Host Id is added in spied_hosts of SpyQWidget.SpyQListWidget
        self.assertTrue('_id0' in under_test.spy_widget.spy_list_widget.spied_hosts)