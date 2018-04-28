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

from PyQt5.Qt import QApplication, Qt

from alignak_app.backend.datamanager import data_manager
from alignak_app.items.host import Host
from alignak_app.items.service import Service
from alignak_app.items.user import User
from alignak_app.utils.config import settings
from alignak_app.locales.locales import init_localization

settings.init_config()
init_localization()
app = QApplication(sys.argv)
user = User()
user.create('_id', {'name': 'name'}, 'name')
data_manager.database['user'] = user

from alignak_app.backend.datamanager import data_manager

from alignak_app.qobjects.service.services import ServicesQWidget


class TestServicesQWidget(unittest2.TestCase):
    """
        This file test methods of ServicesQWidget class object
    """

    # Host data test
    host_list = []
    for i in range(0, 10):
        host = Host()
        host.create(
            '_id%d' % i,
            {
                'name': 'host%d' % i,
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
                'ls_state': 'OK',
                'aggregation': 'disk',
                'passive_checks_enabled': False,
                'active_checks_enabled': True
            },
            'service%d' % i
        )
        service_list.append(service)
        service = Service()
        service.create(
            'other_id2%d' % i,
            {
                'name': 'other_service2%d' % i,
                'alias': 'Other Service %d' % i,
                'host': '_id%d' % i,
                'ls_acknowledged': False,
                'ls_downtimed': False,
                'ls_state': 'CRITICAL',
                'aggregation': 'CPU',
                'passive_checks_enabled': False,
                'active_checks_enabled': True
            },
            'other_service%d' % i
        )
        service_list.append(service)

    @classmethod
    def setUpClass(cls):
        """Create QApplication"""
        try:
            cls.app = QApplication(sys.argv)
        except Exception as e:
            print(e)
            pass

    def test_initialize(self):
        """Initialize ServicesQWidget"""

        under_test = ServicesQWidget()

        self.assertIsNone(under_test.services)
        self.assertIsNotNone(under_test.services_tree_widget)
        self.assertIsNotNone(under_test.service_data_widget)
        self.assertIsNotNone(under_test.services_dashboard)

        under_test.initialize()

        self.assertIsNone(under_test.services)
        self.assertIsNotNone(under_test.services_tree_widget)
        self.assertIsNotNone(under_test.service_data_widget)
        self.assertIsNotNone(under_test.services_dashboard)

    def test_update_widget(self):
        """Update Services QWidget"""

        under_test = ServicesQWidget()
        data_manager.update_database('host', self.host_list)
        data_manager.update_database('service', self.service_list)

        under_test.initialize()

        self.assertIsNone(under_test.services)

        services = data_manager.get_host_services(self.host_list[2].item_id)
        under_test.update_widget(services)

        self.assertIsNotNone(under_test.services)

    def test_set_filter_items(self):
        """Set Filter Services Items"""

        under_test = ServicesQWidget()
        data_manager.update_database('host', self.host_list)
        data_manager.update_database('service', self.service_list)

        under_test.initialize()
        services = data_manager.get_host_services(self.host_list[2].item_id)
        under_test.update_widget(services)

        self.assertEqual(0, under_test.services_list_widget.count())

        under_test.set_filter_items('OK')

        # Host has only one service OK
        self.assertEqual(1, under_test.services_list_widget.count())

        under_test.services_list_widget.clear()
        under_test.set_filter_items('UNKNOWN')
        under_test.services_list_widget.setCurrentItem(under_test.services_list_widget.item(0))

        # Host has no service UNKNOWN, so item have hint text
        self.assertEqual(1, under_test.services_list_widget.count())
        self.assertEqual(
            'No such services to display...',
            under_test.services_list_widget.currentItem().data(Qt.DisplayRole)
        )

    def test_add_filter_item(self):
        """Add Filter Service Item to QListWidget"""

        under_test = ServicesQWidget()
        under_test.initialize()

        self.assertEqual(0, under_test.services_list_widget.count())

        under_test.add_filter_item(self.service_list[2])
        under_test.services_list_widget.setCurrentItem(under_test.services_list_widget.item(0))

        # Service "Service 1" is added to QListWidget
        self.assertEqual(1, under_test.services_list_widget.count())
        self.assertEqual(
            'Service 1',
            under_test.services_list_widget.currentItem().data(Qt.DisplayRole)
        )
