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
from PyQt5.Qt import QApplication, QLabel, QPushButton, QWidget

from alignak_app.backend.datamanager import data_manager
from alignak_app.items.host import Host
from alignak_app.items.service import Service
from alignak_app.items.user import User
from alignak_app.utils.config import settings
from alignak_app.locales.locales import init_localization

from alignak_app.qobjects.panel.service import ServiceDataQWidget

settings.init_config()
init_localization()
app = QApplication(sys.argv)
user = User()
user.create('_id', {'name': 'name'}, 'name')
data_manager.database['user'] = user


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
            {
                'name': 'host%d' % i,
                '_id': '_id%d' % i,
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
                'alias': 'service %d' % i,
                '_id': '_id%d' % i,
                'host': '_id%d' % i,
                'ls_acknowledged': False,
                'ls_downtimed': False,
                'ls_state': 'OK',
                'aggregation': 'disk',
                'ls_last_check': 123456789,
                'ls_output': 'All is ok',
                'business_impact': 2,
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
                '_id': 'other_id2%d' % i,
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
        """Initialize ServiceDataQWidget"""

        under_test = ServiceDataQWidget()

        self.assertIsNone(under_test.service_item)
        self.assertIsNotNone(under_test.labels)

        for label in under_test.labels:
            self.assertIsInstance(under_test.labels[label], QLabel)
        self.assertIsNotNone(under_test.buttons)
        for button in under_test.buttons:
            self.assertIsInstance(under_test.buttons[button], QPushButton)

        under_test.initialize()

        self.assertIsNone(under_test.service_item)
        self.assertIsNotNone(under_test.labels)

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

        under_test = service_data_widget_test.get_service_icon_widget()

        self.assertIsInstance(under_test, QWidget)

    def test_update_widget(self):
        """Update ServiceData QWidget"""

        under_test = ServiceDataQWidget()
        under_test.initialize()

        old_labels = {}

        # Store QLabel.text() = ''
        for label in under_test.labels:
            old_labels[label] = under_test.labels[label]

        data_manager.database['user'].data['can_submit_commands'] = True
        data_manager.update_database('service', self.service_list)

        under_test.update_widget(self.service_list[0])

        new_labels = under_test.labels

        # Assert labels have been filled by update
        for label in old_labels:
            self.assertNotEqual(new_labels[label].text(), old_labels[label])




