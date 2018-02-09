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

from alignak_app.core.backend.client import BackendClient
from alignak_app.core.utils.config import init_config, get_app_config


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

        under_test = BackendClient()

        connect = under_test.login()

        # Compare config url and app_backend
        self.assertEquals(
            under_test.backend.url_endpoint_root,
            get_app_config('Alignak', 'backend')
        )
        self.assertTrue(under_test.connected)
        self.assertTrue(under_test.backend.authenticated)
        self.assertTrue(connect)

        second_test = BackendClient()

        connect = second_test.login('admin', 'admin')
        self.assertTrue(connect)

    def test_get_endpoint_with_params_and_projection(self):
        """Backend GET"""

        backend_test = BackendClient()

        backend_test.login()

        # Get hosts states
        test_projection = [
            'name', 'alias'
        ]

        test_params = {'where': json.dumps({'_is_template': False})}

        under_test = backend_test.get('host', params=test_params, projection=test_projection)

        self.assertTrue(under_test)
        self.assertTrue(under_test['_items'])
        self.assertTrue('name' in under_test['_items'][0])
        self.assertTrue('alias' in under_test['_items'][0])

    def test_patch(self):
        """PATCH User Notes"""

        under_test = BackendClient()
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

    def test_get_realm_name(self):
        """Get User Realm Name"""

        backend_test = BackendClient()
        backend_test.login()

        under_test = backend_test.get_realm_name('false_id')
        self.assertEqual('n/a', under_test)

        backend_test.login()
        under_test2 = backend_test.get_realm_name('59c4e38535d17b8dcb0bed42')
        self.assertEqual('All', under_test2)

    def test_query_user_data(self):
        """Query User Data"""

        under_test = BackendClient()
        under_test.login()

        from alignak_app.core.backend.data_manager import data_manager
        under_test.query_user_data()

        self.assertIsNotNone(data_manager.database['user'])

    def test_query_hosts_data(self):
        """Query Host Data"""

        under_test = BackendClient()
        under_test.login()

        from alignak_app.core.backend.data_manager import data_manager
        under_test.query_hosts_data()

        self.assertIsNotNone(data_manager.database['host'])

    def test_query_services_data(self):
        """Query Services Data"""

        under_test = BackendClient()
        under_test.login()

        from alignak_app.core.backend.data_manager import data_manager
        under_test.query_services_data()

        self.assertIsNotNone(data_manager.database['service'])

    def test_query_daemons_data(self):
        """Query Daemons Data"""

        under_test = BackendClient()
        under_test.login()

        from alignak_app.core.backend.data_manager import data_manager
        under_test.query_daemons_data()

        self.assertIsNotNone(data_manager.database['alignakdaemon'])

    def test_query_livesynthesis_data(self):
        """Query Live Synthesis Data"""

        under_test = BackendClient()
        under_test.login()

        from alignak_app.core.backend.data_manager import data_manager
        under_test.query_livesynthesis_data()

        self.assertIsNotNone(data_manager.database['livesynthesis'])

    # def test_query_history_data(self):
    #     """Query History Data"""
    #
    #     under_test = BackendClient()
    #     under_test.login()
    #
    #     from alignak_app.core.backend.data_manager import data_manager
    #     under_test.query_history_data()
    #
    #     self.assertIsNotNone(data_manager.database['history'])

    def test_get_period_name(self):
        """Get Period Name"""

        backend_test = BackendClient()
        backend_test.login()

        under_test = backend_test.get_period_name('host')

        self.assertEqual('n/a', under_test)

        under_test = backend_test.get_period_name('service')

        self.assertEqual('n/a', under_test)

    def test_get_backend_status_icon(self):
        """Get Backend Status Icon Name"""

        backend_test = BackendClient()

        under_test = backend_test.get_backend_status_icon()
        self.assertEqual('disconnected', under_test)

        backend_test.login()

        under_test = backend_test.get_backend_status_icon()
        self.assertEqual('connected', under_test)

