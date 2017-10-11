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
from alignak_app.core.utils import init_config, get_app_config


class TestAppBackend(unittest2.TestCase):
    """
        This file test methods of AppBackend class
    """

    # Create config for all methods.
    init_config()

    @classmethod
    def setUpClass(cls):
        cls.host_id = '59c4e40635d17b8e096acc70'
        cls.service_id = '59c4e41535d17b8e0c6acd50'

    def test_log_to_backend(self):
        """Connection to Alignak-Backend"""

        under_test = AppBackend()

        connect = under_test.login()

        # Compare config url and app_backend
        self.assertEquals(
            under_test.backend.url_endpoint_root,
            get_app_config('Alignak', 'backend')
        )
        self.assertTrue(under_test.connected)
        self.assertTrue(under_test.backend.authenticated)
        self.assertTrue(connect)

        under_test = AppBackend()

        connect = under_test.login('admin', 'admin')
        self.assertTrue(connect)

    def test_hosts_endpoint_without_params(self):
        """Collect Hosts States"""

        backend_test = AppBackend()

        backend_test.login()

        # Get hosts states
        under_test = backend_test.get('host')

        self.assertTrue(under_test)
        self.assertTrue(under_test['_items'])

    def test_service_endpoint_with_params(self):
        """Collect Services States"""

        backend_test = AppBackend()

        backend_test.login()

        params = {'where': json.dumps({'_is_template': False})}
        # Get services states
        under_test = backend_test.get('service', params=params)

        self.assertTrue(under_test)
        self.assertTrue(under_test['_items'])
        self.assertTrue(under_test['_status'])

    def test_get_host(self):
        """GET Host Data"""

        backend_test = AppBackend()
        backend_test.login()
        projection_test = ['name', 'alias', 'address']

        under_test = backend_test.get_host('name', 'localhost', projection=projection_test)

        self.assertIsNotNone(under_test)

        # Wanted fields are here
        self.assertTrue('name' in under_test)
        self.assertEqual('localhost', under_test['name'])
        self.assertTrue('address' in under_test)
        self.assertEqual('127.0.0.1', under_test['address'])

        # Unwanted fields are not returned
        self.assertTrue('ls_acknowledged' not in under_test)
        self.assertTrue('ls_downtimed' not in under_test)

    def test_get_service(self):
        """GET Service Data"""

        backend_test = AppBackend()
        backend_test.login()

        under_test = backend_test.get_service(
            self.host_id,
            self.service_id,
            ['ls_acknowledged']
        )

        self.assertIsNotNone(under_test)
        self.assertTrue('ls_acknowledged' in under_test)
        self.assertTrue('name' not in under_test)
        self.assertIsNotNone(under_test['ls_acknowledged'])

    def test_patch(self):
        """PATCH User Notes"""

        under_test = AppBackend()
        under_test.login()

        users = under_test.get('user')
        user = users['_items'][0]
        notes = 'Unit Test from Alignak-app'

        data = {'notes': notes}
        headers = {'If-Match': user['_etag']}
        endpoint = '/'.join(['user', user['_id']])

        patched = under_test.patch(endpoint, data, headers)

        self.assertTrue(patched)
        user_modified = under_test.get('/'.join(['user', user['_id']]))

        self.assertEqual(user_modified['notes'], notes)

        back_patched = under_test.patch(endpoint, data={'notes': ''}, headers=headers)

        self.assertTrue(back_patched)
        user_modified = under_test.get('/'.join(['user', user['_id']]))

        self.assertNotEqual(user_modified['notes'], notes)
        self.assertEqual(user_modified['notes'], '')
