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
from alignak_app.qobjects.panel.host import HostQWidget

# app = QApplication(sys.argv)
init_localization()
data_manager.database['user'] = User()
data_manager.database['user'].create('_id', {}, 'name')

host = Host()
host.create(
    '_id1',
    {
        'name': 'localhost',
        'ls_state': 'DOWN',
        'ls_acknowledged': False,
        'ls_downtimed': False,
     },
    'localhost'
)
data_manager.database['host'] = [host]


class TestHostQWidget(unittest2.TestCase):
    """
        This file test methods of AppBackend class
    """

    # Create config for all methods.
    settings.init_config()

    @classmethod
    def setUpClass(cls):
        """Create QApplication"""
        try:
            cls.app = QApplication(sys.argv)
        except:
            pass

    def test_initialize_host_widget(self):
        """Initialize Host QWidget"""

        under_test = HostQWidget()

        self.assertIsNone(under_test.host_item)
        self.assertIsNone(under_test.service_items)
        self.assertIsNone(under_test.history_widget)
        self.assertIsNone(under_test.layout())
        self.assertIsNotNone(under_test.labels)
        self.assertIsNotNone(under_test.history_btn)

        under_test.initialize()

        self.assertIsNotNone(under_test.layout())

    def test_set_data(self):
        """Set Data Host QWidget"""

        under_test = HostQWidget()
        under_test.initialize()

        self.assertIsNone(under_test.host_item)
        self.assertIsNone(under_test.service_items)

        data_manager.database['host'] = [host]
        under_test.set_data('localhost')

        self.assertIsNotNone(under_test.host_item)
        self.assertIsInstance(under_test.host_item, Host)
        self.assertIsNotNone(under_test.service_items)
        for item in under_test.service_items:
            self.assertIsInstance(item, Service)

