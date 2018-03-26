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

from alignak_app.qobjects.panel import PanelQWidget
from alignak_app.qobjects.events.events import init_event_widget


class TestPanelQWidget(unittest2.TestCase):
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
                'active_checks_enabled': True,
                '_overall_state_id': 1
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
                '_id': '_id%d' % i,
                'ls_acknowledged': False,
                'ls_downtimed': False,
                'ls_state': 'CRITICAL',
                'ls_output': 'output host %d' % i,
                'aggregation': 'disk',
                '_overall_state_id': 4,
                'passive_checks_enabled': False,
                'active_checks_enabled': True,
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

        # Add problems
        data_manager.update_database('host', self.host_list)
        data_manager.database['problems'] = []
        for item in self.host_list:
            data_manager.database['problems'].append(item)
        for item in self.service_list:
            data_manager.database['problems'].append(item)

        for item in self.host_list:
            assert 'host' in item.item_type

        under_test = PanelQWidget()

        self.assertIsNotNone(under_test.layout)
        self.assertIsNotNone(under_test.line_search)
        self.assertIsNotNone(under_test.completer)
        self.assertIsNotNone(under_test.dashboard_widget)
        self.assertIsNotNone(under_test.host_widget)
        self.assertIsNotNone(under_test.services_widget)
        self.assertIsNotNone(under_test.spy_button)
        self.assertIsNotNone(under_test.spy_widget)

        self.assertFalse(under_test.hostnames_list)

        under_test.initialize()

        self.assertIsNotNone(under_test.layout)
        self.assertIsNotNone(under_test.line_search)
        self.assertIsNotNone(under_test.completer)
        self.assertIsNotNone(under_test.dashboard_widget)
        self.assertIsNotNone(under_test.host_widget)
        self.assertIsNotNone(under_test.services_widget)
        self.assertIsNotNone(under_test.spy_button)
        self.assertIsNotNone(under_test.spy_widget)

        self.assertEqual(
            ['host0', 'host1', 'host2', 'host3', 'host4', 'host5',
             'host6', 'host7', 'host8', 'host9'],
            under_test.hostnames_list
        )

    def test_spy_host(self):
        """Panel Add Spy Host"""

        # init_event_widget()

        under_test = PanelQWidget()
        under_test.initialize()

        # Host is not in hostname_list
        under_test.line_search.setText('no_host')
        under_test.spy_host()
        spy_index = under_test.get_tab_order().index('s')

        self.assertTrue(under_test.spy_button.isEnabled())
        self.assertEqual('Spied Hosts', under_test.tab_widget.tabText(spy_index))
        # Host Id is not added in spied_hosts of SpyQWidget.SpyQListWidget
        self.assertFalse('_id0' in under_test.spy_widget.spy_list_widget.spied_hosts)

    def test_update_panels(self):
        """Update QTabPanel Problems"""

        under_test = PanelQWidget()
        under_test.initialize()

        # 10 problems for CRITICAL services
        problems_index = under_test.get_tab_order().index('p')
        self.assertEqual('Problems (20)', under_test.tab_widget.tabText(problems_index))

        # Remove a service from problems
        data_manager.database['problems'].remove(self.service_list[0])

        under_test.tab_widget.widget(problems_index).update_problems_data()

        # There are only 9 services in CRITICAL condition
        self.assertEqual('Problems (19)', under_test.tab_widget.tabText(problems_index))

    def test_display_host(self):
        """Display Host in Panel"""

        under_test = PanelQWidget()
        under_test.initialize()

        self.assertTrue(under_test.spy_button.isEnabled())

        under_test.display_host()

        self.assertTrue(under_test.spy_button.isEnabled())
        self.assertTrue(under_test.host_widget.isHidden())
        self.assertTrue(under_test.services_widget.isHidden())

        under_test.line_search.setText(self.host_list[0].name)
        under_test.display_host()

        self.assertTrue(under_test.spy_button.isEnabled())
        self.assertFalse(under_test.host_widget.isHidden())
        self.assertFalse(under_test.services_widget.isHidden())
