#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015-2016:
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

import unittest2
import json

from alignak_app.backend.backend import AlignakBackend
from alignak_app.core.utils import set_app_config, get_app_config


class TestBackend(unittest2.TestCase):
    """
        This file test methods of AlignakData class
    """

    # Create config for all methods.
    set_app_config()

    def test_log_to_backend(self):
        """Connection to Alignak-Backend"""

        under_test = AlignakBackend()

        under_test.login()

        # Compare config url and backend
        self.assertEquals(
            under_test.backend.url_endpoint_root,
            get_app_config('Backend', 'backend_url')
        )
        self.assertTrue(under_test.backend.authenticated)

    def test_hosts_endpoint_without_params(self):
        """Collect Hosts States"""

        backend = AlignakBackend()

        backend.login()

        # Get hosts states
        under_test = backend.get('host')

        self.assertTrue(under_test)
        self.assertTrue(under_test['_items'])

    def test_service_endpoint_with_params(self):
        """Collect Services States"""

        alignak_data = AlignakBackend()

        alignak_data.login()

        params = {'where': json.dumps({'_is_template': False})}
        # Get services states
        under_test = alignak_data.get('service', params=params)

        self.assertTrue(under_test)
        self.assertTrue(under_test['_items'])
        self.assertTrue(under_test['_status'])
