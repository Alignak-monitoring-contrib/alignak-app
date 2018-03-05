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

from alignak_app.utils.config import settings
from alignak_app.backend.datamanager import data_manager
from alignak_app.items.service import Service

from alignak_app.qobjects.panel.service_tree_item import ServiceTreeItem


class TestServiceTreeItem(unittest2.TestCase):
    """
        This file test the ServiceTreeItem class.
    """

    settings.init_config()

    service = Service()
    service.create(
        '_id_1',
        {
            '_id': '_id_1',
            'name': 'service_1',
            'host': '_id_1',
            'ls_state': 'CRITICAL',
            'ls_acknowledged': False,
            'ls_downtimed': False,
            'passive_checks_enabled': False,
            'active_checks_enabled': True,
        },
        'service_1'
    )

    @classmethod
    def setUpClass(cls):
        """Create QApplication"""
        try:
            cls.app = QApplication(sys.argv)
        except Exception as e:
            print(e)
            pass

    def test_create_livestate_widget(self):
        """Inititalize ServiceTreeItem"""

        under_test = ServiceTreeItem()

        self.assertFalse(under_test.service_id)
        self.assertFalse(under_test.service_item)

        under_test.initialize(self.service)

        self.assertEqual('_id_1', under_test.service_id)
        self.assertEqual('service_1', under_test.service_item.name)
        self.assertEqual(self.service.data, under_test.service_item.data)

    def test_update_item(self):
        """Update ServiceTreeItem"""

        under_test = ServiceTreeItem()
        under_test.initialize(self.service)

        self.assertEqual('Service_1', under_test.text(0))
        self.assertEqual('service_1', under_test.service_item.name)

        # Update name of service and add to database
        self.service.name = 'service_2'
        self.service.data['name'] = 'service_2'
        data_manager.update_database('service', [self.service])

        # Update ServiceTreeItem
        under_test.update_item()

        # Name of ServiceTreeItem should change, and Service() item also
        self.assertEqual('Service_2', under_test.text(0))
        self.assertEqual('service_2', under_test.service_item.name)
