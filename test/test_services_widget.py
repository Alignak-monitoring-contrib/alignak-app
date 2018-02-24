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
from PyQt5.Qt import QApplication

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

from alignak_app.qobjects.panel.services import ServicesQWidget


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
        except:
            pass

    def test_initialize(self):
        """Initialize ServicesQWidget"""

        under_test = ServicesQWidget()

        self.assertIsNone(under_test.host_item)
        self.assertIsNone(under_test.service_items)
        self.assertIsNotNone(under_test.services_tree_widget)
        self.assertIsNotNone(under_test.service_data_widget)
        self.assertIsNotNone(under_test.nb_services_widget)

        under_test.initialize()

        self.assertIsNone(under_test.host_item)
        self.assertIsNone(under_test.service_items)
        self.assertIsNotNone(under_test.services_tree_widget)
        self.assertIsNotNone(under_test.service_data_widget)
        self.assertIsNotNone(under_test.nb_services_widget)

    def test_set_data(self):
        """Set Data Services QWidget"""

        under_test = ServicesQWidget()
        self.assertIsNone(under_test.host_item)
        self.assertIsNone(under_test.service_items)

        data_manager.update_database('host', self.host_list)
        data_manager.update_database('service', self.service_list)

        under_test.set_data('host1')

        # Assert Data is filled
        self.assertIsNotNone(under_test.host_item)
        self.assertIsInstance(under_test.host_item, Host)
        self.assertEqual('host1', under_test.host_item.name)

        self.assertIsNotNone(under_test.service_items)
        for service in under_test.service_items:
            self.assertIsInstance(service, Service)
            self.assertEqual('_id1', service.data['host'])

    def test_update_widget(self):
        """Update Services QWidget"""

        under_test = ServicesQWidget()
        data_manager.update_database('host', self.host_list)
        data_manager.update_database('service', self.service_list)

        under_test.set_data('host2')
        under_test.initialize()

        old_tree_widget = under_test.services_tree_widget
        old_service_data_widget = under_test.service_data_widget
        old_nb_services_widget = under_test.nb_services_widget
        old_service_items = under_test.service_items

        under_test.update_widget()

        self.assertNotEqual(old_tree_widget, under_test.services_tree_widget)
        self.assertNotEqual(old_service_data_widget, under_test.service_data_widget)
        self.assertNotEqual(old_nb_services_widget, under_test.nb_services_widget)
        # Assert Services Items had been sorted
        self.assertNotEqual(old_service_items, under_test.service_items)
