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

import json

import unittest2

from alignak_app.core.backend import AppBackend
from alignak_app.core.data_manager import DataManager
from alignak_app.core.utils import init_config


class TestDataManager(unittest2.TestCase):
    """
        This file test the DataManager class.
    """

    init_config()
    params = {'where': json.dumps({'_is_template': False})}
    host_projection = ['name', 'alias', 'ls_state', '_id', 'ls_acknowledged', 'ls_downtimed',
                       'ls_last_check', 'ls_output', 'address', 'business_impact', 'parents',
                       'ls_last_state_changed']

    def test_initialize(self):
        """Initialize DataManager"""

        under_test = DataManager()

        self.assertTrue('hosts' in under_test.database)
        self.assertTrue('services' in under_test.database)

    def test_update_database(self):
        """Update DataManager Database"""

        backend_test = AppBackend()
        backend_test.login()
        data_test = backend_test.get('host', params=self.params, projection=self.host_projection)

        under_test = DataManager()
        under_test.update_item_type('hosts', data_test['_items'])

        for d in data_test['_items']:
            self.assertTrue(d['_id'] in under_test.database['hosts'])

    def test_get_item(self):
        """Get Item in DataManager"""

        backend_test = AppBackend()
        backend_test.login()
        data_test = backend_test.get('host', params=self.params, projection=self.host_projection)

        under_test = DataManager()
        under_test.update_item_type('hosts', data_test['_items'])

        for d in data_test['_items']:
            wanted_item = under_test.get_item('hosts', d['_id'])
            self.assertEqual(d, wanted_item)

