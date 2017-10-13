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

from alignak_app.core.data_manager import data_manager
from alignak_app.core.items.item_user import User
from alignak_app.core.items.item_host import Host
from alignak_app.core.items.item_service import Service
from alignak_app.core.utils import init_config
from alignak_app.core.locales import init_localization

from PyQt5.Qt import QApplication, QLabel, QPushButton, QWidget

init_config()
init_localization()
app = QApplication(sys.argv)
user = User()
user.create('_id', {'name': 'name'}, 'name')
data_manager.database['user'] = user
from alignak_app.widgets.panel.service_data_widget import ServiceDataQWidget


class TestServiceDataQWidget(unittest2.TestCase):
    """
        This file test methods of ServiceDataQWidget class object
    """

    # Host data test
    host_list = []
    for i in range(0, 10):
        host = Host()
        host.create(
            '_id%d' % i,
            {'name': 'host%d' % i},
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
                'host': '_id%d' % i,
                'ls_acknowledged': False,
                'ls_downtimed': False,
                'ls_state': 'OK',
                'aggregation': 'disk'
            },
            'service%d' % i
        )
        service_list.append(service)
        service = Service()
        service.create(
            'other_id2%d' % i,
            {
                'name': 'other_service2%d' % i,
                'host': '_id%d' % i,
                'ls_acknowledged': False,
                'ls_downtimed': False,
                'ls_state': 'CRITICAL',
                'aggregation': 'CPU'
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
        """Initialize ServiceDataQWidget"""

        under_test = ServiceDataQWidget()

        self.assertIsNone(under_test.service_item)
        self.assertIsNone(under_test.host_id)
        self.assertIsNotNone(under_test.labels)
        for label in under_test.labels:
            self.assertIsInstance(under_test.labels[label], QLabel)
        self.assertIsNotNone(under_test.buttons)
        for button in under_test.buttons:
            self.assertIsInstance(under_test.buttons[button], QPushButton)

        under_test.initialize()

        self.assertIsNone(under_test.service_item)
        self.assertIsNone(under_test.host_id)
        self.assertIsNotNone(under_test.labels)
        self.assertIsNotNone(under_test.buttons)
        for label in under_test.labels:
            self.assertIsInstance(under_test.labels[label], QLabel)
        self.assertIsNotNone(under_test.buttons)
        for button in under_test.buttons:
            self.assertIsInstance(under_test.buttons[button], QPushButton)
        # Assert QWidget is Hidden for first display
        self.assertTrue(under_test.isHidden())

    def test_get_icon_widget(self):
        """Get Icon QWidget ServiceDataQWidget"""

        service_data_widget_test = ServiceDataQWidget()

        under_test = service_data_widget_test.get_icon_widget()

        self.assertIsInstance(under_test, QWidget)




